from sprouts.SproutsGame import SproutsGame
from random import choice
import random
from solvers.Minimax import Minimax
from solvers.MCTS import MCTS


game = SproutsGame(5)
done = game.done
game.render()
r = game.get_state_value()
while not done:
    # minimax = Minimax()
    # action = minimax.minimax(game)[1]
    mcts = MCTS()
    action = mcts.monte_carlo_tree_search(game)

    s, done, r = game.step(action)
    game.render()

if r == 1:
    print("Player 1 won!")
elif r == -1:
    print("Player 2 won!")