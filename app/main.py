from fastapi import FastAPI, HTTPException
from app.minesweeper.minesweeper import Minesweeper
from app.model import GameState, CellState, CellRequest
from app.minesweeper.cell import EmptyCell

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


minesweeper = None

@app.get("/")
def root():
    return {"message": "Hello, Minesweeper!"}

@app.post("/minesweeper/init")
def init_game():
    global minesweeper
    minesweeper = Minesweeper()
    return 

@app.get("/minesweeper/state", response_model=GameState)
def get_state():
    if minesweeper is None:
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    board = []
    for row in minesweeper.board:
        row_list = []
        for cell in row:
            neighbour_mines = None
            is_mine = True
            if isinstance(cell, EmptyCell):
                neighbour_mines = cell.neighbor_mines
                is_mine = False

            cell_state = CellState(
                is_revealed=cell.is_revealed,
                has_flag=cell.has_flag,
                neighbor_mines=neighbour_mines,
                is_mine=is_mine
            )
            row_list.append(cell_state)
        board.append(row_list)

    return GameState(
        game_over=minesweeper.game_over,
        game_win=minesweeper.game_won,
        board=board,
        remaining=minesweeper.remaining
    )

@app.post("/minesweeper/reveal")
def reveal_cell(request: CellRequest):
    if minesweeper is None:
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    minesweeper.reveal_cell(request.row, request.col)

@app.post("/minesweeper/flag")
def flag_cell(request: CellRequest):
    if minesweeper is None:
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    minesweeper.flag_cell(request.row, request.col)


