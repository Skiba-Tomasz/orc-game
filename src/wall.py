import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from enum import Enum


class WallType(Enum):
		BRICK = 'wall_brick.png'
		GROUND = 'wall_ground.png'

class Wall(Sprite):

	def __init__(self, position, size, wallType, collidable):
		super().__init__()
		self.collidable = collidable
		self.wallType = wallType
		self.image = pygame.image.load('../img/'+wallType.value);
		self.image = pygame.transform.scale(self.image, (size))
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

