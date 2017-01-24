import threading
import time



class BPCD(threading.Thread):
    """
    Broad phase collision detection algorithm. It is based on comparing each two pair rectangle if they are in collision.
    Class also measure time and number of collisions.

    atributes:
		self.collisions: (int) number of collisions
		self.rectangles: (array) of Rectangles
		self.time: (int) time for algorithm
		self.isRuning: (boolean) Is algoritm running?
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.collisions = 0
        self.rectangles = []
        self.time = 0
        self.isRuning = False


    def stopCounting(self):
        """Stops algorithm"""
        self.isRuning = False

    
    def startCounting(self, rectangles):
        """
        Starts algorithm and loads rectangles

        Args:
	    rectangles: (array) of Rectangles
	"""
        self.rectangles = rectangles
        self.isRuning = True


    def run(self):
        """Infinity loop. If algorithms is running than computing works or the thread is put to sleep."""
        while True:
            if self.isRuning:
                time.sleep(0.2)
                self.collisionDetection()
            else:
                time.sleep(0.5)


    def collisionDetection(self):
        """
        In this method every two rectangles are detected on collision.
        During the detection it measures time of the detection and it counts colissions. 
        """
        rectanglesInCollision = set()
        collisions = 0
        start = time.time()
        for i in range(len(self.rectangles)):
            for j in range(i+1, len(self.rectangles)):
                if self.collision(self.rectangles[i], self.rectangles[j]):
                    rectanglesInCollision.add(self.rectangles[i])
                    rectanglesInCollision.add(self.rectangles[j])
                    collisions += 1
                end = time.time()
                self.collisions = collisions
                self.time = end - start
                self.makrAsCollided(rectanglesInCollision)
	
    
    def collision(self, A, B):
        """
        Mothod which evaluates collision of rectangles A and B

        Args:
            A: (Rectangle) first rectangle
	    B: (Rectangle) second rectangle

        Returns:
	    (boolean) Value of collision
        """
        Xcollision = (A.x1 + A.width) >= B.x1  and  A.x1 <= (B.x1 + B.width)
        Ycollision = (A.y1 + A.height) >= B.y1  and  A.y1 <= (B.y1 + B.height)
        return Xcollision and Ycollision


    def makrAsCollided(self, rectanglesInCollision):
        """Method changes collision property of rectangle"""
        for rec in self.rectangles:
            if rec in rectanglesInCollision:
                rec.inCollision = True
            else:
                rec.inCollision = False


    def collisionInfo(self):
        """
        Returns:
    	    len(self.rectangles): number of rectangles 
	    self.collisions: number of collisions
	    self.time: time of duration algorithm 
        """
        return len(self.rectangles), self.collisions, self.time
