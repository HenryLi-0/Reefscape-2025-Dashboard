'''This file makes sure that everything the program needs is set and ready to run!'''

'''Test import all major modules'''
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import os, numpy, time, math, robotpy
from settings import *

'''Test import all subsystems'''
from subsystems.lib.counter import *
from subsystems.lib.fancy import *
from subsystems.lib.label import *
from subsystems.lib.render import *
from subsystems.lib.simplefancy import *
from subsystems.lib.visuals import *
from subsystems.interface import *
from subsystems.window import *

class Check:
    def check():
        print("Finished Checks")
    def error(message):
        print(f"The check has detected an issue: {message}")