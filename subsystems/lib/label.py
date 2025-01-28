'''This file contains a wrapper for tkinter labels!'''
import tkinter as tk
import numpy
from PIL import Image, ImageTk
from subsystems.lib.simplefancy import generateColorBox
from settings import *
from subsystems.lib.render import *

class LabelWrapper:
    '''A wrapper for tkinter labels'''
    def __init__(self, root, size, offset = (0,0), place = (0,0), bg = "#ffffff", instructions = None):
        self.offset = offset
        self.size = size
        self.section = tk.Label(root, width=size[0], height=size[1], bg=bg, highlightthickness=0, bd=0, image = ImageTk.PhotoImage(TEST_IMAGE))
        self.section.pack()
        self.position = place
        self.shown = True
        self.section.place(x = place[0], y = place[1])
        self.blankConnected = CONNECTED_ALLIANCE_BACKGROUND.copy()
        self.blankDisconnected = DISCONNECTED_ALLIANCE_BACKGROUND.copy()

    def update(self, image:numpy.ndarray):
        '''Updates the label's image to the given array'''
        img = ImageTk.PhotoImage(image)
        self.section.configure(image = img)
        self.section.image = img
    
    def hide(self):
        '''Hides the label by moving it far off screen'''
        self.section.place(x = 5000, y = 0)
        self.shown = False
    
    def show(self):
        '''Shows the label by placing it back to its proper position'''
        self.section.place(x = self.position[0], y = self.position[1])
        self.shown = True