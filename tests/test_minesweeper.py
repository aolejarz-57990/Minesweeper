from app.minesweeper.minesweeper import Minesweeper
from unittest.mock import patch
from app.minesweeper.cell import EmptyCell, MineCell
import pytest

#do przygotowania powstarzających się elementów w testach
@pytest.fixture 
def minesweeper_basic():
    minesweeper = Minesweeper()
    return minesweeper

#czy funkcja zlicza dobrze ilość sąsiadujących min
@patch('minesweeper.ROWS', 3)
@patch('minesweeper.COLS', 3)
def test_assign_neighboring_mines_count_in_center(minesweeper_basic):
    minesweeper_basic.board = minesweeper_basic._create_board()

    minesweeper_basic.board[1][1] = MineCell()
    minesweeper_basic._assign_neighboring_mines_count(0,0)

    assert minesweeper_basic.board[0][0].neighbor_mines == 1


@patch('minesweeper.ROWS', 3)
@patch('minesweeper.COLS', 3)
def test_assign_neighboring_mines_in_corner(minesweeper_basic):

    minesweeper_basic.board = minesweeper_basic._create_board()

    minesweeper_basic.board[2][2] = MineCell()

    #podaje konkretną komórkę, dla której to sprawdzam
    minesweeper_basic._assign_neighboring_mines_count(1, 1)

    assert minesweeper_basic.board[1][1].neighbor_mines == 1



@patch('minesweeper.ROWS', 4)
@patch('minesweeper.COLS', 4)
def test_reveal_empty_cells_chain_reaction(minesweeper_basic):

    minesweeper_basic.board = minesweeper_basic._create_board()

    #umieszczam minę
    minesweeper_basic.board[1][2] = MineCell()
    minesweeper_basic.board[3][0] = MineCell()
    
    # Najpierw muszę wyliczyć miny sąsiadujące, żeby pola wiedziały, czy są bezpieczne i jakie mają cyfry
    minesweeper_basic._count_neighbor_mines()

    #Odkrywam lewy górny róg (0, 0), który jest całkowicie bezpieczny i oddalony od miny bo licze do 2 od miny. 
    minesweeper_basic.reveal_cell(0, 0)

    # Pole (0, 0) powinno być odkryte
    assert minesweeper_basic.board[0][0].is_revealed is True
    
    assert minesweeper_basic.board[1][0].is_revealed is True
    assert minesweeper_basic.board[0][1].is_revealed is True
    assert minesweeper_basic.board[2][0].is_revealed is True
    #zakryte bo jest mina
    assert minesweeper_basic.board[3][0].is_revealed is False
    assert minesweeper_basic.board[3][3].is_revealed is False
    assert minesweeper_basic.board[3][2].is_revealed is False
    assert minesweeper_basic.board[2][2].is_revealed is False


@patch('minesweeper.ROWS', 3)
@patch('minesweeper.COLS', 3)
def test_click_on_mine_loses_game(minesweeper_basic):
    minesweeper_basic.board = minesweeper_basic._create_board()
    
    minesweeper_basic.board[1][1] = MineCell()

    minesweeper_basic.reveal_cell(1, 1)

    assert minesweeper_basic.game_over is True