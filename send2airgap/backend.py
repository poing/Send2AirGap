#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# backend.py

"""
"""


import base64
import datetime

# import cv2
import hashlib
import json
import random

import barcode

# import numpy as np
# import os
import qrcode
import requests
from barcode.writer import ImageWriter
from PIL import Image, ImageTk


class Backend:
    def __init__(self, gui):
        self.gui = gui
        self.ack_code = "000000000000"
        self.chunk_size = 64
        self.queue = []

    # self.after(22000, lambda: alt_image(root))

    def mock_test(self):
        self.gui.qr_image.configure(image="aaa")
        return "aaaa"

    def alt_image(self):
        # self.qr_image.place(x=root.winfo_height(), y=root.winfo_width())
        self.gui.image = Image.open("test_stamp.jpg")
        # self.gui.photo = ImageTk.PhotoImage(self.image)
        self.gui.photo = ImageTk.PhotoImage(self.gui.image)
        # self.qr_image = ttk.Label(root, image=self.photo)
        self.gui.qr_image.configure(image=self.photo)

        # Store a reference to avoid garbage
        self.gui.qr_image.photo = self.photo

    def update_ui(self):
        self.gui.button.configure(state="disabled")

    def run_process(self, text):
        self.gui.confirm_label.configure(text=text)

    def run_loop(self):
        while True:
            self.set_qrcode(random.range(100, 99999999999999999999))

    def cycle_data(self):
        self.set_qrcode()

    def set_qrcode(self):

        global index
        if "index" not in globals():
            index = 0

        active_image = self.queue[index]

        # self.photo = self.generate_qrcode(random.uniform(100, 200))
        # self.photo = self.preamble()
        self.photo = active_image
        # self.gui.photo = ImageTk.PhotoImage(self.photo)
        # self.gui.qr_image.photo = self.photo
        # self.gui.image = self.photo
        # self.gui.image = self.photo
        self.gui.qr_image.configure(image=self.photo)
        self.gui.bottom_center.configure(
            text=f"Sending {index+1} of {len(self.queue)}"
        )
        index = (index + 1) % len(self.queue)

    def generate_qrcode(self, data):
        # foo = [
        #   qrcode.constants.ERROR_CORRECT_L,
        #   qrcode.constants.ERROR_CORRECT_M,
        #   qrcode.constants.ERROR_CORRECT_Q,
        #   qrcode.constants.ERROR_CORRECT_H,
        # ]
        #
        # global index
        # if 'index' not in globals():
        #   index = 0

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            # error_correction=foo[index],
            # box_size=15,
            # border=5,
        )  # L,M,Q,H
        qr.add_data(data)
        qr.make(fit=True)

        # index = (index + 1) % len(foo)

        # Generate the QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert the PIL Image to a Tkinter PhotoImage
        photo = ImageTk.PhotoImage(qr_img)

        # Store a reference to avoid garbage collection
        self.gui.photo = photo

        return photo

    def confirmation(self, value):
        if value == self.ack_code:
            self.gui.bottom_center.configure(text="match")
            self.preamble()
        else:
            self.gui.bottom_center.configure(text="no go")

    # self.gui.barcode_label.configure(image=ack_barcode())

    def ack_barcode(self):
        # ack_code = self.ack_code or '000000000000'
        # self.ack_code = str(self.ack_code) or '000000000000'
        # Generate a barcode for acknowledgement
        # ack_code = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        code128 = barcode.get("code128", self.ack_code, writer=ImageWriter())
        barcode_image = code128.render(
            {
                "module_width": 0.15,
                "module_height": 2,
                "font_size": 3,
                "text_distance": 1.75,
            }
        )
        return ImageTk.PhotoImage(barcode_image)

    def update_barcode(self):

        photo = self.ack_barcode()
        self.gui.barcode_img = photo
        self.gui.barcode_label.configure(image=self.gui.barcode_img)
        self.gui.barcode_label.configure(image=photo)

    # Define the position function
    def position(self, current_pos, bound, size, direction):
        if current_pos <= 0:
            direction = random.uniform(0.0, 1.0)
        elif current_pos >= (bound - size):
            direction = -random.uniform(0.0, 1.0)
        return direction

    # determine data hash
    def hash_data(self, data):
        """Return the SHA-256 hash of the given data."""
        sha256 = hashlib.sha256()
        sha256.update(data.encode("utf-8"))
        return sha256.hexdigest()

    # get data to transmit
    def get_json_data(self):
        # url = 'http://localhost:3000/%s' % random.randrange(5)
        url = "http://localhost:3000/template"
        response = requests.get(url)
        return json.dumps(response.json())

    def chunk_data(self, data):
        """Return a list of chunks from the given data."""
        chunks = []
        for i in range(0, len(data), self.chunk_size):
            chunks.append(data[i : i + self.chunk_size])
        return chunks

    def preamble(self):

        global index
        if "index" not in globals():
            index = 0
        index = 0

        self.ack_code = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        self.queue = []

        transmit_data = self.get_json_data()
        original_hash = self.hash_data(transmit_data)
        chunks = self.chunk_data(transmit_data)

        header = {
            "original_hash": original_hash,
            "num_chunks": len(chunks),
            "ack_code": self.ack_code,
        }
        # self.gui.mainframe.after(1250, self.update_barcode())

        self.queue.append(self.generate_qrcode(header))

        for i, chunk in enumerate(chunks):
            encoded_chunk = base64.b64encode(chunk.encode("utf-8")).decode(
                "utf-8"
            )
            data = {"chunk_number": i, "chunk_data": encoded_chunk}

            # chunk_qr = generate_qrcode(json_chunk)
            # display_image(chunk_qr)
            self.queue.append(self.generate_qrcode(data))

        self.update_barcode()

    """

    json_data > hash > chunks > preamble > qr_chunks

    """
