#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

"""
This is a generic base window to establish the desired layout.
"""

import tkinter as tk
from tkinter import ttk
import cv2
from unittest.mock import patch
import numpy as np
from PIL import Image, ImageTk  # To display OpenCV frames in tkinter

# Mock class to simulate cv2.VideoCapture
class MockVideoCapture:
    def __init__(self, video_source):
        self.video_source = video_source
        self.frames = [self.generate_fake_frame(i) for i in range(100)]  # 100 fake frames
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


class BroadcastWindow:

    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")

        # root window
        root.title('Broadcast Window')

        # window size
        width = root.winfo_screenwidth() // 2
        height = root.winfo_screenheight() // 2
        root.geometry("%dx%d" % (width, height))

        # setup the grid
        root.columnconfigure(0, weight=19)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=19)
        root.rowconfigure(1, weight=1)

        # top left - large area for the camera feed
        self.camera_label = ttk.Label(root, text="Camera Feed")
        self.camera_label.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # Start the mocked camera feed
        self.cap = MockVideoCapture(0)
        self.update_camera_feed()

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a format tkinter can display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        # Schedule the next frame update
        self.camera_label.after(30, self.update_camera_feed)


if __name__ == "__main__":
    root = tk.Tk()
    app = BroadcastWindow(root)
    root.mainloop()
