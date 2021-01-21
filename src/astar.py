# Implementation of A* based on source
# https://www.geeksforgeeks.org/a-search-algorithm/
# Author Tomasz Skiba

from time import sleep

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

	def __init__(self, maxIterations):
		self.blockedNodes = []
		self.mapMaxX = 20
		self.mapMaxY = 10
		self.depth = 0
		self.maxIterations = maxIterations
		self.levelRows = []

	# Find path from startNode to endNode
	# Node at endNode location will be returned, path can be recreated by recursive endNode.parent lookup
	def process(self, startNode, endNode):
		openList = []
		closedList = []
		openList.append(startNode)
		iters = 0
		while len(openList) > 0 and iters < self.maxIterations:
			openList.sort(reverse=False, key=self.__getF)
			q = openList[0]
			for o in openList:
				iters+=1
				#print(str(q.x) + "x" + str(q.y))
				o.f = self.__calculateTravelCost(o, endNode)
				#print("cost " + str(o.f))
				if o.f <= q.f:
					q = o
					#print('len' + str(len(openList)))
					openList.remove(q)
					#print('len a' + str(len(openList)))
					successors = self.__generateChildren(q)
					#print('Parent(' + str(q.x) + 'x' + str(q.y) + ') f=' + str(q.f) + ' g=' + str(q.g) + ' h=' + str(q.h))
					for s in successors:
						if s.x == endNode.x and s.y == endNode.y:
							return s
						s.g = q.g + self.__distance(s, q)
						s.h = self.__distance(s, endNode)
						s.f = s.g + s.h
						#print('Successor(' + str(s.x) + 'x' + str(s.y) + ') f=' + str(s.f) + ' g=' + str(s.g) + ' h=' + str(s.h))
					successors.sort(reverse=True, key=self.__getF)
					for s in successors:
						if not self.__isLowerCostNodeInList(openList, s):
							if not self.__isLowerCostNodeInList(closedList, s):
								#print('Successor inserted(' + str(s.x) + 'x' + str(s.y) + ') f=' + str(s.f) + ' g=' + str(s.g) + ' h=' + str(s.h))
								openList.insert(0, s)
			closedList.append(q)

	def printTrack(self, node):
		if node is not None:
			print(str(node.x) + "x" + str(node.y))
			self.printTrack(node.parent)

	def revertTrack(self, node, track):
		if node is not None:
			self.revertTrack(node.parent, track)
			track.append(node)

	def consolePrintMap(self, node):
		self.__resetPrintedMap()
		self.__printMap(node)

	def __getF(self, node):
		return node.f

	def __calculateTravelCost(self, startNode, endNode):
		return startNode.totalCost + self.__distance(startNode, endNode)

	def __distance(self, n1, n2, type = 'Manhatan'):
		if type == 'Euclidean':
			return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)
		elif type == 'Manhatan':
			return abs(n1.x - n2.x) + abs(n1.y - n2.y)		

	def __generateChildren(self, node):
		chilren = []
		if(node.x-1 > 0):
			nodeW = Node((node.x-1, node.y), node.totalCost, node.f, node)
			if not self.__isNodeBlocked(nodeW):
				chilren.append(nodeW)
		if(node.x+1 < self.mapMaxX):
			nodeE = Node((node.x+1, node.y), node.totalCost, node.f, node)
			if not self.__isNodeBlocked(nodeE):
				chilren.append(nodeE)
		if(node.y-1 > 0):
			nodeN = Node((node.x, node.y-1), node.totalCost, node.f, node)
			if not self.__isNodeBlocked(nodeN):
				chilren.append(nodeN)
		if(node.y+1 < self.mapMaxY):
			nodeS = Node((node.x, node.y+1), node.totalCost, node.f, node)
			if not self.__isNodeBlocked(nodeS):
				chilren.append(nodeS)
		return chilren

	def __isNodeBlocked(self, node):
		for bNode in self.blockedNodes:
			if node.x == bNode.x and node.y == bNode.y:
				return True
		return False

	def __isLowerCostNodeInList(self, openList, node):
		for n in openList:
			if n.x == node.x and n.y == node.y:
				if n.f < node.f:
					return True
		return False

	def __loadTask(self):
		file = open('astarTask.txt', 'r')
		data = file.read()
		self.levelRows = data.split('\n')
		print(type(self.levelRows))
		print(self.levelRows)

	def __getTaskStart(self):
		for y in range(len(self.levelRows)):
			for x in range(len(self.levelRows[y])):	
				if self.levelRows[y][x] == 'S':
					print('Start foud')
					self.taskStartNode = Node((x,y))
				elif self.levelRows[y][x] == 'E':
					print('End foud')
					self.taskEndNode = Node((x,y))
				elif not self.levelRows[y][x] == ' ':
					bn = Node((x,y))
					self.blockedNodes.append(bn)
					print('Blocking: ' + str(bn.x) + 'x' + str(bn.y))

	def __printMap(self, node):
		self.depth += 1
		if node is not None:
			for y in range(len(self.levelRows)):
				row = '';
				for x in range(len(self.levelRows[y])):	
					if x == node.x and y == node.y:
						row += "X"
					else:
						row += self.levelRows[y][x]
				print(row)
				self.levelRows[y] = row
			sleep(0.02)
			self.__printMap(node.parent)

	def __resetPrintedMap(self):
		self.levelRows = []
		for i in range(10):
			self.levelRows.append(" " * 20)


# Use this to test 
#	def test(self):
#		self.__loadTask()
#		self.__getTaskStart()
#		result = self.process(self.taskStartNode, self.taskEndNode)
#		print('====================')
#		self.__printMap(result)
#		print(self.depth)
#
#if __name__ == '__main__':
#	app = Astar(10000)
#	app.test()