#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

"""
cv_mock_6.py - Mock camera includes the BroadcastWindow within the frame
"""

import cv2
import numpy as np
import time
from tkinter import Canvas, Tk


width=1920
height=1080


class BroadcastWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()
        self.draw_content()

    def draw_content(self):
        # Example content (replace with your desired BroadcastWindow content)
        self.canvas.create_rectangle(50, 50, 250, 150, fill="blue", outline="black")
        self.canvas.create_text(150, 100, text="BroadcastWindow", fill="white", font=("Arial", 14))

    def render_to_array(self):
        self.root.update_idletasks()
        self.root.update()
        # Capture the canvas content as an array
        self.canvas.postscript(file="temp_canvas.ps", colormode="color")
        img = cv2.imread("temp_canvas.ps")  # Use Pillow if preferred for better control
        return img


class MockVideoCapture:
    def __init__(self, broadcast_window):
        self.broadcast_window = broadcast_window
        self.index = 0

    def isOpened(self):
        return True

    def read(self):
        # Generate a frame with embedded BroadcastWindow content
        frame = self.generate_fake_frame(self.index)
        self.index += 1
        return True, frame

    def release(self):
        pass

    def generate_fake_frame(self, index):
        # Create a blank canvas for the frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Get the content from the BroadcastWindow
        broadcast_content = self.broadcast_window.render_to_array()
        resized_content = cv2.resize(broadcast_content, (int(width/2),int(height/2)))  # Resize to fit in frame

        # Embed the content in the center of the mock frame
        x_offset = (640 - 320) // 2
        y_offset = (480 - 240) // 2
        frame[y_offset:y_offset + 240, x_offset:x_offset + 320] = resized_content

        # Overlay debugging text for the frame index
        cv2.putText(frame, f"Frame {index}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame


if __name__ == "__main__":
    # Create BroadcastWindow without displaying it
    broadcast_window = BroadcastWindow(width=320, height=240)

    # Initialize the mocked camera
    mock_camera = MockVideoCapture(broadcast_window)

    # OpenCV display loop with 300 seconds timeout
    start_time = time.time()
    while True:
        ret, frame = mock_camera.read()
        if not ret:
            break

        cv2.imshow("Mock Camera Feed", frame)

        # Break after 300 seconds or on 'q' key press
        if (time.time() - start_time > 300) or (cv2.waitKey(30) & 0xFF == ord('q')):
            break

    cv2.destroyAllWindows()


