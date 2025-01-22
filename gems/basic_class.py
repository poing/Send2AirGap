#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# basic_class.py

class FirstChild:
    def __init__(self, gui):
        self.gui = gui
        self.gui = "one"
        
        self.gui.qr_image.configure(x="lkj")

    def foobar(self):
        return self.gui
        

class SecondChild:
    def __init__(self, gui):
        self.gui = gui

    def configure(self, **kwargs):
        # Dummy to ignore this. 
        return self.gui

    def foobar(self):
        return self.gui

class MainClass:
    def __init__(self, gui):

        # Assign the parent object to the 'parent' attribute
        self.gui = gui

        self.gui = FirstChild(gui)
        self.qr_image = SecondChild(gui)

        
        #self.gui.configure(new="do nothing")
       
    def print_parent(self):
        #child = FirstChild("John")
        return f"Parent: {self.gui.foobar()}"


# Example usage:

main_class_instance = MainClass('foo')

# Print the result using the defined method
print(main_class_instance.print_parent())