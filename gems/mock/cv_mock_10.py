#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_10.py

import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from tkinter import ttk
from PIL import Image, ImageTk

from send2airgap import Backend


width=1920
height=1080
padding=75


class guiMock:

    def __init__(self, gui):
        self.gui = gui

    def configure(self, **kwargs):
        # Dummy to ignore this. 
        return self.gui

    def place(self, **kwargs):
        # Dummy to ignore this. 
        return self.gui


    def foobar(self):
        return self.gui
        
# Mock class to simulate cv2.VideoCapture
class MockVideoCapture:
    def __init__(self, video_source):
        self.video_source = video_source
        self.frames = [self.generate_fake_frame(i) for i in range(300)]  # 100 fake frames
        self.index = 0

        self.backend = Backend(self)

        #self.qr_image = guiMock(self)
        ##print(self.backend.mock_test())
        #self.test = self.backend.generate_qrcode("sdfsdf")

        #self.qr_image = guiMock(self)
        #self.qr_image.photo = (
        #    None  # Store a reference to avoid garbage collection
        #)
        #self.qr_image.place(x=0, y=0)  # Adjust the position as needed
        #
        #foo = self.backend.alt_image()

        
    def isOpened(self):
        return True

    def read(self):
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            self.index += 1
            return True, frame
        else:
            return False, None

    def release(self):
        pass

    @staticmethod
    def generate_fake_frame(index):
        # Create a blank image with a QR code-like rectangle
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Use formula for target window
        cv2.rectangle(frame, (int((width+padding)-width), int((height+padding)-height)), (int(width-padding), int(height-padding)), (255, 255, 255), -1)
        cv2.putText(frame, "Insert ttk.Frame() here.", (int(width/2)-200,int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Load and overlay an image
        try:

            image = Image.open("test_stamp.jpg").convert("RGB")
            image_cv = np.array(image)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

            x_offset = width // 2 - image_cv.shape[1] // 2
            y_offset = height // 2 - image_cv.shape[0] // 2
            frame[y_offset:y_offset + image_cv.shape[0], x_offset:x_offset + image_cv.shape[1]] = image_cv
            
        except FileNotFoundError:
            cv2.putText(
                frame,
                "Image not found",
                (width // 2 - 100, height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # root window
        #root.title('Broadcast Window')

        # Overlay the frame index for debugging
        cv2.putText(frame, f"Frame {index}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        return frame

def display_mock_camera():
    # Patch cv2.VideoCapture to use the mock
    with patch('cv2.VideoCapture', return_value=MockVideoCapture(0)):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Failed to open mocked camera")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Display the mocked camera output
            cv2.imshow("Mocked Camera View", frame)

            # Break on pressing 'q'
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Call the function to run the mocked camera display
display_mock_camera()


