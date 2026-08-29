import uuid
from fastapi import FastAPI, HTTPException
from app.minesweeper.minesweeper import Minesweeper
from app.model import GameState, CellState, CellRequest, GameInitRequest, GameRequest
from app.minesweeper.cell import EmptyCell
from app.services.game import GameService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_service = GameService()

def get_game_state(minesweeper: Minesweeper) -> GameState:
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

@app.get("/")
def root():
    return {"message": "Hello, Minesweeper!"}

@app.post("/minesweeper/init")
def init_game(request: GameInitRequest):
    session_id = game_service.create_session(request.name, request.rows, request.cols)
    return {"session_id": session_id}

@app.get("/minesweeper/state/{session_id}", response_model=GameState)
def get_state(session_id: str):
    if not game_service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    game_session = game_service.get_session(session_id)
    return get_game_state(game_session.minesweeper)

@app.post("/minesweeper/reveal/{session_id}")
def reveal_cell(request: CellRequest, session_id: str):
    if not game_service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    game_session = game_service.get_session(session_id)
    game_session.minesweeper.reveal_cell(request.row, request.col)

@app.post("/minesweeper/flag/{session_id}")
def flag_cell(request: CellRequest, session_id):
    if not game_service.session_exists(session_id):
        raise HTTPException(status_code=404, detail="The game has not been initialized.")
    game_session = game_service.get_session(session_id)
    game_session.minesweeper.flag_cell(request.row, request.col)


