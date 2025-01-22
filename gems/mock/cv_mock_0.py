#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_0.py

import cv2
from unittest.mock import MagicMock, patch
import numpy as np
import pytest

# Mock function to replace cv2.VideoCapture
class MockVideoCapture:
    def __init__(self, video_source):
        self.video_source = video_source
        self.frames = [self.generate_fake_frame() for _ in range(10)]  # Create 10 fake frames
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
    def generate_fake_frame():
        # Create a blank image with a QR code-like pattern
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(frame, (200, 150), (440, 330), (255, 255, 255), -1)  # A white rectangle simulating a QR code
        return frame

@pytest.fixture
def mock_video_capture():
    with patch('cv2.VideoCapture', return_value=MockVideoCapture(0)):
        yield

def test_qr_code_detection(mock_video_capture):
    # Your function that uses cv2.VideoCapture
    cap = cv2.VideoCapture(0)
    assert cap.isOpened()  # Ensure the mock behaves like a camera

    for _ in range(10):
        ret, frame = cap.read()
        assert ret  # The mock should return a frame
        assert frame is not None  # Frame should not be None
        # Further tests, like detecting QR codes in the frame
        # For example:
        qr_detector = cv2.QRCodeDetector()
        decoded_info, points, _ = qr_detector.detectAndDecode(frame)
        assert decoded_info == ""  # Since the mock frame has no real QR code

    cap.release()
