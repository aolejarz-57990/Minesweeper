from pydantic import BaseModel
from typing import Optional

class CellState(BaseModel):
    is_revealed: bool
    has_flag: bool
    neighbor_mines: Optional[int]
    is_mine: bool 

class GameState(BaseModel):
    game_over: bool
    game_win: bool 
    board: list[list[CellState]]
    remaining: int

class CellRequest(BaseModel):
    row: int
    col: int

