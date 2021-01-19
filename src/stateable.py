from abc import ABC, abstractmethod

class Stateable:

	@abstractmethod
	def calculateState(self):
		pass