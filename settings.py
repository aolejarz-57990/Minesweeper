ROWS = 20
COLS = 20

CELL_SIZE = 40

MAP_WIDTH = COLS * CELL_SIZE
MAP_HEIGHT = ROWS * CELL_SIZE

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
DARK_RED = (139, 0, 0)
PURPLE = (128, 0, 128)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Nasz słownik łączący wyliczone miny z odpowiednią farbą
NUMBER_COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: DARK_RED,
    5: PURPLE,
    6: BLACK,
    7: BLACK,
    8: BLACK
}

MINES_COUNT = 40
