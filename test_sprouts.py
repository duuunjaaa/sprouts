from sprouts.SproutsGame import SproutsGame
from random import choice
import random
from solvers.Minimax import Minimax

# seed random
random.seed(1)

game = SproutsGame(2)
done = False
game.render()
while not done:
    minimax = Minimax()
    action = minimax.minimax(game, None)[1]
    s, done, r = game.step(action)
    game.render()

if r == 1:
    print("Player 1 won!")
elif r == -1:
    print("Player 2 won!")