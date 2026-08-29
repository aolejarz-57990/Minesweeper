from app.settings import MINES_COUNT
from app.minesweeper.cell import EmptyCell, MineCell
from random import randint

class Minesweeper:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.init_game()


    def init_game(self):
        self.game_over = False
        self.game_won = False
        self.board = self._create_board()
        self._place_mines()
        self._count_neighbor_mines()
        self.remaining = self.rows * self.cols - MINES_COUNT

    def _create_board(self):
        board = []

        for row in range(self.rows):
            row_list = []

            for col in range(self.cols):
                row_list.append(EmptyCell())

            board.append(row_list)

        return board
    
    def _place_mines(self):
        mines_placed = 0
        
        while mines_placed < MINES_COUNT:
            row = randint(0, self.rows - 1)
            col = randint(0, self.cols - 1)

            if not isinstance(self.board[row][col], MineCell):
                self.board[row][col] = MineCell()
                mines_placed += 1


    def _assign_neighboring_mines_count(self, row, col):
        mines_count = 0

        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if (
                    0 <= neighbor_row < self.rows
                    and 0 <= neighbor_col < self.cols
                    and isinstance(self.board[neighbor_row][neighbor_col], MineCell)
                ):
                    mines_count += 1

        self.board[row][col].neighbor_mines = mines_count

    def _count_neighbor_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.board[row][col], EmptyCell):
                    self._assign_neighboring_mines_count(row, col)

    def reveal_cell(self, row, col):
        cell = self.board[row][col]

        if not cell.has_flag and not cell.is_revealed:
            if isinstance(cell, MineCell):
                self.game_over = True
                self.reveal_all_mines()
            else:
                self._reveal_empty_cells(row, col)

    def flag_cell(self, row, col):
        cell = self.board[row][col]
        if not cell.is_revealed:
            cell.has_flag = not cell.has_flag
    
    def _reveal_empty_cells(self, row, col):
        cell = self.board[row][col]

        if cell.is_revealed or cell.has_flag:
            return
        
        cell.is_revealed = True
        self.remaining -= 1
        
        if self.remaining == 0:
            self.game_over = True
            self.game_won = True

        if cell.neighbor_mines > 0:
            return
        
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    self._reveal_empty_cells(neighbor_row, neighbor_col)

    def reveal_all_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.board[row][col], MineCell):
                    self.board[row][col].is_revealed = True