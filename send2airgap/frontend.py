#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# frontend.py

"""
This is a revised base window to establish the desired layout.
Using tk instead of ttk.
"""

import tkinter as tk

from backend import Backend


class BroadcastWindow:

    def __init__(self, root):
        self.mainframe = tk.Frame(root)
        self.backend = Backend(self)

        self.x_direction = 0  # Initialize x_direction
        self.y_direction = 0  # Initialize y_direction
        self.photo = None
        # self.barcode_label = None

        # application icon
        # icon = tk.PhotoImage(file = './icons/custom-256x256.png')
        # root.wm_iconphoto(False, icon)

        # root window
        root.title("Broadcast Window")
        root.configure(background="white")

        # window size
        # width = root.winfo_screenwidth() /2
        height = root.winfo_screenheight()
        width = height
        root.geometry("%dx%d" % (width, height))

        # alt - full screen window
        # root.attributes('-fullscreen', True)

        # prepare 3x2 grid
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=18)
        root.rowconfigure(0, weight=19)
        root.rowconfigure(1, weight=1)

        # place initial center text
        self.bottom_center = tk.Label(root, text=None, bg="white")
        self.bottom_center.grid(
            column=0, row=1, columnspan=4, sticky=tk.S, padx=5, pady=5
        )

        # place initial image
        self.qr_image = tk.Label(root, image=None, bg="white")
        self.qr_image.photo = (
            None  # Store a reference to avoid garbage collection
        )
        self.qr_image.place(x=0, y=0)  # Adjust the position as needed

        # place confirmation box label
        self.confirm_label = tk.Label(
            root, text="Confirm:", bg="white", justify="right"
        )
        self.confirm_label.grid(column=0, row=1, sticky=tk.SE, padx=0, pady=10)

        # place confirmation input box
        self.confirm = tk.StringVar()
        self.confirm_entry = tk.Entry(
            root, width=20, justify="left", textvariable=self.confirm
        )
        self.confirm_entry.grid(column=1, row=1, sticky=tk.SW, padx=0, pady=5)
        self.confirm_entry.focus()

        # bind acknowledge function
        self.confirm_entry.bind("<Return>", self.acknowledge)

    # acknowledge process
    def acknowledge(self, *args):
        value = self.confirm_entry.get()
        # self.bottom_center.configure(text=value)
        self.backend.confirmation(value)
        self.confirm.set("")

        # return focus to entry
        self.confirm_entry.focus_set()

    # place the confirmation barcode
    def place_barcode(self):
        self.barcode_img = self.backend.ack_barcode()
        self.barcode_label = tk.Label(root, image=self.barcode_img, bg="white")
        self.barcode_label.grid(column=3, row=1, sticky=tk.SE, padx=0, pady=0)

    # animate the image
    def qr_animate(self):

        self.x_direction = self.backend.position(
            self.qr_image.winfo_x(),
            root.winfo_width(),
            self.qr_image.winfo_width(),
            self.x_direction,
        )

        self.y_direction = self.backend.position(
            self.qr_image.winfo_y(),
            root.grid_bbox(0, 0, 1)[3],
            self.qr_image.winfo_height(),
            self.y_direction,
        )

        new_x = self.qr_image.winfo_x() + self.x_direction
        new_y = self.qr_image.winfo_y() + self.y_direction

        self.qr_image.place(x=new_x, y=new_y)
        root.after(30, self.qr_animate)  # Schedule next frame after 30 ms

    # qrcode loop process
    def qr_loop(self):
        self.backend.cycle_data()
        # self.bottom_center.configure(text='Awaiting confirmation... ')
        root.after(1250, self.qr_loop)

    # initiate core functions
    def start(self):
        self.place_barcode()
        self.backend.preamble()
        self.qr_loop()
        self.qr_animate()


root = tk.Tk()
broadcast_window = BroadcastWindow(root)
broadcast_window.start()
root.mainloop()
