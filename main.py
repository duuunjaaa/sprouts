from random import choice
from tic_tac_toe.TicTacToeGame import TicTacToeGame

game = TicTacToeGame()
done = False
while not done:
    actions = game.get_valid_actions()
    action = choice(actions)
    board, done, reward = game.step(action)
    game.render()
    print("Reward:", reward)