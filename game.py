import pygame
from settings import MINES_COUNT, CELL_SIZE, MAP_WIDTH, MAP_HEIGHT, ROWS, COLS, WHITE, BLACK, GRAY
from cell import Cell
import random


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        self.running = True
        self.game_over = False
        self.board = self.create_board()
        self.pleace_mines()

    def draw_map(self):
        #rysuje pola
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                if self.board[row][col].is_revealed:
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (x, y, CELL_SIZE, CELL_SIZE)
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        GRAY,
                        (x, y, CELL_SIZE, CELL_SIZE)
                    )

                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (x, y, CELL_SIZE, CELL_SIZE),
                    1
                )

    def handle_mouse_click(self):
        #funckja pygame, która sprawdza aktualną pozycję myszki, zwraca x,y
        x, y = pygame.mouse.get_pos()

        #ile pikseli od lewej górnej strony okna, // dzielenie calkowite 
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        self.board[row][col].is_revealed = True

        print(row, col)
        print(self.board[row][col].has_mine)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                #To jest specjalna stała/event type w Pygame, która oznacza, 
                # ze użytkownik nacisnął przycisk myszy
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()

            self.screen.fill(WHITE)
            self.draw_map()
            pygame.display.update()

        pygame.quit()

    #buduje plansze z obiektami Cell, o wlasciowsciach egz. 
    def create_board(self):
        board = []

        #tworze plansze dla zmiennej board, gdzie w kazdej komorce znajduje sie Cell
        #np. self.board[row][col].has_mine = True, self.board[row][col].has_flag = True, osv. 

        for row in range(ROWS):
            row_list = []

            for col in range(COLS):
                row_list.append(Cell())

            board.append(row_list)

        return board
    
    def pleace_mines(self):
        mines_pleaced = 0

        #wybieranie losowego pola, kiedy liczba min jest mniejsza od 40
        while mines_pleaced < MINES_COUNT:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)

        #jeśli pole jest puste, dodaje mine i zapisuje ilość min w liście
        if not self.board[row][col].has_mine:
            self.board[row][col].has_mine = True
            mines_pleaced += 1
        
    
