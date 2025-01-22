#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# cv_mock_5.py

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

"""
cv_mock_4.py - Mock camera sees the BroadcastWindow content
"""

import cv2
import numpy as np
from unittest.mock import patch
from basic_window import BroadcastWindow
import tkinter as tk
from PIL import ImageGrab


class MockVideoCapture:
    def __init__(self, video_source, root_window):
        self.video_source = video_source
        self.frames = [self.generate_fake_frame(i, root_window) for i in range(300)]  # 300 fake frames
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
    def generate_fake_frame(index, root_window):
        # Capture the BroadcastWindow content
        x0 = root_window.winfo_rootx()
        y0 = root_window.winfo_rooty()
        x1 = x0 + root_window.winfo_width()
        y1 = y0 + root_window.winfo_height()
        
        try:
            # Grab the current content of the BroadcastWindow
            window_capture = ImageGrab.grab(bbox=(x0, y0, x1, y1))
            window_frame = cv2.cvtColor(np.array(window_capture), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error capturing window: {e}")
            # Fallback to a black frame if capture fails
            window_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Overlay frame index for debugging
        cv2.putText(window_frame, f"Frame {index}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return window_frame


if __name__ == "__main__":
    root = tk.Tk()
    app = BroadcastWindow(root)
    
    # Create a MockVideoCapture with the root window reference
    mock_camera = MockVideoCapture(0, root)
    
    def update_camera_feed():
        ret, frame = mock_camera.read()
        if ret:
            cv2.imshow("Mock Camera Feed", frame)
        
        # Refresh the OpenCV window every 30ms
        if cv2.waitKey(30) & 0xFF == ord('q'):
            root.destroy()
            cv2.destroyAllWindows()

        root.after(30, update_camera_feed)

    root.after(1000, update_camera_feed)  # Start after 1 second to ensure the window initializes
    root.mainloop()


