import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from objectfactory import ObjectFactory
from settings import Settings
from backgroundsprite import BackgroundSprite
from attackable import Attackable
from enemy import Enemy

class Map(Sprite):

	def __init__(self, size, part, character):
		super().__init__()
		self.part = part
		self.size = size;
		self.character = character;
		self.envObjects = pygame.sprite.Group()
		self.envObjects.empty()
		self.attObjects = pygame.sprite.Group()
		self.attObjects.empty()
		self.killed = {}
		self.objectFactory = ObjectFactory()
		self.__loadPart(part)
		self.__prepareBG('../img/bg_brick3.png')
		self.__prepareEnvObj()

	def checkMapChange(self, globalEnvSprites, globalEffectors, globalAttObjects, stat, coli):
		settings = Settings()
		chPos = (self.character.rect.x, self.character.rect.y)
		if chPos[0] < 0:
			tmpPart = (self.part[0]-1, self.part[1])
			newChPos = (self.size[0] - settings.tileSize, chPos[1])
		elif chPos[0] > self.size[0] - settings.tileSize:
			tmpPart = (self.part[0]+1, self.part[1]) 
			newChPos = (settings.tileSize, chPos[1])
		elif chPos[1] < 0:
			tmpPart = (self.part[0], self.part[1]-1) 
			newChPos = (chPos[0], self.size[1] - settings.tileSize)
		elif chPos[1] > self.size[1] - settings.tileSize:
			tmpPart = (self.part[0], self.part[1]+1)
			newChPos = (chPos[0], 0)
		else:
			tmpPart = self.part
			newChPos = chPos

		if tmpPart is not None and tmpPart != self.part:
			self.part = tmpPart
			self.character.rect.x = newChPos[0]
			self.character.rect.y = newChPos[1]
			self.__refreshMap()

			for a in globalAttObjects:
				if a in stat:
					stat.remove(a)
				if a in coli:
					coli.remove(a)


			globalEnvSprites.empty()
			globalEnvSprites.add(self)
			globalEnvSprites.add(self.envObjects)
			globalAttObjects.empty()
			globalAttObjects.add(self.attObjects)
			globalEffectors.empty()
			return True
		return False

	def __prepareBG(self, textureDir):
		texture = pygame.image.load(textureDir)
		texture = pygame.transform.scale(texture, (48*3,48*3))
		textureRect = texture.get_rect();
		self.image = Surface(self.size)
		for x in range(textureRect.width % self.size[0]):
			for y in range(textureRect.height % self.size[1]):
				self.image.blit(texture, (x*textureRect.width, y*textureRect.height), (0, 0, textureRect.width, textureRect.height))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect();
		self.rect.x = 0;
		self.rect.y = 0;

	def __prepareEnvObj(self):
		for y in range(len(self.levelRows)):
			for x in range(len(self.levelRows[y])):
				ob = self.objectFactory.produce(self.levelRows[y][x], (x, y))
				if ob is not None and isinstance(ob, Attackable):
					if isinstance(ob, Enemy) and (str(self.part) not in self.killed or ob.initialPosition not in self.killed[str(self.part)]):
						print('Adding Enemy ' + str(ob.rect.x) + ' ' + str(ob.rect.y))
						self.attObjects.add(ob)
					else:
						print('Enemy was dead ' + str(ob.rect.x) + ' ' + str(ob.rect.y))
				elif ob is not None and isinstance(ob, BackgroundSprite):
					self.envObjects.add(ob)


	def __loadPart(self, part):
		print(part)
		file = open('../level/' + str(part[0]) + '_' + str(part[1]) + '.txt', 'r')
		data = file.read()
		self.levelRows = data.split('\n')
		print(type(self.levelRows))
		print(self.levelRows)

	def __refreshMap(self):
		self.__loadPart(self.part)
		self.envObjects.empty()
		self.attObjects.empty()
		self.__prepareEnvObj()