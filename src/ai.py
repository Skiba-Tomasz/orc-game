from astar import *

class gameAI:

	def __init__(self):
		self.astar = Astar(10000)

	def move(self, character, enemy):
		a = self.astar
		cNode = Node((character.rect.x/48, character.rect.y/48))
		eNode = Node((enemy.rect.x/48, enemy.rect.y/48))
		if a.distance > 5:
			return
		result = a.process(eNode, cNode)
		path = []
		a.revertTrack(result, path)
		nextStep = path.pop(0)
		print(nextStep)
