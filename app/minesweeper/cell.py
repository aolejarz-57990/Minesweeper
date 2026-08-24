from abc import ABC

class Cell(ABC):
    def __init__(self):
        self.is_revealed = False
        self.has_flag = False

class EmptyCell(Cell):
    def __init__(self):
        super().__init__()
        self.neighbor_mines = 0

class MineCell(Cell):
    def __init__(self):
        super().__init__()
        

