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
from PIL import Image, ImageTk, ImageGrab  # To capture and display images


class MockVideoCapture:
    def __init__(self, root):
        self.root = root  # Reference to the root window
        self.is_opened = True

    def isOpened(self):
        return self.is_opened

    def read(self):
        try:
            # Capture the current content of the tkinter window
            x0 = self.root.winfo_rootx()
            y0 = self.root.winfo_rooty()
            x1 = x0 + self.root.winfo_width()
            y1 = y0 + self.root.winfo_height()

            # Grab the content of the window as an image
            img = ImageGrab.grab(bbox=(x0, y0, x1, y1))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            return True, frame
        except Exception as e:
            print(f"Error capturing window: {e}")
            return False, None

    def release(self):
        self.is_opened = False


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

        # top left - large area for some display
        top_left = ttk.Label(root, text="Top Left")
        top_left.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # right center
        right_center = ttk.Label(root, text="Right Center")
        right_center.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=5)

        # bottom row
        bottom_row = ttk.Label(root, text="Bottom Row")
        bottom_row.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        # Mocked camera
        self.cap = MockVideoCapture(root)

        # Display what the mocked camera "sees"
        self.camera_label = ttk.Label(root, text="Camera View")
        self.camera_label.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
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
