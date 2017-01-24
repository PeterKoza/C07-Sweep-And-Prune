import random

from tkinter import *
from rectangle import *


class MainCanvas():
    """
    Class wich is responsible for behavior of rectangles on canvas.
    It has also mode property (add, remove, update)

    atributes:
        self.canvas: (object) tkinter object
        self.width: (int) width of canvas
        self.height: (int) height of canvas
        self.isPlaying: (boolean) Are rectangles moving? 
        self.mode: (string) type of mode which was selected. Options: "ADD", "REMOVE", "UPDATE"
        self.rectangles: (array) of Rectangles
        self.actualRectangle: (Rectangle) actually creating rectangle
        self.clicked: (array[int]) indexes of clicked rectangles
        self.ex: (int) last x coord clicked
        self.ey: (int) last y coord clicked
    """
    def __init__(self, canvas, w, h):
        self.canvas = canvas
        self.width = w
        self.height = h
        self.canvas.bind("<Button-1>", self.onClick)
        self.isPlaying = False
        self.mode = None
        self.rectangles = self.createRandomRectangles(70)
        self.actualRectangle = None
        self.clicked = None
        self.ex = None
        self.ey = None


    def setMode(self, mode):
        """
        Sets mode which provides this canvas. (add, remove, update)

        Args:
            mode: (string) name
        """
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
        """
        When canvas is clicked it behaves based on mode.

        Args:
            e: click event
        """
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


    # CREAT NEW RECTANGLE   ==============================================
    def createNewRectangle(self, e):
        """It creates little rectangle"""
        self.actualRectangle = Rectangle(e.x, e.y, e.x+3, e.y+3)
        self.actualRectangle.draw(self.canvas, self.width, self.height)
        self.rectangles.append(self.actualRectangle)

    def setSizesOfRectangle(self, e):
        """Resizes just created rectangle."""
        self.actualRectangle.resize(e.x, e.y)

    def unbindCreatingRectangle(self, e):
        """After releasing button on mouse it unbinds resizing rectangle"""
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.actualRectangle.setXYinOrder()
        self.actualRectangle = None


    # REMOVE RECTANGLE   ===================================================
    def removeRectangle(self, e):
        """Removes rectangles on which were clicked if mode is REMOVE"""
        clicked = self.getClickedRectangles(e)
        for i in clicked:
            self.rectangles[i].delete()
            self.rectangles[i] = None
        self.rectangles = [rec for rec in self.rectangles if rec != None]


    # UPDATE RECTANGLE   ===================================================
    def updateRectangle(self, e): 
        """During updating rectangle by mouse it finds clicked rectangles and starting positions"""
        self.clicked = self.getClickedRectangles(e)
        self.ex, self.ey = e.x, e.y
            
    def moveRectagles(self, e):
        """Moves each selected rectangle during updating."""
        for i in self.clicked:
            self.rectangles[i].move(e.x-self.ex, e.y-self.ey, True)
        self.ex, self.ey = e.x, e.y

    def unbindMovingRectagles(self, e):
        """Releases moved rectangles."""
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.clicked = None


    #=======================================================================
    #-----------------------------------------------------------------------
    def createRandomRectangles(self, n):
        """
        Creates n random positioned rectangles.

        Args:
            n: (int) number of random rectangles
        """
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
        """
        Args:
            e: click event

        Returns:
            array of indexes(int) which rectangles were clicked
        """
        clicked = []
        for i in range(len(self.rectangles)):
            if self.rectangles[i].isClicked(e):
                clicked.append(i)
        return clicked


    #-----------------------------------------------------
    def play(self):
        """Statrs all rectangles to move in animation"""
        if self.isPlaying:
            return
        self.isPlaying = True
        self.removeRecanglesOutOfCanvas()
        for rec in self.rectangles:
            rec.startMoving()
            rec.moveWithEuler()


    def stop(self):
        """Stops all rectangles to move in animation"""
        self.isPlaying = False
        for rec in self.rectangles:
            rec.stopMoving()
        

    #---------------------------------------------------
    def removeRecanglesOutOfCanvas(self):
        """Removes all rectangles which has piece of themselfs out of canvas."""
        rectangles = []
        for rec in self.rectangles:
            if rec.isOut():
                rec.delete()
            else:
                rectangles.append(rec)
        self.rectangles = rectangles
    
        

    

