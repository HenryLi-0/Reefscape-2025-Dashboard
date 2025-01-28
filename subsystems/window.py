'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from subsystems.lib.label import LabelWrapper
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.grid()
        self.window.title("Interactable Visual Objects!")
        self.window.geometry("1500x865")
        # self.window.wm_attributes('-alpha', 0.5)
        # self.window.minsize(500,500)
        # self.window.maxsize(500,500)
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsTimestamps = []
        self.mPressed = False
        self.keysPressed = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(TEST_IMAGE)
        self.label = LabelWrapper(self.window, SECTION_DATA[2], SECTION_DATA[0], SECTION_DATA[0], BACKGROUND_COLOR, SECTION_FRAME_INSTRUCTIONS)
        self.blankLabel = self.label.blankConnected

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0: self.mPressed += 1
        else: self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keysPressed, self.mouseScroll)
        self.mouseScroll = 0

        if self.fps > INTERFACE_FPS:
                self.label.update(self.interface.processNone(self.blankLabel))

        now = time.time()
        self.fpsTimestamps.append(now)
        while now-self.fpsTimestamps[0] > FPS_DAMPENING:
            self.fpsTimestamps.pop(0)
        self.fps = round(len(self.fpsTimestamps)/FPS_DAMPENING)

        self.window.after(TICK_MS, self.windowProcesses)

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Interactable Visual Objects {self.interface.ticks}")
        print(self.getFPS())

        if self.label.shown:
            self.label.update(self.interface.processNone(self.blankLabel))

        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999

    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)

        self.window.after(2, self.windowProcesses)
        self.window.after(2, self.windowOccasionalProcesses)
        self.window.after(1, self.windowStartupProcesses)
        self.window.mainloop()