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
		self.speed = 12 #IT HAS TO BE A DEVIDER OF MAP FIELD SIZE! (for now at least)
		self.frame = 1
		self.isMoving = False
		self.direction = Direction.DOWN
		self.spriteSheet = pygame.image.load('../img/goblins.png')
		self.prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48
		self.path = []
		self.nextMove = None

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
		if self.path is not None and len(self.path) > 0 and self.nextMove is None:
			self.nextMove = self.path.pop(0)
		if self.nextMove is not None:
			xTo = self.nextMove.x * 48
			yTo = self.nextMove.y * 48
			print('Enemy position(' + str(self.rect.x) + 'x' + str(self.rect.y) + ' Target position (' + str(xTo) + 'x' + str(yTo) + ')')
			self.isMoving = True
			if xTo < self.rect.x:
				self.direction = Direction.LEFT
			elif xTo > self.rect.x:
				self.direction = Direction.RIGHT
			elif yTo < self.rect.y:
				self.direction = Direction.UP
			elif yTo > self.rect.y:
				self.direction = Direction.DOWN
			if self.rect.x == xTo and self.rect.y == yTo:
				self.nextMove = None
				self.isMoving = False
				
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