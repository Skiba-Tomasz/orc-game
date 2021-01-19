from abc import ABC, abstractmethod
from stateable import Stateable

class Collidable(Stateable):
	@abstractmethod
	def calculateCollisions(self, colliders):
		pass