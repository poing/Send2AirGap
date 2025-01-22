#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_11.py

from unittest.mock import patch, MagicMock

# Mock ImageTk.PhotoImage globally for the test
with patch('PIL.ImageTk.PhotoImage', MagicMock(return_value="MockPhotoImage")):

    # Original content of cv_mock_10.py starts here
    import cv2
    import numpy as np

    class MockVideoCapture:
        def __init__(self, source):
            self.source = source
            self.is_opened = True

        def read(self):
            # Simulate a valid frame
            return True, np.zeros((480, 640, 3), dtype=np.uint8)

        def isOpened(self):
            return self.is_opened

        def release(self):
            self.is_opened = False

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
        with patch('cv2.VideoCapture', return_value=MockVideoCapture(0)):
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Cannot open camera")
                return
            ret, frame = cap.read()
            if ret:
                print("Displaying frame")
            else:
                print("Error: Cannot read frame")
            cap.release()

    if __name__ == "__main__":
        display_mock_camera()


