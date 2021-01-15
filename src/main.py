import pygame, sys
from settings import Settings
class Main:
	SETTINGS = Settings()

	def __init__(self):
		pygame.init()
		self.frames = 0;
		self.screen = pygame.display.set_mode((Main.SETTINGS.screen_width, Main.SETTINGS.screen_height), pygame.RESIZABLE)
		Main.SETTINGS.screen_width = self.screen.get_rect().width
		Main.SETTINGS.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Let me out")

	def close(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

	def onEvent(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.close()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				self.close()

	def draw(self):
		self.screen.fill(Main.SETTINGS.bg_color)
		pygame.display.flip()		

	def run(self):
		while True:
			self.onEvent()
			self.draw()
			self.frames += 1
			print(self.frames)



if __name__ == '__main__':
	app = Main()
	app.run()