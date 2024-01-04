from random import choice
from tic_tac_toe.TicTacToeGame import TicTacToeGame
from tic_tac_toe.TicTacToeAction import TicTacToeAction
from solvers.Minimax import Minimax
from solvers.MCTS import MCTS
import random

game = TicTacToeGame()
done = False
minimax = Minimax()
mcts = MCTS()
game.player = 1

game = TicTacToeGame()
while(not game.done):
        pos_i, pos_j = input("Enter two numbers here: ").split()
        pos_i, pos_j = [int(pos_i), int(pos_j)]
        player_action = TicTacToeAction(pos_i, pos_j)
        board, done, reward = game.step(player_action)
        game.render()
        if done:
            break
        comp_action = mcts.monte_carlo_tree_search(game)
        board, done, reward = game.step(comp_action)
        game.render()

print("Reward:", reward)
