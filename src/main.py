import pygame, sys, random
from time import sleep

from settings import Settings
from character import Character
from projectile import *
from map import Map
from enemy import Enemy
from attackable import Attackable
from gameAI import GameAI

from characterFactory import *

from os import walk

class Main:
	SETTINGS = Settings()
	IS_GAME_OVER = False

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((Main.SETTINGS.screen_width, Main.SETTINGS.screen_height), pygame.RESIZABLE)
		Main.SETTINGS.screen_width = self.screen.get_rect().width
		Main.SETTINGS.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Let me out")



		self.totalEnemies = 0 
		self.totalKilled = 0 
		_, _, filenames = next(walk('../level/'))
		for i in range(len(filenames)):
			file = open('../level/' + filenames[i], 'r')
			data = file.read()
			for d in data:
				if ord(d) >= 97 and ord(d) <=122:
					print(d)
					self.totalEnemies += 1
			#print(self.totalEnemies)

		self.player = CharacterFactory(random.choice(list(CharacterType))).character
		self.map = Map((Main.SETTINGS.screen_width, Main.SETTINGS.screen_height), (0,0), self.player)
		self.bgSprites = pygame.sprite.Group()
		self.bgSprites.empty()
		self.bgSprites.add(self.map)
		self.bgSprites.add(self.map.envObjects)
		self.attackableObjects = pygame.sprite.Group()
		self.attackableObjects.empty()		
		self.attackableObjects.add(self.map.attObjects)

		self.controllableSprites = pygame.sprite.Group()
		self.controllableSprites.empty()
		self.controllableSprites.add(self.player)




		self.effectors = pygame.sprite.Group()
		self.effectors.empty()

		#self.e = Enemy((1,1))
		#self.bgSprites.add(self.e)

		self.controllableObjects = [self.player]

		self.stateableObjs = [self.player]#, self.e]
		self.collidableObjs = [self.player]#, self.e]
		self.controllableObjects = [self.player]


		self.ai = GameAI(8)

		#self.ai.move(self.player, self.bgSprites)#, self.e,)


		self.framesPassed = 0;
		self.generateNextPath = False


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
		self.attackableObjects.draw(self.screen)
		self.killCounter()
		pygame.display.flip()		

	def run(self):
		while not self.player.isDead and self.totalKilled < self.totalEnemies:
			self.onEvent()
			for atOb in self.attackableObjects:
				if(atOb not in self.stateableObjs):
					self.stateableObjs.append(atOb)
				if(atOb not in self.collidableObjs):
					self.collidableObjs.append(atOb)

			if self.framesPassed % Main.SETTINGS.pathfindingFreq == 0:
				self.generateNextPath = True
				self.framesPassed = 0
			for atOb in self.attackableObjects:
				if isinstance(atOb, Enemy) and (self.generateNextPath and atOb.isReadyForNewPath()) or atOb.isPathCompleted():
					self.ai.move(self.player, atOb, self.bgSprites)
					self.generateNextPath = False
					self.framesPassed = 0
					#atOb.calculateCollisions(self.bgSprites)
					#atOb.calculateCollisions(self.collidableObjs)
					#atOb.calculateCollisions(self.effectors)
			#if self.e.isReadyForNewPath() and self.ai.enemyPath is not None and len(self.ai.enemyPath) > 0:
			#	self.e.path = self.ai.enemyPath
			self.effectors.add(self.player.getEffectors())
			for effect in self.effectors:
				effect.calculateState()
			for sObj in self.stateableObjs:
				sObj.calculateState()
			for cObj in self.collidableObjs:
				#print('Cobj: '+ cObj)
				cObj.calculateCollisions(self.bgSprites)
				cObj.calculateCollisions(self.collidableObjs)
				cObj.calculateCollisions(self.effectors)
			self.clearOutOfScreenObjects()
			self.clearBodies()
			self.map.checkMapChange(self.bgSprites, self.effectors, self.attackableObjects, self.stateableObjs, self.collidableObjs)
			self.draw()
			self.framesPassed += 1
			


			sleep(0.04)
		self.afterGameFinished()


	def clearOutOfScreenObjects(self):
		toDelete = []
		for e in self.effectors:
			if e.delete():
				toDelete.append(e)
		self.effectors.remove(toDelete)


	def clearBodies(self):
		toDelete = []
		for e in self.attackableObjects:
			if isinstance(e, Enemy) and e.delete():
				self.totalKilled += 1
				if str(self.map.part) not in self.map.killed:
					self.map.killed[str(self.map.part)] = [e.initialPosition]
				else:
					self.map.killed[str(self.map.part)].append(e.initialPosition)
				toDelete.append(e)
			if len(toDelete) > 0:
				print(toDelete)
				if toDelete in self.bgSprites:
					print('from bg')
					self.bgSprites.remove(toDelete)
				if toDelete[0] in self.stateableObjs:
					print('from st')
					self.stateableObjs.remove(toDelete[0])
				if toDelete[0] in self.collidableObjs:
					print('from col')
					self.collidableObjs.remove(toDelete[0])
				if toDelete[0] in self.attackableObjects:
					print('from col')
					self.attackableObjects.remove(toDelete[0])

	def afterGameFinished(self):
		if self.totalKilled == self.totalEnemies:
			WLstr = 'YOU WON!'
			WLcol = (0,255,0)
		else:
			WLstr = 'YOU LOST!'
			WLcol = (255,0,0)
		fontWON = pygame.font.Font('freesansbold.ttf', 60)
		textWON = fontWON.render( WLstr, True, WLcol, (0, 0, 128))
		textRectWON = textWON.get_rect()
		textRectWON.center = (Main.SETTINGS.screen_width / 2, Main.SETTINGS.screen_height / 2 - 100)

		fontGO = pygame.font.Font('freesansbold.ttf', 60)
		textGO = fontGO.render('GAME OVER', True, (255, 100, 0), (0, 0, 128))
		textRectGO = textGO.get_rect()
		textRectGO.center = (Main.SETTINGS.screen_width / 2, Main.SETTINGS.screen_height / 2)

		fontRE = pygame.font.Font('freesansbold.ttf', 30)
		textRE = fontRE.render('RESTART?', True, (255, 100, 0), (0, 0, 128))
		textRectRE = textRE.get_rect()
		textRectRE.center = (Main.SETTINGS.screen_width / 2, Main.SETTINGS.screen_height / 2 + 100)

		fontYES = pygame.font.Font('freesansbold.ttf', 30)
		textYES = fontYES.render('YES', True, (255, 100, 0), (0, 0, 128))
		textRectYES = textYES.get_rect()
		textRectYES.center = (Main.SETTINGS.screen_width / 2, Main.SETTINGS.screen_height / 2 + 135)

		fontNO = pygame.font.Font('freesansbold.ttf', 30)
		textNO = fontNO.render('NO', True, (255, 100, 0), (0, 0, 128))
		textRectNO = textNO.get_rect()
		textRectNO.center = (Main.SETTINGS.screen_width / 2, Main.SETTINGS.screen_height / 2 + 170)

		while True:
			#if self.totalKilled == self.totalEnemies:
			self.screen.blit(textWON, textRectWON)
			self.screen.blit(textGO, textRectGO)
			self.screen.blit(textRE, textRectRE)
			self.screen.blit(textYES, textRectYES)
			self.screen.blit(textNO, textRectNO)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse=pygame.mouse.get_pos()
					if mouse[0] in range (textRectYES.x ,textRectYES.x + textRectYES.w) and  mouse[1]in range (textRectYES.y, textRectYES.y + textRectYES.h):
						print('YES')
						Main.IS_GAME_OVER = True
						self.__init__()
						self.run()
					if mouse[0] in range (textRectNO.x ,textRectNO.x + textRectNO.w) and  mouse[1]in range (textRectNO.y, textRectNO.y + textRectNO.h):
						print('NO')
						pygame.quit()
						quit()
					pygame.display.update()

	def killCounter(self):
		fontKILL = pygame.font.Font('freesansbold.ttf', 20)
		textKILL = fontKILL.render(str(self.totalKilled) + ' / ' + str(self.totalEnemies) + ' KILLED', True, (255, 100, 0), (0, 0, 128))
		textRectGO = textKILL.get_rect()
		textRectGO.topleft = (0,0)
		self.screen.blit(textKILL, textRectGO)

if __name__ == '__main__':
	app = Main()
	app.run()