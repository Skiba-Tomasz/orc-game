from abc import ABC, abstractmethod

class Controllable:

	@abstractmethod
	def onKeyDown(self, event):
		pass

	@abstractmethod
	def onKeyUp(self, event):
		pass