#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# #! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_9.py

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

    def read(self):
        frame = self.frames[self.index]
        self.index = (self.index + 1) % len(self.frames)
        return True, frame

    def generate_fake_frame(self, index):
        """Generate a fake frame and overlay the image."""
        # Create a blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw a placeholder rectangle
        cv2.rectangle(
            frame,
            (padding, padding),
            (width - padding, height - padding),
            (255, 255, 255),
            -1
        )

        # Add placeholder text
        cv2.putText(
            frame,
            f"Frame {index}",
            (padding + 10, padding + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Load and overlay an image
        try:
            image = Image.open("test_stamp.png").convert("RGB")
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

        return frame

    def release(self):
        pass

# Example of usage
if __name__ == "__main__":
    mock_capture = MockVideoCapture("video_source")
    success, frame = mock_capture.read()
    if success:
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
    cv2.destroyAllWindows()


