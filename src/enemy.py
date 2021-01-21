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
		self.speed = 4 #IT HAS TO BE A DEVIDER OF MAP FIELD SIZE! (for now at least)
		self.frame = 1
		self.isMoving = False
		self.direction = Direction.DOWN
		self.spriteSheet = pygame.image.load('../img/goblins.png')
		self.__prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48
		self.path = []
		self.nextMove = None

	def isPathCompleted(self):
		if (self.path is None or len(self.path) == 0) and self.nextMove is None and self.isReadyForNewPath():
			return True
		return False

	def isReadyForNewPath(self):
		if self.rect.x % 48 == 0 and self.rect.y % 48 == 0:
			return True
		return False

	def setPath(self, path):
		self.path = path
		self.nextMove = None

	def calculateState(self):
		self.__setMoveFromPath()				
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
		self.__prapareSprite(self.frame)

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

	def __prapareSprite(self, frame):
		size = self.spriteSize
		self.image = Surface((25,25))
		spTopLeft = size * self.spriteID * 3
		spX = spTopLeft + size * frame
		spY = self.direction.value * size
		self.image.blit(self.spriteSheet, (0, 0), (spX+11, spY+23, 25, 25))
		self.image = pygame.transform.scale(self.image, (size,size))
		self.image.set_colorkey((0, 0, 0))

	def __setMoveFromPath(self):
		if self.path is not None and len(self.path) > 0 and self.nextMove is None:
			if len(self.path) > 1 and self.__getMoveDirection(self.path[1].x, self.path[1].y) == self.direction:
				self.path.pop(0)
			self.nextMove = self.path.pop(0)
		if self.nextMove is not None:
			xTo = self.nextMove.x * 48
			yTo = self.nextMove.y * 48
			#print('Enemy position(' + str(self.rect.x) + 'x' + str(self.rect.y) + ' Target position (' + str(xTo) + 'x' + str(yTo) + ')')
			self.isMoving = True
			self.direction = self.__getMoveDirection(xTo, yTo)
			if self.rect.x == xTo and self.rect.y == yTo:
				print('Position reached (' + str(self.rect.x) + 'x' + str(self.rect.y) + ' Target position (' + str(xTo) + 'x' + str(yTo) + ')')
				self.nextMove = None
				self.isMoving = False
				self.__setMoveFromPath()

	def __getMoveDirection(self, xTo, yTo):
		direction = self.direction
		if xTo < self.rect.x:
			direction = Direction.LEFT
		elif xTo > self.rect.x:
			direction = Direction.RIGHT
		elif yTo < self.rect.y:
			direction = Direction.UP
		elif yTo > self.rect.y:
			direction = Direction.DOWN
		return direction