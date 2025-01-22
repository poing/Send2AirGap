#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_1.py

import cv2
import numpy as np
from unittest.mock import patch

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
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add a white rectangle to simulate a QR code
        cv2.rectangle(frame, (200, 150), (440, 330), (255, 255, 255), -1)
        # Overlay the frame index for debugging
        cv2.putText(frame, f"Frame {index}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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


