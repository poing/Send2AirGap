#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_7.py

import cv2
import numpy as np
from unittest.mock import patch
from tkinter import ttk
from PIL import Image, ImageTk


width=1920
height=1080
padding=75

# Mock class to simulate cv2.VideoCapture
class MockVideoCapture:
    def __init__(self, video_source):
        self.video_source = video_source
        self.frames = [self.generate_fake_frame(i) for i in range(300)]  # 100 fake frames
        self.index = 0

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
        
        # I want to put the ttk.Frame() here.
        #mainframe = ttk.Frame(frame, padding="3 3 12 12")
        #cv2.imread('test_stamp.png') 

        #image = Image.open("test_stamp.png")
        #photo = ImageTk.PhotoImage(self.image)
        # self.qr_image = ttk.Label(root, image=self.photo)
        #self.gui.qr_image.configure(image=self.photo)
        #cv2.imread(photo)

        #image = Image.open("test_stamp.png")
        #photo = ImageTk.PhotoImage(image)

        #cv2.imshow(photo, photo)  # Display the image instead of trying to display a PhotoImage
        
        # Load the stamp image
        stamp_image = cv2.imread('test_stamp.jpg', cv2.IMREAD_UNCHANGED)
        if stamp_image is not None:
            # Resize the stamp image if needed
            scale_factor = 1  # Scale down to 20% of the original size
            new_width = int(stamp_image.shape[1] * scale_factor)
            new_height = int(stamp_image.shape[0] * scale_factor)
            resized_stamp = cv2.resize(stamp_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Define position for overlay (top-left corner of the stamp)
            x_offset, y_offset = 100, 100  # Change these values for desired position

            # Overlay the stamp onto the frame
            y1, y2 = y_offset, y_offset + resized_stamp.shape[0]
            x1, x2 = x_offset, x_offset + resized_stamp.shape[1]

#             # Handle alpha channel if present
#             if resized_stamp.shape[2] == 4:  # RGBA image
#                 alpha_s = resized_stamp[:, :, 3] / 255.0
#                 alpha_l = 1.0 - alpha_s
# 
#                 for c in range(3):  # Blend each color channel
#                     frame[y1:y2, x1:x2, c] = (
#                         alpha_s * resized_stamp[:, :, c] +
#                         alpha_l * frame[y1:y2, x1:x2, c]
#                     )
#             else:  # RGB image
                
            frame[y1:y2, x1:x2] = resized_stamp

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


