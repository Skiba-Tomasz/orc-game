import pygame

from controllable import Controllable
from direction import Direction
from standardcollider import StandardCollider



class CharacterController(Controllable):
	STATIONARY_FRAME = 1


	def __init__(self, rect, setDirectionProc, getDirectionProc, imageRefreshProc):
		self.isMoving = False
		self.frame = 1
		self.speed = 10
		self.rect = rect
		self.imageRefreshProc = imageRefreshProc
		self.setDirection = setDirectionProc
		self.collider = StandardCollider(self.rect, getDirectionProc)

	def onKeyDown(self, event):
		if event.key == pygame.K_RIGHT:
			self.isMoving = True
			self.setDirection(Direction.RIGHT)
			self.frame = CharacterController.STATIONARY_FRAME
		elif event.key == pygame.K_LEFT:
			self.isMoving = True
			self.setDirection(Direction.LEFT)
			self.frame = CharacterController.STATIONARY_FRAME
		elif event.key == pygame.K_UP:
			self.isMoving = True
			self.setDirection(Direction.UP)
			self.frame = CharacterController.STATIONARY_FRAME
		elif event.key == pygame.K_DOWN:
			self.isMoving = True
			self.setDirection(Direction.DOWN)
			self.frame = CharacterController.STATIONARY_FRAME

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
			self.frame = CharacterController.STATIONARY_FRAME
		self.imageRefreshProc(self.frame)

	def calculateCollisions(self, colliders):
		self.collider.calculateCollisions(colliders)