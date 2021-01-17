import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from charactercontroller import CharacterController
from direction import Direction

class Character(Sprite):
	SPRITE_SIZE = 48

	def __init__(self, position):
		super().__init__()
		self.characterSpriteID = 1
		self.hp = 5
		self.spriteSheet = pygame.image.load('../img/characters.png')
		self.direction = Direction.DOWN
		self.prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48
		self.controller = CharacterController(self.rect, self.setDirection, self.getDirection, self.prapareSprite)


	def prapareSprite(self, frame):
		size = Character.SPRITE_SIZE
		self.image = Surface((size,size))
		spTopLeft = size * (self.characterSpriteID * 3)
		spX = spTopLeft + size * frame
		spY = self.direction.value * size
		self.image.blit(self.spriteSheet, (0, 0), (spX, spY, size, size))
		self.image.set_colorkey((0, 0, 0))

	def setDirection(self, direction):
		self.direction = direction
		self.controller.direction = direction

	def getDirection(self):
		return self.direction