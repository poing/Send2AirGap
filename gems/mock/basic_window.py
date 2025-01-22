#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

"""
This is a generic base window to establish the desired layout.
"""

import tkinter as tk
from tkinter import ttk


class BroadcastWindow:

    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")

        # root window
        root.title('Broadcast Window')

        # window size
        # root.attributes('-fullscreen', True)
        width= root.winfo_screenwidth() / 2
        height= root.winfo_screenheight() / 2          
        root.geometry("%dx%d" % (width, height))

        # setup the grid
        root.columnconfigure(0, weight=19)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=19)
        root.rowconfigure(1, weight=1)

        # top left - large area
        top_left = ttk.Label(root, text="Top Left")
        top_left.grid(column=0, row=0, sticky=tk.SE, padx=5, pady=5)

        # right center
        right_center = ttk.Label(root, text="Right Center")
        right_center.grid(column=1, row=0, rowspan=2, sticky=tk.E, padx=5, pady=5)

        # top right
        top_right = ttk.Label(root, text="Top Right")
        top_right.grid(column=1, row=0, sticky=tk.NE, padx=5, pady=5)

        # bottom left
        bottom_left = ttk.Label(root, text="Bottom Left")
        bottom_left.grid(column=0, row=1, sticky=tk.SW, padx=5, pady=5)

        # bottom center
        bottom_center = ttk.Label(root, text="Bottom Center")
        bottom_center.grid(column=0, row=1, columnspan=2, sticky=tk.S, padx=5, pady=5)

        # bottom right
        bottom_right = ttk.Label(root, text="Bottom Right")
        bottom_right.grid(column=1, row=1, sticky=tk.SE, padx=5, pady=5)

root = tk.Tk()
BroadcastWindow(root)
root.mainloop()

# root.update()
# print('top left:', root.grid_bbox(0,0))
# print('top right:', root.grid_bbox(1,0))
# print('bottom left:', root.grid_bbox(1,0))
# print('bottom right:', root.grid_bbox(1,1))

