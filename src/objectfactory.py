import pygame

from pygame.sprite import Sprite
from pygame.surface import Surface
from wall import *
class ObjectFactory:

	def produce(self, character, position):
		position = (48*position[0], 48*position[1])
		if character == '1':
			return Wall(position, (48, 48), WallType.BRICK, True)
		elif character == '2':
			return Wall(position, (48, 48), WallType.GROUND, True)
		return None