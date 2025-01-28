'''This file contains classes all about the visual objects the user sees'''

import math
from subsystems.lib.render import placeOver
from subsystems.lib.fancy import *
from settings import *

'''Point Stuff'''
def subtractP(coord1: tuple|list, coord2: tuple|list):
    '''Subtracts (x1,y1) by (x2,y2) given in (x,y) format'''
    return (coord1[0]-coord2[0],coord1[1]-coord2[1])


'''Hitboxes'''

class CircularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific ciruclar range'''
    def __init__(self, r:int = 10, ix = 0, iy = 0):
        '''Circular detection box will be centered!'''
        self.r, self.ix, self.iy = r, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy): 
        '''Returns whether or not the mouse is in range of interaction'''
        return math.sqrt((rmx-self.ix)**2 + (rmy-self.iy)**2) <= self.r
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getR(self): return self.r
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setR(self, nr): self.r = nr

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

class FixedRegionPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific region. Not movable by interaction.'''
    def __init__(self, pointA:tuple|list = (0,0), pointB:tuple|list = (10,10)):
        '''Point A and Point B are two opposite corners of a region!'''
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        pass
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the region of interaction'''
        return (self.pointA[0] < rmx) and (rmx < self.pointB[0]) and (self.pointA[1] < rmy) and (rmy < self.pointB[1])
    def getPosition(self): return self.pointA
    def getX(self): return self.pointA[0]
    def getY(self): return self.pointA[1]
    def getRegion(self): return (self.pointA, self.pointB)
    def setPosition(self, position: tuple|list): 
        self.pointB = subtractP(self.pointB, subtractP(self.pointA, position))
        self.pointA = position
    def setRegion(self, pointA, pointB):
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))

'''Visual Objects'''

class VisualObject:
    '''Basic template for Visual Objects'''
    def keepInFrame(self, minX, minY, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < minX or maxX < pos[0] or pos[1] < minY or maxY < pos[1]:
            self.positionO.setPosition((max(minX,min(pos[0],maxX)), max(minY,min(pos[1],maxY))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)
    def keyAction(self, keys):
        pass

class ButtonVisualObject(VisualObject):
    '''A button.'''
    def __init__(self, name, pos:tuple|list, img:Image, img2:Image):
        self.type = "button"
        self.name = name
        self.lastInteraction = time.time()
        self.img = img
        self.img2 = img2
        self.positionO = RectangularPositionalBox((img.width,img.height), pos[0], pos[1])
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.img2 if active else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    
class DummyVisualObject(VisualObject):
    '''I sit around doing nothing and can store data.'''
    def __init__(self, name, pos:tuple|list, data = None):
        self.type = "dummy"
        self.name = name
        self.lastInteraction = time.time()
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        self.data = data
    def tick(self, img, visualactive, actives):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, minX, minY, maxX, maxY):
        pass
    def getInteractable(self,rmx,rmy):
        return False

class IconVisualObject(VisualObject):
    '''An icon, basically a fancy button.'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, icon:Image, size:tuple|list = (29,29)):
        self.type = "icon"
        self.name = name
        self.lastInteraction = time.time()
        self.img = generateIcon(icon, False, size)
        self.img2 = generateIcon(icon, True, size)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.img2 if visualactive else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

    
class ToggleVisualObject(VisualObject):
    '''A toggle, basically a fancy button/icon, but this time with two faces, on and off that switch on rising detection of clicks!'''
    # generateIcon(img, active = False, size = (29,29), color = "")
    def __init__(self, name, pos:tuple|list, iconOn:Image, iconOff:Image, size:tuple|list = (29,29), runOn = lambda: 0, runOff = lambda: 0):
        self.type = "icon"
        self.name = name
        self.lastInteraction = time.time()
        self.img = generateIcon(iconOn, False, size)
        self.img2 = generateIcon(iconOff, False, size)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.active = 0
        self.state = False
        self.runOn = runOn
        self.runOff = runOff
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.active +=1
        else: self.active = 0
        if self.active == 1:
            self.state = not(self.state)
            if self.state == True: self.runOn()
            if self.state == False: self.runOff()
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
        if active: placeOver(img, displayText(self.name, "s", (0,0,0,200)), self.positionO.getPosition(), False)
    def setToggle(self, runOn, runOff):
        self.runOn = runOn
        self.runOff = runOff
    def updatePos(self, rmx, rmy):
        pass
    
class CheckboxVisualObject(VisualObject):
    '''A checkbox, basically a simple toggle.'''
    def __init__(self, name, pos:tuple|list, size:tuple|list = (29,29), state = False):
        self.type = "checkbox"
        self.name = name
        self.lastInteraction = time.time()
        self.img = generateIcon(generateColorBox(size, (255,0,0,255)), False, size)
        self.img2 = generateIcon(generateColorBox(size, (0,255,0,255)), False, size)
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.active = 0
        self.state = state
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.active +=1
        else: self.active = 0
        if self.active == 1: self.state = not(self.state)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

    
class TextButtonPushVisualObject(VisualObject):
    '''A button, but it has text! and it resets itself after some ticks!'''
    def __init__(self, name, text:Image, pos:tuple|list, ticks = 60):
        self.type = "button"
        self.name = name
        self.lastInteraction = time.time()
        temp = displayText(str(text), "m")
        self.img = generateIcon(temp, False, (temp.width, temp.height))
        self.img2 = generateIcon(temp, True, (temp.width,temp.height))
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0], pos[1])
        self.lastPressed = 9999999
        self.state = False
        self.time = ticks
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        if active: self.lastPressed = 0
        else: self.lastPressed += 1
        self.state = (self.time > self.lastPressed)
        placeOver(img, self.img2 if self.state else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass

class BranchButtonVisualObject(VisualObject):
    '''A custom button for branches.'''
    def __init__(self, name, pos:tuple|list, branch):
        self.type = "branch button"
        self.name = name
        self.lastInteraction = time.time()
        self.imgDisconnected = generateBorderBox((94,94), 3, (50,50,50,255))
        placeOver(self.imgDisconnected, displayText(str(branch), "l", bold = True), (50, 50), True)
        self.imgRed = generateBorderBox((94,94), 3, (255,0,0,255))
        placeOver(self.imgRed, displayText(str(branch), "l", bold = True), (50, 50), True)
        self.imgBlue = generateBorderBox((94,94), 3, (0,0,255,255))
        placeOver(self.imgBlue, displayText(str(branch), "l", bold = True), (50, 50), True)
        self.img = self.imgDisconnected
        self.positionO = RectangularPositionalBox((self.img.width,self.img.height), pos[0] - 50, pos[1] - 50)
    def tick(self, img, visualactive, active):
        if active: self.lastInteraction = time.time()
        placeOver(img, self.img2 if active else self.img, self.positionO.getPosition(), False)
    def setAlliance(self, alliance):
        if alliance == "blue": self.img = self.imgBlue
        elif alliance == "red": self.img = self.imgRed
        else: self.img = self.imgDisconnected
    def updatePos(self, rmx, rmy):
        pass