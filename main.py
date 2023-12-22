from random import choice
from tic_tac_toe.TicTacToeGame import TicTacToeGame
from tic_tac_toe.TicTacToeAction import TicTacToeAction
from solvers.Minimax import Minimax

game = TicTacToeGame()
done = False
while not done:
    # actions = game.get_valid_actions()
    minimax = Minimax()
    game.player = 1

    while(not game.done):
        # turn = input('Enter X action: ')
        pos_i, pos_j = input("Enter two numbers here: ").split()
        pos_i, pos_j = [int(pos_i), int(pos_j)]
        player_action = TicTacToeAction(pos_i, pos_j)
        board, done, reward = game.step(player_action)
        game.render()
        if done:
            break
        
        comp_action = minimax.minimax(game, player_action)[1]
        board, done, reward = game.step(comp_action)
        game.render()
        # if(game.player == 1):
        #     turn = input('Enter X action: ')
        #     pos = tuple(int(x) for x in turn.split(","))
        #     # pos_i =
        #     # pos_j = 
        #     player_action = TicTacToeAction(pos)
        #     action = player_action
        #     # board, done, reward = game.step(player_action)
        # else:
        #     comp_action = minimax.minimax(game, player_action)[1]
        #     action = comp_action
        #     # board, done, reward = game.step(comp_action)
        # board, done, reward = game.step(action)
        # game.render()
    # action = choice(actions)
    # board, done, reward = game.step(action)

    # game.render()
    print("Reward:", reward)