import pygame

from pygame.sprite import Sprite
from pygame.surface import Surface
from wall import *
from enemy import Enemy
from direction import Direction
class ObjectFactory:

	def produce(self, character, position):
		position = (48*position[0], 48*position[1])
		if character == '1':
			return Wall(position, (48, 48), WallType.BRICK, True)
		elif character == '2':
			return Wall(position, (48, 48), WallType.GROUND, True)
		elif character == 'q':
			return Enemy(position, 3, 20, 4)
		elif character == 'w':
			return Enemy(position, 2, 1, 12)
		elif character == 'e':
			return Enemy(position, 0, 8, 6)
		return None