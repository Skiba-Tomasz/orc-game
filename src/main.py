import pygame, sys
from time import sleep

from settings import Settings
from character import Character
from projectile import *
from map import Map
from enemy import Enemy
from attackable import Attackable
class Main:
	SETTINGS = Settings()

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((Main.SETTINGS.screen_width, Main.SETTINGS.screen_height), pygame.RESIZABLE)
		Main.SETTINGS.screen_width = self.screen.get_rect().width
		Main.SETTINGS.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Let me out")

		self.player = Character((10,4))
		self.map = Map((Main.SETTINGS.screen_width, Main.SETTINGS.screen_height), (0,0), self.player)
		self.bgSprites = pygame.sprite.Group()
		self.bgSprites.empty()
		self.bgSprites.add(self.map)
		self.bgSprites.add(self.map.envObjects)
		

		self.controllableSprites = pygame.sprite.Group()
		self.controllableSprites.empty()
		self.controllableSprites.add(self.player)

		#self.projectile = Projectile(ProjectileType.FROST, self.player.direction, (10,5))
		#self.controllableSprites.add(self.projectile)

		self.effectors = pygame.sprite.Group()
		self.effectors.empty()

		self.e = Enemy((12,4))
		if isinstance(self.e, Attackable):
			print("Tak gowno w dupie!")
		else:
			print("Nie, w pizdzie!")
		self.bgSprites.add(self.e)

		self.controllableObjects = [self.player]

		self.stateableObjs = [self.player, self.e]
		self.collidableObjs = [self.player, self.e]
		self.controllableObjects = [self.player]

	def close(self):
		pygame.display.quit()
		pygame.quit()

	def onEvent(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.close()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				self.close()
			elif event.type == pygame.KEYDOWN:
				for contrOb in self.controllableObjects:
					contrOb.onKeyDown(event)
			elif event.type == pygame.KEYUP:
				for contrOb in self.controllableObjects:
					contrOb.onKeyUp(event)

	def draw(self):
		self.screen.fill(Main.SETTINGS.bg_color)
		self.bgSprites.draw(self.screen)
		self.controllableSprites.draw(self.screen)
		self.effectors.draw(self.screen)
		pygame.display.flip()		

	def run(self):
		while True:
			self.onEvent()
			for sObj in self.stateableObjs:
				sObj.calculateState()
			for cObj in self.collidableObjs:
				#print('Cobj: '+ cObj)
				cObj.calculateCollisions(self.bgSprites)
				cObj.calculateCollisions(self.collidableObjs)
			self.effectors.add(self.player.getEffectors())
			for effect in self.effectors:
				effect.calculateState()
			self.cleanOutOfScreenObjects()
			self.map.checkMapChange(self.bgSprites, self.effectors)
			self.draw()
			sleep(0.04)

	def cleanOutOfScreenObjects(self):
		toDelete = []
		for e in self.effectors:
			if e.delete():
				toDelete.append(e)
		self.effectors.remove(toDelete)

if __name__ == '__main__':
	app = Main()
	app.run()