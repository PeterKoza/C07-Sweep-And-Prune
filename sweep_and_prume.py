import threading
import time

class SAP(threading.Thread):
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
			# TODO: Maros  :)
			#sem napíš tvoj algoritmus
			#collisions += ...
		end = time.time()
		self.collisions = collisions
		self.time = end - start
		# tento riadok odkomentuje, ked to budes mat hotove
		#self.makrAsCollided(rectanglesInCollision)
	

	def makrAsCollided(self, rectanglesInCollision):
		for rec in self.rectangles:
			if rec in rectanglesInCollision:
				rec.inCollision = True
			else:
				rec.inCollision = False

	def collisionInfo(self):
		return len(self.rectangles), self.collisions, self.time
