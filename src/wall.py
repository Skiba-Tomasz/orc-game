import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from enum import Enum

from backgroundsprite import BackgroundSprite


class WallType(Enum):
		BRICK = 'wall_brick.png'
		GROUND = 'wall_ground.png'

class Wall(Sprite, BackgroundSprite):

	def __init__(self, position, size, wallType, solid):
		super().__init__()
		BackgroundSprite.__init__(self, solid)
		self.wallType = wallType
		self.image = pygame.image.load('../img/'+wallType.value);
		self.image = pygame.transform.scale(self.image, (size))
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

