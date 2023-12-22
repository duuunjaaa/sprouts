from Action import Action
class TicTacToeAction(Action):
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __str__(self):
        return f"({self.row}, {self.col})"
    