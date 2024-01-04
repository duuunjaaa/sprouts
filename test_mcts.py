from tic_tac_toe.TicTacToeGame import TicTacToeGame
from tic_tac_toe.TicTacToeAction import TicTacToeAction
from copy import deepcopy
import random

def simulate(game, cnt = 1000):
    wins_x = 0
    wins_o = 0
    tied = 0
    for _ in range(cnt):
        game_cpy = deepcopy(game)
        while not game_cpy.done:
            game_cpy.step(random.choice(game_cpy.get_valid_actions()))
        state_value = game_cpy.get_state_value()
        if state_value == 1:
            wins_x += 1
        elif state_value == -1:
            wins_o += 1
        else:
            tied += 1
    return wins_x, wins_o, tied
game = TicTacToeGame()
game.step(TicTacToeAction(1,1))
game.step(TicTacToeAction(2,2))
game.step(TicTacToeAction(2,1))

remaining_moves = game.get_valid_actions()
for move in remaining_moves:
    game2 = deepcopy(game)
    game2.step(move)
    wins_x, wins_o, tied = simulate(game2)
    game2.render()
    print(f'Wins X: {wins_x}, Wins O: {wins_o}, Tied: {tied} Score: {wins_o - wins_x}')
    print('------------------')