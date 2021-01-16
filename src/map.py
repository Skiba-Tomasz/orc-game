import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from spriteinterpreter import SpriteInterpreter
from settings import Settings

class Map(Sprite):

	def __init__(self, size, part, character):
		super().__init__()
		self.part = part
		self.size = size;
		self.character = character;
		self.envObjects = pygame.sprite.Group()
		self.envObjects.empty()
		self.interpreter = SpriteInterpreter()
		self.loadPart(part)
		self.prepareBG('../img/bg_brick3.png')
		self.prepareEnvObj()

	def prepareBG(self, textureDir):
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

	def prepareEnvObj(self):
		for y in range(len(self.levelRows)):
			for x in range(len(self.levelRows[y])):
				ob = self.interpreter.interpret(self.levelRows[y][x], (x, y))
				if ob is not None:
					print('Obj added ' + ob.wallType.value)
					self.envObjects.add(ob)


	def loadPart(self, part):
		print(part)
		file = open('../level/' + str(part[0]) + '_' + str(part[1]) + '.txt', 'r')
		data = file.read()
		self.levelRows = data.split('\n')
		print(type(self.levelRows))
		print(self.levelRows)

	def refreshMap(self):
		self.loadPart(self.part)
		self.envObjects.empty()
		self.prepareEnvObj()


	def checkMapChange(self, globalEnvSprites):
		settings = Settings()
		chPos = (self.character.rect.x, self.character.rect.y)
		#print(chPos)
		if chPos[0] < 0:
			tmpPart = (self.part[0]-1, self.part[1], chPos[1])
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
			self.refreshMap()
			globalEnvSprites.empty()
			globalEnvSprites.add(self)
			globalEnvSprites.add(self.envObjects)
		#	return self.envObjects
		#return globalEnvSprites