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
			enemy = Enemy(position, 3)
		#	self.hp = 10
		#	self.speed = 8 #IT HAS TO BE A DEVIDER OF MAP FIELD SIZE! (for now at least)
			#self.direction = Direction.LEFT
			return enemy
		elif character == 'w':
			return Wall(position, (48, 48), WallType.GROUND, True)
		return None