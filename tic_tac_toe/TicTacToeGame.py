import numpy as np
from Game import Game
from tic_tac_toe.TicTacToeAction import TicTacToeAction

class TicTacToeGame(Game):
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        self.done = False
    
    def get_valid_actions(self) -> list[TicTacToeAction]:
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    actions.append(TicTacToeAction(i, j))
        return actions

    def __is_done(self) -> bool:
        return self.__get_state_value() != 0 or len(self.get_valid_actions()) == 0

    def __get_state_value(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        return 0
    
    def step(self, action: TicTacToeAction) -> tuple[any, bool, float]:
        self.board[action.row][action.col] = self.player
        self.player = -self.player
        self.done = self.__is_done()
        reward = self.__get_state_value()
        return self.board, self.done, reward
    
    def render(self):
        # Print board nicely
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    print(" ", end="")
                elif self.board[i][j] == 1:
                    print("X", end="")
                else:
                    print("O", end="")
                if j != 2:
                    print("|", end="")
            print()
            if i != 2:
                print("-----")
        print()