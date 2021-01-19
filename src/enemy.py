import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from direction import Direction
from attackable import Attackable
from wall import Wall

class Enemy(Sprite, Attackable):
	STATIONARY_FRAME = 1

	def __init__(self, position):
		super().__init__()
		self.spriteID = 2
		self.hp = 2
		self.spriteSize = 48
		self.speed = 12
		self.frame = 1
		self.isMoving = False
		self.direction = Direction.DOWN
		self.spriteSheet = pygame.image.load('../img/goblins.png')
		self.prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48

	def prapareSprite(self, frame):
		size = self.spriteSize
		self.image = Surface((25,25))
		spTopLeft = size * self.spriteID * 3
		spX = spTopLeft + size * frame
		spY = self.direction.value * size
		self.image.blit(self.spriteSheet, (0, 0), (spX+11, spY+23, 25, 25))
		self.image = pygame.transform.scale(self.image, (size,size))
		self.image.set_colorkey((0, 0, 0))



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
			self.frame = Enemy.STATIONARY_FRAME
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
		derection = self.direction
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