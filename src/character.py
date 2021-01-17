import pygame
import copy
from pygame.sprite import Sprite
from pygame.surface import Surface
from enum import Enum

from controllable import Controllable
from wall import Wall
#from drawable import Drawable

class Direction(Enum):
		DOWN = 0
		LEFT = 1
		RIGHT = 2
		UP = 3

class Character(Sprite, Controllable):
	SPRITE_SIZE = 48
	STATIONARY_FRAME = 1

	def __init__(self, position):
		super().__init__()
		self.characterSpriteID = 1
		self.hp = 5
		self.speed = 10
		self.frame = 1
		self.isMoving = False
		self.direction = Direction.UP
		self.spriteSheet = pygame.image.load('../img/characters.png')
		self.prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48

	def prapareSprite(self, frame):
		size = Character.SPRITE_SIZE
		self.image = Surface((size,size))
		spTopLeft = size * (self.characterSpriteID * 3)
		spX = spTopLeft + size * frame
		spY = self.direction.value * size
		self.image.blit(self.spriteSheet, (0, 0), (spX, spY, size, size))
		self.image.set_colorkey((0, 0, 0))



	def onKeyDown(self, event):
		if event.key == pygame.K_RIGHT:
			self.isMoving = True
			self.direction = Direction.RIGHT
			self.frame = Character.STATIONARY_FRAME
		elif event.key == pygame.K_LEFT:
			self.isMoving = True
			self.direction = Direction.LEFT
			self.frame = Character.STATIONARY_FRAME
		elif event.key == pygame.K_UP:
			self.isMoving = True
			self.direction = Direction.UP
			self.frame = Character.STATIONARY_FRAME
		elif event.key == pygame.K_DOWN:
			self.isMoving = True
			self.direction = Direction.DOWN
			self.frame = Character.STATIONARY_FRAME

	def onKeyUp(self, event):
		if event.key == pygame.K_RIGHT and self.direction == Direction.RIGHT:
			self.isMoving = False
		elif event.key == pygame.K_LEFT and self.direction == Direction.LEFT:
			self.isMoving = False
		elif event.key == pygame.K_UP and self.direction == Direction.UP:
			self.isMoving = False
		elif event.key == pygame.K_DOWN and self.direction == Direction.DOWN:
			self.isMoving = False

	def calculateState(self):
		if self.isMoving:
			self.frame += 1
			if self.frame == 3:
				self.frame = 0
			if self.direction == Direction.UP:
				self.rect.y -= self.speed
			elif self.direction == Direction.DOWN:
				self.rect.y += self.speed
			elif self.direction == Direction.RIGHT:
				self.rect.x += self.speed
			elif self.direction == Direction.LEFT:
				self.rect.x -= self.speed
		else:
			self.frame = Character.STATIONARY_FRAME
		self.prapareSprite(self.frame)

	def calculateCollisions(self, colliders):
		walls = pygame.sprite.Group()
		for ob in colliders:
			if type(ob) is Wall:
				walls.add(ob)
		self.onWallCollision(walls)
		walls.empty()


	def onWallCollision(self, walls):
		collisions = pygame.sprite.spritecollide(self, walls, False)
		derection = copy.deepcopy(self.direction)
		for collision in collisions:
			print(collision)
			if collision.collidable:
				if derection == Direction.UP:
					self.rect.y = collision.rect.y + collision.rect.height
				elif derection == Direction.DOWN:
					self.rect.y = collision.rect.y - self.rect.height
				elif derection == Direction.RIGHT:
					self.rect.x = collision.rect.x - collision.rect.width
				elif derection == Direction.LEFT:
					self.rect.x = collision.rect.x + collision.rect.width
				collisions.clear()