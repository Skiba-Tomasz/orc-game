from abc import ABC, abstractmethod

class Controllable:

	@abstractmethod
	def onKeyDown(self, event):
		pass

	@abstractmethod
	def onKeyUp(self, event):
		pass

	@abstractmethod
	def calculateState(self):
		pass

	@abstractmethod
	def calculateCollisions(self, colliders):
		pass