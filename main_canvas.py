import random

from tkinter import *
from rectangle import *


class MainCanvas():
    def __init__(self, canvas, w, h):
        self.canvas = canvas
        self.width = w
        self.height = h
        self.canvas.bind("<Button-1>", self.onClick)
        self.isPlaying = False
        self.mode = None
        self.rectangles = self.createRandomRectangles(20)
        self.actualRectangle = None
        self.clicked = None
        self.ex = None
        self.ey = None

    def setMode(self, mode):
        self.mode = mode
        if(mode == "ADD"):
            self.canvas.configure(cursor = "tcross")
        elif(mode == "REMOVE"):
            self.canvas.configure(cursor = "target")
        elif(mode == "UPDATE"):
            self.canvas.configure(cursor = "fleur")
        else:
            self.canvas.configure(cursor = "")

    def onClick(self, e):
        if(self.mode == "ADD"):
            self.createNewRectangle(e)
            self.canvas.bind("<B1-Motion>", self.setSizesOfRectangle)
            self.canvas.bind("<ButtonRelease-1>", self.unbindCreatingRectangle)
        elif(self.mode == "REMOVE"):
            self.removeRectangle(e)
        elif(self.mode == "UPDATE"):
            self.updateRectangle(e)
            self.canvas.bind("<B1-Motion>", self.moveRectagles)
            self.canvas.bind("<ButtonRelease-1>", self.unbindMovingRectagles)

    # CREAT NEW RECTANGLE
    def createNewRectangle(self, event):
        self.actualRectangle = Rectangle(event.x, event.y, event.x+3, event.y+3)
        self.actualRectangle.draw(self.canvas, self.width, self.height)
        self.rectangles.append(self.actualRectangle)

    def setSizesOfRectangle(self, e):
        self.actualRectangle.resize(e.x, e.y)

    def unbindCreatingRectangle(self, e):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.actualRectangle.setXYinOrder()
        if self.isPlaying:
            self.actualRectangle.startMoving()
            self.actualRectangle.moveWithEuler()
        self.actualRectangle = None

    # REMOVE RECTANGLE
    def removeRectangle(self, e):
        clicked = self.getClickedRectangles(e)
        for i in clicked:
            self.rectangles[i].delete()
            self.rectangles[i] = None
        self.rectangles = [rec for rec in self.rectangles if rec != None]

    # UPDATE RECTANGLE
    def updateRectangle(self, e): 
        self.clicked = self.getClickedRectangles(e)
        self.ex, self.ey = e.x, e.y
            
    def moveRectagles(self, e):
        for i in self.clicked:
            self.rectangles[i].move(e.x-self.ex, e.y-self.ey, True)
        self.ex, self.ey = e.x, e.y

    def unbindMovingRectagles(self, e):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.clicked = None

    #----------------------------------------------------
    def createRandomRectangles(self, n):
        rectangles = []
        maxWidth = 50
        maxHeight = 50
        for i in range(n):
            centerX = random.randrange(maxWidth, self.width - maxWidth)
            centerY = random.randrange(maxHeight, self.height - maxHeight)
            x1 = random.randrange(centerX - maxWidth, centerX)
            x2 = random.randrange(centerX, centerX + maxWidth)
            y1 = random.randrange(centerY - maxHeight, centerY)
            y2 = random.randrange(centerY, centerY + maxHeight)
            rec = Rectangle(x1, y1, x2, y2)
            rec.draw(self.canvas, self.width, self.height)
            rectangles.append(rec)
        return rectangles

    #-----------------------------------------------------
    def getClickedRectangles(self, e):
        clicked = []
        for i in range(len(self.rectangles)):
            if self.rectangles[i].isClicked(e):
                clicked.append(i)
        return clicked

    #-----------------------------------------------------
    def play(self):
        if self.isPlaying:
            return
        self.isPlaying = True
        self.removeRecanglesOutOfCanvas()
        for rec in self.rectangles:
            rec.startMoving()
            rec.moveWithEuler()

    def stop(self):
        self.isPlaying = False
        for rec in self.rectangles:
            rec.stopMoving()
        
    #---------------------------------------------------
    def removeRecanglesOutOfCanvas(self):
        rectangles = []
        for rec in self.rectangles:
            if rec.isOut():
                rec.delete()
            else:
                rectangles.append(rec)
        self.rectangles = rectangles
    
        

    

