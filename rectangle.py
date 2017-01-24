import random



class EndPoint():
    """
    Class wich represents boundary in rectangle.
    Each rectangle has four end points(boudaries).

    atributes:
        self.id: (int) id of the rectangle
        self.value: (int) It could by one of the coord: x1, y1, x2, y2.
        self.isMin: (boolean) x1, y1 are mins. x2, y2 aro not. Because they has biger value.
    """
    def __init__(self, value, isMin):
        self.id = 0
        self.value = value
        self.isMin = isMin



class Rectangle():
    """    
                 height
                    ^
    [x1, y1]        |
    
        -------------   -> width
        |           |
        |           |
        |           |
        -------------
                    [x2, y2]


    atributes:
        self.endx1, self.endy1, self.endx2, self.endy2: (object) We need it in sweep and prume algoritm
        self.dtx, self.dty:
        self.color: (string) rectangle color
        self.width: (int) rectangle width
        self.height: (int) rectangle height
        self.id: (int) each rectangle has own id.
        self.velocity: (int) random speed/velocity of rectangle
        self.inCollision: (boolean) says if the rectangle is in collision with other rectangle
        self.isRunning: (boolean) says if the rectangle is moving as animation
    """
    def __init__(self, x1, y1, x2, y2, color='green'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.endx1 = EndPoint(x1, True)
        self.endy1 = EndPoint(y1, True)
        self.endx2 = EndPoint(x2, False)
        self.endy2 = EndPoint(y2, False)
        self.dtx = random.randrange(-100, 100) /10
        self.dty = random.randrange(-100, 100) /10
        self.color = color
        self.width = abs(x1 - x2)
        self.height = abs(y1 - y2)
        self.id = None
        self.velocity = random.randrange(-50, 50) /100
        self.inCollision = False
        self.isRunning = False


    def draw(self, g, w, h):
        """
        This method provides rendering the rectangle on the canvas.
        It is necessary to call it at the beginning to make rectangle visible.

        Args:
            g: Reference to the canvas.
            w: width of the canvas.
            h: height of the canvas
        """
        self.canWidth = w
        self.canHeight = h
        self.g = g
        if self.id != None:
            self.g.delete(self.id)
        self.id = self.g.create_rectangle(self.x1, self.y1,
                                          self.x2, self.y2,
                                          fill=self.color)
        self.endx1.id = self.id
        self.endy1.id = self.id
        self.endx2.id = self.id
        self.endy2.id = self.id


    def delete(self):
        """Remove the rectangle from the canvas."""
        self.g.delete(self.id)


    def isOut(self):
        """
        This method says that the rectangle has piece of itself out of the canvas.

        Returns:
            True or False value
        """
        isXout = self.x1 < 0 or self.x2 > self.canWidth
        isYout = self.y1 < 0 or self.y2 > self.canHeight
        return isXout or isYout 
        

    def move(self, dx=0, dy=0, update=False):
        """
        This method provide moving itself on the canvas during the animation or updating.
        If the object is moving during the animation it is also bouncing from walls.

        Args:
            dx: sliding value on x-axis.
            dy: sliding value on y-axis.
            update: True/Flase. Is the object moving during the animation or during updating by user?
        """
        if not update:
            dx, dy = self.bouncing(dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.endx1.value += dx
        self.endy1.value += dy
        self.endx2.value += dx
        self.endy2.value += dy
        self.g.move(self.id, dx, dy)


    def bouncing(self, dx, dy):
        """
        Checks if bouncing is needable.

        Args:
            dx: sliding value on x-axis.
            dy: sliding value on y-axis.
        Returns:
            new dx, dy values
        """
        if self.x1 + dx <= 0 or self.x2 >= self.canWidth:
            self.dtx *= -1
            dx *= -1
        if self.y1 + dy <= 0 or self.y2 >= self.canHeight:
            self.dty *= -1
            dy *= -1
        return dx, dy


    def resize(self, newX2, newY2):
        """
        During creating rectangle the coordinates of one corner changes.
        And the method provides updating coordinates.

        Args:
            newX2: new X value of one corner.
            newY2: new Y value of one corner.
        """
        self.x2 = newX2
        self.y2 = newY2
        self.endx2.value = newX2
        self.endy2.value = newY2
        self.width = abs(self.x1 - self.x2)
        self.height = abs(self.y1 - self.y2)
        self.g.coords(self.id, self.x1,self.y1,
                              self.x2, self.y2)
     

    def setXYinOrder(self):
        """When creating a new rectangle is finished. We must coordinates of the corners keep in order."""
        if self.x2 < self.x1:
            self.x1, self.x2 = self.x2, self.x1
            self.endx1, self.endx2 = self.endx2, self.endx1
        if self.y2 < self.y1:
            self.y1, self.y2 = self.y2, self.y1
            self.endy1, self.endy2 = self.endy2, self.endy1


    def changeColor(self, col):
        """
        By this method we can change color of the rectangle.

        Args:
            col: (string) Name of a new color.
        """
        self.color = col
        self.g.itemconfig(self.id, fill=col)


    def isClicked(self, e):
        """
        Args:
            e: click event in canvas.

        Returns:
            True when the cick event was inside the rectangle.
        """
        return self.x1 <= e.x <= self.x2  and  self.y1 <= e.y <= self.y2


    def moveWithEuler(self):
        """
        Moves the rectangle in evry 50ms. And also check if the rectangle is in collision and accordingly changes color. 
        """
        self.move(self.dtx * self.velocity, self.dty * self.velocity)
        if self.inCollision:
            self.changeColor("red")
        else:
            self.changeColor("green")
        if self.isRunning:
            self.g.after(50, self.moveWithEuler)


    def startMoving(self):
        """Stops moving rectangle during animation"""
        self.isRunning = True


    def stopMoving(self):
        """Starts moving rectangle during animation"""
        self.isRunning = False


