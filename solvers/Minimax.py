from Game import Game
from copy import deepcopy
class Minimax:
    def __init__(self) -> None:
        pass

    # def minimax(self, game: Game, prev_action) -> tuple[float, any]:
    #     if game.done: 
    #         return game.get_state_value(), prev_action
    #     actions = game.get_valid_actions()
    #     best_action = None
    #     if game.player == 1:
    #         value = float("-inf")
    #         for action in actions:
    #             game2 = deepcopy(game)
    #             game2.step(action)
    #             curr_value = self.minimax(game2, action)[0]
    #             if value < curr_value:
    #                 best_action = action
    #             value = max(value, curr_value)
    #     else:
    #         value = float("inf")
    #         for action in actions:
    #             game2 = deepcopy(game)
    #             game2.step(action)
    #             curr_value = self.minimax(game2, action)[0]
    #             if value > curr_value:
    #                 best_action = action
    #             value = min(value, curr_value)
    #     return value, best_action

    def minimax(self, game: Game, prev_action, alpha, beta) -> tuple[float, any]:
        if game.done: 
            return game.get_state_value(), prev_action
        actions = game.get_valid_actions()
        best_action = None
        if game.player == 1:
            value = float("-inf")
            for action in actions:
                game2 = deepcopy(game)
                game2.step(action)
                curr_value = self.minimax(game2, action, alpha, beta)[0]
                if value < curr_value:
                    best_action = action
                value = max(value, curr_value)
                if value >= beta:
                    break
                alpha = max(alpha, value)
        else:
            value = float("inf")
            for action in actions:
                game2 = deepcopy(game)
                game2.step(action)
                curr_value = self.minimax(game2, action, alpha, beta)[0]
                if value > curr_value:
                    best_action = action
                value = min(value, curr_value)
                if value <= alpha:
                    break
                beta = min(beta, value)
        return value, best_action
    
    

        