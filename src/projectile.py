import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from direction import Direction
from collidable import Collidable
from enum import Enum
from settings import Settings

class ProjectileType(Enum):
	FROST = '../img/frost_bolt.png'
	FIRE = '../img/fire_bolt.png'

class Projectile(Sprite, Collidable):
	MAX_FRAMES = 2
	FRAME_HEIGHT = 137
	FRAME_WIDHT = 128
	ANIMATION_STEPING =  2# value f.e. 10 means that each 10-th frame animation frame will be changed

	def __init__(self, projectileType, direction, position):
		super().__init__()
		self.speed = 15
		self.direction = direction
		self.frame = 0
		self.size = 48
		self.spriteSheet = pygame.image.load(projectileType.value)
		self.prapareSprite(self.frame)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]
		self.timelapsed = 0
		self.animationDirection = 1

	def calculateState(self):
		if self.frame < Projectile.MAX_FRAMES and self.frame >= 0:
			self.timelapsed += 1
			if self.timelapsed % Projectile.ANIMATION_STEPING == 0:
				self.prapareSprite(self.frame)
				self.frame += self.animationDirection
		else:
			self.animationDirection *= -1
			self.frame += self.animationDirection
		if self.direction == Direction.DOWN:
			self.rect.y += self.speed
		elif self.direction == Direction.UP:
			self.rect.y -= self.speed
		elif self.direction == Direction.LEFT:
			self.rect.x -= self.speed
		elif self.direction == Direction.RIGHT:
			self.rect.x += self.speed

	def prapareSprite(self, frame):
		self.image = Surface((Projectile.FRAME_HEIGHT,Projectile.FRAME_HEIGHT))
		spX = Projectile.FRAME_WIDHT * frame
		spY = 0
		self.image.blit(self.spriteSheet, (0, 0), (spX, spY, Projectile.FRAME_HEIGHT, Projectile.FRAME_HEIGHT))
		self.image.set_colorkey((0, 0, 0))
		self.image =  pygame.transform.scale(self.image, (self.size, self.size))
		if self.direction == Direction.DOWN:
			self.image = pygame.transform.rotate(self.image, -90)
		elif self.direction == Direction.UP:
			self.image = pygame.transform.rotate(self.image, 90)
		elif self.direction == Direction.LEFT:
			self.image = pygame.transform.flip(self.image, True, False)

	def delete(self):
		s = Settings()
		if self.rect.x  + 2 * self.size < 0 or self.rect.x - self.size > s.screen_width or self.rect.y + 2 * self.size < 0 or self.rect.y - self.size > s.screen_height:
			return True
		return False
