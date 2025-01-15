#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# receiver.py

import ast

import cv2
from tqdm import tqdm

# import json


class QRDecoder:
    def __init__(self, camera_id=0, delay=1, window_name="OpenCV QR Code"):
        self.camera_id = camera_id
        self.delay = delay
        self.window_name = window_name
        self.qcd = cv2.QRCodeDetector()
        self.camera = cv2.VideoCapture(camera_id)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 1080, 720, 360
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 1920, 1280, 640
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        self.scanned = None
        self.received_chunks = []
        self.received_hash = None
        self.reassembly_failed = False
        self.pbar = None
        self.header = None
        self.num_chunks = None
        self.ack_code = None

    def process_header(self, payload):
        # print(payload)
        if payload["original_hash"] != self.header:
            print("header")
            self.ack_code = payload["ack_code"]
            self.header = payload["original_hash"]
            self.num_chunks = payload["num_chunks"]
            # Create the progress bar here
            self.pbar = tqdm(
                total=self.num_chunks, desc=self.ack_code, leave=True
            )
            # self.num_chunks = None

    def process_code(self, s):
        payload = ast.literal_eval(s)
        # print(type(payload))
        if isinstance(payload, dict):
            if "original_hash" in payload:
                self.process_header(payload)
            else:
                if self.num_chunks:
                    self.store_chunks(self.received_chunks, payload)
                    # num_items = len(self.received_chunks)

                    # print(num_items)

    # store new chunk
    def store_chunks(self, chunk_tuple, chunk_code):

        if chunk_code not in chunk_tuple:
            chunk_tuple.append(chunk_code)

            # update progress bar
            self.pbar.update(1)

    # qrcode outline, green/red
    def outline_qrcode(self, frame, points, state):
        color = (0, 255, 0) if state else (0, 0, 255)
        return cv2.polylines(frame, [points.astype(int)], True, color, 8)

    def run(self):
        # Loop until there are no more frames to read from the camera
        while self.camera.isOpened():
            # Start a new dataset
            self.received_chunks = []
            self.num_chunks = None

            # Loop until a complete dataset is received
            while (
                self.num_chunks is None
                or len(self.received_chunks) < self.num_chunks
            ):
                streaming, frame = self.camera.read()
                if streaming:
                    detected, decoded_info, points, _ = (
                        self.qcd.detectAndDecodeMulti(frame)
                    )
                    if detected:
                        for s, p in zip(decoded_info, points):
                            if s and not (self.scanned == s):
                                self.scanned = s
                                self.process_code(s)
                                self.outline_qrcode(frame, p, True)
                            else:
                                self.outline_qrcode(frame, p, False)

                    cv2.imshow(self.window_name, frame)

                else:
                    print("Camera stream ended.")
                    break

                key = cv2.waitKey(self.delay)
                if key & 0xFF == ord("q"):
                    break

            # Check if the dataset is complete
            # if self.num_chunks and len(self.received_chunks) ==
            #  self.num_chunks:
            #    break

        cv2.destroyWindow(self.window_name)


#     def run(self):
#         while True:
#             # Start a new dataset
#             self.received_chunks = []
#             #self.header = None
#             self.num_chunks = None
#
#             # Loop until a complete dataset is received
#             while True:
#                 streaming, frame = self.camera.read()
#                 if streaming:
#                     detected, decoded_info, points, _ =
#                        self.qcd.detectAndDecodeMulti(frame)
#                     if detected:
#                         for s, p in zip(decoded_info, points):
#                             #print('detected')
#                             if s and not (self.scanned == s):
#                                 #print('new')
#                                 self.scanned = s
#                                 self.process_code(s)
#                                 self.outline_qrcode(frame, p, True)
#                             else:
#                                 self.outline_qrcode(frame, p, False)
#                     cv2.imshow(self.window_name, frame)
#                 else:
#                     print('Camera not detected.')
#                     break
#
#                 if cv2.waitKey(self.delay) & 0xFF == ord('q'):
#                     break
#
#                 # Check if the dataset is complete
#                 if self.num_chunks:
#                     if len(self.received_chunks) == self.num_chunks:
#                         break
#
#             # Process the complete dataset here
#             #print("Complete dataset received:", self.received_chunks)
#
#             if cv2.waitKey(self.delay) & 0xFF == ord('q'):
#                 break
#
#         cv2.destroyWindow(self.window_name)

if __name__ == "__main__":
    qr_decoder = QRDecoder()
    qr_decoder.run()
