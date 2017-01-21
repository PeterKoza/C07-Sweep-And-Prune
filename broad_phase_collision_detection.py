import threading
import time

class BPCD(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.collisions = 0
		self.rectangles = []
		self.time = 0
		self.isRuning = False

	def stopCounting(self):
		self.isRuning = False

	def startCounting(self, rectangles):
		self.rectangles = rectangles
		self.isRuning = True

	def run(self):
		while True:
			if self.isRuning:
				time.sleep(0.2)
				self.collisionDetection()
			else:
				time.sleep(0.5)

	def collisionDetection(self):
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
		Xcollision = (A.x1 + A.width) >= B.x1  and  A.x1 <= (B.x1 + B.width)
		Ycollision = (A.y1 + A.height) >= B.y1  and  A.y1 <= (B.y1 + B.height)
		return Xcollision and Ycollision

	def makrAsCollided(self, rectanglesInCollision):
		for rec in self.rectangles:
			if rec in rectanglesInCollision:
				rec.inCollision = True
			else:
				rec.inCollision = False

	def collisionInfo(self):
		return len(self.rectangles), self.collisions, self.time
