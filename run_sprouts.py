from sprouts.SproutsGame import SproutsGame
from random import choice
import random
from solvers.Minimax import Minimax

random.seed(1)

game = SproutsGame(3)
done = game.done
game.render()
r = game.get_state_value()
while not done:
    minimax = Minimax()
    action = minimax.minimax(game)[1]
    s, done, r = game.step(action)
    game.render()

if r == 1:
    print("Player 1 won!")
elif r == -1:
    print("Player 2 won!")