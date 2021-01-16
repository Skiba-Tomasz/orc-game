import pygame

from pygame.sprite import Sprite
from pygame.surface import Surface
from wall import *
class SpriteInterpreter:

	#def __init__(self):
	def interpret(self, character, position):
		#position = (Main.SETTINGS.tileSize*position[0], Main.SETTINGS.tileSize*position[1])
		position = (48*position[0], 48*position[1])
		if character == '1':
			return Wall(position, (48, 48), WallType.BRICK, True)
		elif character == '2':
			return Wall(position, (48, 48), WallType.GROUND, True)
		return None