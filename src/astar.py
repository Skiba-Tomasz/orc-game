# Implementation of A* based on source
# https://www.geeksforgeeks.org/a-search-algorithm/
# Author Tomasz Skiba

class Node:
	def __init__(self, position, totalCost = 0, f = 0, parent = None):
		self.x = position[0]
		self.y = position[1]
		self.f = f
		self.g = 0
		self.h = 0
		self.totalCost = totalCost
		self.parent = parent

class Astar:

	def __init__(self):
		self.blockedNodes = []
		self.blockedNodes.append(Node((2,0)))
		self.blockedNodes.append(Node((1,1)))
		self.blockedNodes.append(Node((2,2)))

	def process(self, startNode, endNode, maxIterations):
		openList = []
		closedList = []
		openList.append(startNode)
		iters = 0
		while len(openList) > 0 and iters < maxIterations:
			q = openList[0]
			for o in openList:
				iters+=1
				print(str(q.x) + "x" + str(q.y))
				o.f = self.calculateTravelCost(o, endNode)
				print("cost " + str(o.f))
				if o.f <= q.f:
					q = o
					print('len' + str(len(openList)))
					openList.remove(q)
					print('len a' + str(len(openList)))
					successors = self.generateChildren(q)
					for s in successors:
						if s.x == endNode.x and s.y == endNode.y:
							return s
						s.g = q.g + self.distance(s, q)
						s.h = self.distance(s, endNode)
						s.f = s.g + s.h
						if not self.isLowerCostNodeInList(openList, s):
							if not self.isLowerCostNodeInList(closedList, s):
								openList.append(s)
			closedList.append(q)

	def calculateTravelCost(self, startNode, endNode):
		return startNode.totalCost + self.distance(startNode, endNode)

	def distance(self, n1, n2):
		return abs(n1.x - n2.x) + abs(n1.y - n2.y)

	def generateChildren(self, node):
		chilren = []
		nodeW = Node((node.x-1, node.y), node.totalCost, node.f, node)
		if not self.isNodeBlocked(nodeW):
			chilren.append(nodeW)
		nodeE = Node((node.x+1, node.y), node.totalCost, node.f, node)
		if not self.isNodeBlocked(nodeE):
			chilren.append(nodeE)
		nodeN = Node((node.x, node.y-1), node.totalCost, node.f, node)
		if not self.isNodeBlocked(nodeN):
			chilren.append(nodeN)
		nodeS = Node((node.x, node.y+1), node.totalCost, node.f, node)
		if not self.isNodeBlocked(nodeS):
			chilren.append(nodeS)
		return chilren

	def isNodeBlocked(self, node):
		for bNode in self.blockedNodes:
			if node.x == bNode.x and node.y == bNode.y:
				return True
		return False

	def isLowerCostNodeInList(self, openList, node):
		for n in openList:
			if n.x == node.x and n.y == node.y:
				if n.f < node.f:
					return True
		return False

	def printTrack(self, node):
		if node is not None:
			print(str(node.x) + "x" + str(node.y))
			self.printTrack(node.parent)

if __name__ == '__main__':
	app = Astar()
	result = app.process(Node((0,0), 0, 100), Node((2,1)), 200)
	print('====================')
	app.printTrack(result)