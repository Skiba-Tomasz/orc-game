from abc import ABC, abstractmethod
from collidable import Collidable

class Attackable(Collidable):
	@abstractmethod
	def onBeeingAttacked(self, attacker):
		pass