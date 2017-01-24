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
                self.isRuning = False

        def startCounting(self, rectangles):
                self.rectangles = rectangles                
                if not len(self.endPointsX):
                        self.setPoints()
                else:
                        self.removePoints()
                        self.addPoints()
                self.isRuning = True

        def run(self):
                while True:
                        if self.isRuning:
                                time.sleep(0.2)                                
                                self.sortByValue()
                                self.setPairManager()
                                self.collisionDetection()
                        else:
                                time.sleep(0.5)

        def setPairManager(self):
                self.n= max(self.rectanglesID)+1
                self.pairManagerX = [[0] * self.n for _ in range(self.n)]
                self.pairManagerY = [[0] * self.n for _ in range(self.n)]
                
        def setPoints(self):                
                for r in self.rectangles:
                        self.adding(r)

        def removePoints(self):
                self.rectanglesID=set()
                self.endPointsX=[]
                self.endPointsY=[]
                for r in self.rectangles:
                        self.adding(r)
                        

        def addPoints(self):
                for r in self.rectangles:
                        if not r.id in self.rectanglesID:
                                self.adding(r)

        def adding(self,r):
                self.rectanglesID.add(r.id)
                self.endPointsX.append(r.endx1)
                self.endPointsY.append(r.endy1)
                self.endPointsX.append(r.endx2)
                self.endPointsY.append(r.endy2)                
                        
        def sortByValue(self):
                self.endPointsX = sorted(self.endPointsX, key =lambda point: point.value)
                self.endPointsY = sorted(self.endPointsY, key =lambda point: point.value)

        def collisionDetection(self):
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
                c = 0
                for i in range(self.n):
                        for j in range(self.n):
                                if self.pairManagerX[i][j] and self.pairManagerY[i][j]:
                                        c+=1
                return c//2

        def detectionX(self):
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
                for rec in self.rectangles:
                        if rec.id in rectanglesInCollision:
                                rec.inCollision = True
                        else:
                                rec.inCollision = False

        def collisionInfo(self):
                return len(self.rectangles), self.collisions, self.time
