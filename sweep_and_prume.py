import threading
import time
import copy

                

class SAP(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.collisions = 0
                self.rectangles = []
                self.rectanglesID = set()
                self.pairManagerX =[]
                self.pairManagerY =[]
                self.endPointsX = [] 
                self.endPointsY = []
                self.time = 0
                self.isRuning = False

        def stopCounting(self):
                """Stops algorithm"""
                self.isRuning = False

        def startCounting(self, rectangles):
                """
                Starts algorithm, loads rectangles, sets endpoint or upgrade endpoints

                Args:
                    rectangles: (array) of Rectangles
                """
                self.rectangles = rectangles                
                if not len(self.endPointsX):
                        self.setPoints()
                else:
                        self.removePoints()
                        self.addPoints()
                self.isRuning = True

        def run(self):
                """Infinity loop. If algorithms is running than computing works or the thread is put to sleep.
                Sorting endpoit by their value.
                """
                while True:
                        if self.isRuning:
                                time.sleep(0.2)                                
                                self.sortByValue()
                                self.setPairManager()
                                self.collisionDetection()
                        else:
                                time.sleep(0.5)

        def setPairManager(self):
                """Creates Pair maneger using list and max id from current rectangles"""
                self.n= max(self.rectanglesID)+1
                self.pairManagerX = [[0] * self.n for _ in range(self.n)]
                self.pairManagerY = [[0] * self.n for _ in range(self.n)]
                
        def setPoints(self):
                """Creates Endpoint list from current rectangles."""
                for r in self.rectangles:
                        self.adding(r)

        def removePoints(self):
                """Remove Endpoints from Endpoint list for removed rectangles"""
                self.rectanglesID=set()
                self.endPointsX=[]
                self.endPointsY=[]
                for r in self.rectangles:
                        self.adding(r)
                        

        def addPoints(self):
                """Add Endpoints into Endpoint list for new rectangles"""
                for r in self.rectangles:
                        if not r.id in self.rectanglesID:
                                self.adding(r)

        def adding(self,r):
                """Generate and directly add Enpoints into list for  given rectangle.
                Args:
                     r: (Rectangle) rectangle
                """
                self.rectanglesID.add(r.id)
                self.endPointsX.append(r.endx1)
                self.endPointsY.append(r.endy1)
                self.endPointsX.append(r.endx2)
                self.endPointsY.append(r.endy2)                
                        
        def sortByValue(self):
                """Sort Endpoints lists by their value"""
                self.endPointsX = sorted(self.endPointsX, key =lambda point: point.value)
                self.endPointsY = sorted(self.endPointsY, key =lambda point: point.value)

        def collisionDetection(self):
                """
                In this method rectangles are detected for collision.
                During the detection it measures time of the detection and it counts colissions. 
                """       
                start = time.time()
                self.InCollisionX=set()
                self.InCollisionY=set()
                self.detectionX()
                self.detectionY()
                self.collisions = self.numberOfCollisions()                
                end = time.time()
                self.time = end - start
                rectanglesInCollision=set()
                for  s in self.InCollisionX & self.InCollisionY:
                        rectanglesInCollision.add(s[0])
                        rectanglesInCollision.add(s[1])
                self.makrAsCollided(rectanglesInCollision)

        def numberOfCollisions(self):
                """
                Method calculate number of collisions and returns it
                Returns:
                       c: (int) number of collisions 
                """
                c = 0
                for i in range(self.n):
                        for j in range(self.n):
                                if self.pairManagerX[i][j] and self.pairManagerY[i][j]:
                                        c+=1
                return c//2

        def detectionX(self):
                """Method itself index endpoints of X axis and calculate collisions on that axis and add collisions in pair manager"""
                for k in range(len(self.endPointsX)-1):
                        for l in range(k+1,len(self.endPointsX)):
                                left = self.endPointsX[k].id
                                if len(self.endPointsX):
                                        right = self.endPointsX[l].id
                                        if (left==right):
                                                break
                                        if not self.endPointsX[k].isMin:
                                                break
                                        else:
                                                self.pairManagerX[left][right]=1
                                                self.pairManagerX[right][left]=1
                                                if left>right:
                                                        self.InCollisionX.add((right,left))  
                                                else:
                                                        self.InCollisionX.add((left,right))
                                                
                                
                                

        def detectionY(self):
                """Method itself index endpoints of Y axis and calculate collisions on that axis and add collisions in pair manager"""
                for k in range(len(self.endPointsY)-1):
                        for l in range(k+1,len(self.endPointsY)):
                                left = self.endPointsY[k].id
                                if len(self.endPointsY):
                                        right = self.endPointsY[l].id
                                        if (left==right):
                                                break
                                        if not self.endPointsY[k].isMin:
                                                break
                                        else:
                                                self.pairManagerY[left][right]=1
                                                self.pairManagerY[right][left]=1
                                                if left>right:
                                                        self.InCollisionY.add((right,left))
                                                else:
                                                        self.InCollisionY.add((left,right))

        def makrAsCollided(self, rectanglesInCollision):
                """Method changes collision property of rectangle"""
                for rec in self.rectangles:
                        if rec.id in rectanglesInCollision:
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
        
