import pygame, sys
from time import sleep

from settings import Settings
from character import Character
from map import Map
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

		self.topSprites = pygame.sprite.Group()
		self.topSprites.empty()
		self.topSprites.add(self.player)
		self.controllableObjects = [self.player.controller]

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
		self.topSprites.draw(self.screen)
		pygame.display.flip()		

	def run(self):
		while True:
			self.onEvent()
			for contrOb in self.controllableObjects:
				contrOb.calculateState()
				contrOb.calculateCollisions(self.bgSprites)
			self.map.checkMapChange(self.bgSprites)
			self.draw()
			sleep(0.04)


if __name__ == '__main__':
	app = Main()
	app.run()