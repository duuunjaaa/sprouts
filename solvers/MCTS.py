from Game import Game
from Action import Action
import numpy as np
import math
import random
from copy import deepcopy
from graphviz import Digraph



class Node:
	def __init__(self, game:Game): 
		self.n :int = 0 
		self.w :int = 0
		self.game :Game = deepcopy(game)
		self.terminal :bool = game.done
		children_count = len(game.get_valid_actions())
		self.children :list[Node] = [None for _ in range(children_count)]
		self.reward :int = game.get_state_value()

from graphviz import Digraph
import math

class Node:
    def __init__(self, game):
        self.n = 0
        self.w = 0
        self.game = game
        self.terminal = game.done
        self.children = [None] * len(game.get_valid_actions())
        self.reward = game.get_state_value()
        self.parent = None  # Add parent attribute

import networkx as nx
import matplotlib.pyplot as plt
import math

class Node:
    def __init__(self, game):
        self.n = 0
        self.w = 0
        self.game = game
        self.terminal = game.done
        self.children = [None] * len(game.get_valid_actions())
        self.reward = game.get_state_value()

class MCTS:
	def __init__(self) -> None:
		pass

	def monte_carlo_tree_search(self, gejm:Game) -> Action:
		root = Node(gejm)
		self.expansion(root)
		for i in range(10000):
			l = []
			res = self.selection(root, l)
			if(res.game.done == True):
				self.backprop(l, res.game.get_state_value())  
			else:
				self.expansion(res)
				self.backprop(l,self.play(res))
		
		return self.bestMove(root)


	def uct(self, node, parentNode) -> float:
		if(node.n == 0):
			return(float("inf"))
		return(float(node.w)/node.n) + 20*math.sqrt((np.log(parentNode.n))/node.n)

	def selection(self, node, l) -> Node:
		l.append(node)
		if(not any(node.children) or node.terminal == True):
			return node

		maxChild = None
		maxVal = float("-inf")
		for i in range(len(node.children)):
			if node.children[i] != None:
				uctVal = self.uct(node.children[i],node) 
				if(uctVal > maxVal):
					maxVal = uctVal
					maxChild = node.children[i]
		
		return self.selection(maxChild,l)

	def play(self, node : Node) -> float:
		game2 = deepcopy(node.game)
		while not game2.done:
			game2.step(random.choice(game2.get_valid_actions()))
		
		return game2.get_state_value()

	def expansion(self, node : Node):

		for i,move in enumerate(node.game.get_valid_actions()):
			game2 = deepcopy(node.game)
			game2.step(move)
			node.children[i] = Node(game2)

	def backprop(self, l : list[Node], res):
		pass
		for i in range(len(l)):
			if res > 0:
				if l[i].game.player < 0:
					l[i].w += 1
				else:
					l[i].w -= 1
			else:
				if l[i].game.player > 0:
					l[i].w += 1
				else:
					l[i].w -= 1
			l[i].n += 1
		

		# for i in reversed(range(len(l))):
		# 	if
			# if(res == -1):
			# 	if(j%2 == 0):
			# 		l[i].w += 1
			# if(res == 1):
			# 	if(j%2 == 1):
			# 		l[i].w += 1
			# l[i].n += 1
			# j += 1


	def bestMove(self, node : Node) -> Action:
		max_score = float("-inf")
		maxMove = None
		for i in range(len(node.children)):
			if(node.children[i] != None):
				win_cnt = node.children[i].w
				if(win_cnt > max_score):
					max_score = win_cnt
					maxMove = node.game.get_valid_actions()[i]
		return(maxMove)
			