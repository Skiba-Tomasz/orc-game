from character import Character
from enum import Enum
from settings import Settings
from projectile import ProjectileType

class CharacterType(Enum):
	EDD = 'EDD'
	ALICE = 'ALICE'
	CYBER = 'CYBER'

class CharacterFactory:

	def __init__(self, characterType):
		self.character = None
		startingPos = (10,4)
		if characterType == CharacterType.EDD:
			self.character = Character(position = startingPos, hp = 5, speed = 15, projectileType = ProjectileType.FROST, damage = 5, spriteID = 1)
		elif characterType == CharacterType.ALICE:
			self.character = Character(position = startingPos, hp = 20, speed = 10, projectileType = ProjectileType.FROST, damage = 1, spriteID = 0)
		elif characterType == CharacterType.CYBER:
			self.character = Character(position = startingPos, hp = 2, speed = 25, projectileType = ProjectileType.FIRE, damage = 7, spriteID = 3)
