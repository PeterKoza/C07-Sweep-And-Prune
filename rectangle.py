import random

class Rectangle():
    def __init__(self, x1, y1, x2, y2, color='red'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dtx = random.randrange(-100, 100) /10
        self.dty = random.randrange(-100, 100) /10
        self.color = color
        self.id = None
        self.velocity = random.randrange(-100, 100) /100
        self.isRunning = False

    def draw(self, g):
        self.g = g
        if self.id != None:
            self.g.delete(self.id)
        self.id = self.g.create_rectangle(self.x1, self.y1,
                                          self.x2, self.y2,
                                          fill=self.color)

    def delete(self):
        self.g.delete(self.id)

    def isOut(self, width, height):
        isXout = self.x1 < 0 or self.x2 > width
        isYout = self.y1 < 0 or self.y2 > height
        return isXout or isYout 
        
    def move(self, dx=0, dy=0):
        if self.x1 + dx < 0 or self.x2 > self.w:
            self.dtx *= -1
            dx *= -1
        if self.y1 + dy < 0 or self.y2 > self.h:
            self.dty *= -1
            dy *= -1
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.g.move(self.id, dx, dy)

    def resize(self, newX2, newY2):
        self.x2 = newX2
        self.y2 = newY2
        self.g.coords(self.id, self.x1,self.y1,
                              self.x2, self.y2)
        
    def setXYinOrder(self):
        if self.x2 < self.x1:
            self.x1, self.x2 = self.x2, self.x1
        if self.y2 < self.y1:
            self.y1, self.y2 = self.y2, self.y1
        

    def changeColor(self, col):
        self.color = col
        self.g.itemconfig(self.id, fill=col)

    def isClicked(self, e):
        return self.x1 <= e.x <= self.x2  and  self.y1 <= e.y <= self.y2

    def moveWithEuler(self):
        self.move(self.dtx*self.velocity, self.dty*self.velocity)
        if self.isRunning:
            self.g.after(50, self.moveWithEuler)

    def startMoving(self, w, h):
        self.w = w
        self.h = h
        self.isRunning = True

    def stopMoving(self):
        self.isRunning = False


