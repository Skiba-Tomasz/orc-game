from astar import *

class GameAI:

	def move(self, character, enemy, obstacles):
		a = Astar(1000)
		self.parseObstacles(obstacles, a)
		cNode = Node((round(character.rect.x/48), round(character.rect.y/48)))
		eNode = Node((round(enemy.rect.x/48), round(enemy.rect.y/48)))
		#self.hardLog(character, enemy, cNode, eNode)
		result = a.process(eNode, cNode)
		#a.consolePrintMap(result)
		path = []
		a.revertTrack(result, path)
		#self.printPath(path)
		enemy.setPath(path[:])


	def printPath(self, paths):
		for s in paths:
			print('Node(' + str(s.x) + 'x' + str(s.y) + ') f=' + str(s.f) + ' g=' + str(s.g) + ' h=' + str(s.h))

	def parseObstacles(self, obstacles, algo):
		for o in obstacles:
			n = Node((round(o.rect.x/48), round(o.rect.y/48)))
			algo.blockedNodes.append(n)
			#print('Add obstacle (' + str(n.x) + 'x' + str(n.y) + ')')

	def hardLog(self, character, enemy, cNode, eNode):
		print('Start pathfinding')
		print('cPos(' + str(character.rect.x) + 'x' + str(character.rect.y) + ')')
		print('ePos(' + str(enemy.rect.x) + 'x' + str(enemy.rect.y) + ')')
		print('cNode(' + str(cNode.x) + 'x' + str(cNode.y) + ') f=' + str(cNode.f) + ' g=' + str(cNode.g) + ' h=' + str(cNode.h))
		print('eNode(' + str(eNode.x) + 'x' + str(eNode.y) + ') f=' + str(eNode.f) + ' g=' + str(eNode.g) + ' h=' + str(eNode.h))
