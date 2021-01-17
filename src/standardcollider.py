import pygame
from pygame.sprite import Sprite
from direction import Direction
from wall import Wall


class StandardCollider:

	def __init__(self, rect, getDirectionProc):
		self.rect = rect
		self.getDirection = getDirectionProc



	def calculateCollisions(self, colliders):
		print(self.rect)
		walls = pygame.sprite.Group()
		for ob in colliders:
			if type(ob) is Wall:
				walls.add(ob)
		self.onWallCollision(walls)
		walls.empty()


	def onWallCollision(self, walls):
		collisions = pygame.sprite.spritecollide(self, walls, False) #copy might not be usefull
		derection = self.getDirection()
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