import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from controllable import Controllable
from wall import Wall
from direction import Direction
from projectile import *
from attackable import Attackable

class Character(Sprite, Controllable, Attackable):
	SPRITE_SIZE = 48
	STATIONARY_FRAME = 1

	def __init__(self, position, hp, speed, projectileType, damage, spriteID):
		super().__init__()
		self.characterSpriteID = spriteID
		self.isDead = False
		self.hp = hp
		self.speed = speed
		self.frame = 1
		self.isMoving = False
		self.direction = Direction.RIGHT
		self.spriteSheet = pygame.image.load('../img/characters.png')
		self.__prapareSprite(1)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]*48
		self.rect.y = position[1]*48
		self.projectileType = ProjectileType.FROST
		self.effectors = pygame.sprite.Group()
		self.projectileDamage = damage
		self.effectors.empty()

	def getEffectors(self):
		tmp = self.effectors
		self.effectors = pygame.sprite.Group()
		return tmp

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
		elif event.key == pygame.K_c:
			proj = Projectile(self.projectileType, self.direction, (self.rect.x, self.rect.y), self.projectileDamage)
			self.effectors.add(proj)

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
		if self.hp <= 0:
			self.isDead = True
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
		self.__prapareSprite(self.frame)

	def calculateCollisions(self, colliders):
		walls = pygame.sprite.Group()
		enemies = pygame.sprite.Group()
		for ob in colliders:
			if ob is self :
				continue
			elif isinstance(ob, Wall):
				walls.add(ob)
			elif isinstance(ob, Attackable):
				enemies.add(ob)
		self.onWallCollision(walls)
		walls.empty()
		self.onBeeingAttacked(enemies)
		enemies.empty()

	def onWallCollision(self, walls):
		collisions = pygame.sprite.spritecollide(self, walls, False)
		derection = self.direction
		for collision in collisions:
			#print(collision)
			if collision.solid:
				if derection == Direction.UP:
					self.rect.y = collision.rect.y + collision.rect.height
				elif derection == Direction.DOWN:
					self.rect.y = collision.rect.y - self.rect.height
				elif derection == Direction.RIGHT:
					self.rect.x = collision.rect.x - collision.rect.width
				elif derection == Direction.LEFT:
					self.rect.x = collision.rect.x + collision.rect.width
				collisions.clear()

	def onBeeingAttacked(self, enemies):
		collisions = pygame.sprite.spritecollide(self, enemies, False)
		derection = self.direction
		for collision in collisions:
#			if derection == Direction.UP:
#				self.rect.y = collision.rect.y + collision.rect.height
#			elif derection == Direction.DOWN:
#				self.rect.y = collision.rect.y - self.rect.height
#			elif derection == Direction.RIGHT:
#				self.rect.x = collision.rect.x - collision.rect.width
#			elif derection == Direction.LEFT:
#				self.rect.x = collision.rect.x + collision.rect.width
			self.hp -= 1
			print('Hit!')

	def __prapareSprite(self, frame):
		size = Character.SPRITE_SIZE
		self.image = Surface((size,size))
		spTopLeft = size * self.characterSpriteID * 3
		spX = spTopLeft + size * frame
		spY = self.direction.value * size
		self.image.blit(self.spriteSheet, (0, 0), (spX, spY, size, size))
		self.image.set_colorkey((0, 0, 0))