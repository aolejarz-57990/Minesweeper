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
        self.place_mines()
        self.count_neighbor_mines()

    def draw_map(self):
        #rysuje pola
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                self.board[row][col].draw(self.screen, x, y)
        

    def handle_mouse_click(self, button):
        if self.game_over:
            return
        
        #funckja pygame, która sprawdza aktualną pozycję myszki, zwraca x,y
        x, y = pygame.mouse.get_pos()

        #ile pikseli od lewej górnej strony okna, // dzielenie calkowite 
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        # Dla wygody tworzyę zmienną "clicked_cell", która odnosi się do klikniętego pola
        clicked_cell = self.board[row][col]

        if button == 3:
                if not clicked_cell.is_revealed:
                    #Jeśli była False, staje się True. Jeśli była True, staje się False.
                    clicked_cell.has_flag = not clicked_cell.has_flag

        elif button == 1:
            # Blokuje możliwość odkrycia pola, jeśli jest na nim flaga
            if not clicked_cell.has_flag and not clicked_cell.is_revealed:
                if clicked_cell.has_mine:
                    self.game_over = True
                    self.reveal_all_mines()
                    pygame.display.set_caption("PRZEGRANA :( Wciśnij 'R', aby zresetować.")
                else:
                    self.reveal_empty_cells(row, col)
                    self.check_win()

    def reveal_all_mines(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].has_mine:
                    self.board[row][col].is_revealed = True

    def run(self):
        #zeby sprawdzic liczbe kafelkow
        self.check_win()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                #To jest specjalna stała/event type w Pygame, która oznacza, 
                # ze użytkownik nacisnął przycisk myszy
                #który przycisk myszy (1 - lewy, 2 czy 3- prawy) został kliknięty
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.button)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

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
    
    def place_mines(self):
        mines_placed = 0

        #wybieranie losowego pola, kiedy liczba min jest mniejsza od 40
        while mines_placed < MINES_COUNT:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)

            #jeśli pole jest puste, dodaje mine i zapisuje ilość min w liście
            if not self.board[row][col].has_mine:
                self.board[row][col].has_mine = True
                mines_placed += 1


    def _assign_neighboring_mines_count(self, row, col):
        mines_count = 0

        #offsett- przesuniecie
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if (
                    0 <= neighbor_row < ROWS
                    and 0 <= neighbor_col < COLS
                    and self.board[neighbor_row][neighbor_col].has_mine
                ):
                    mines_count += 1

        self.board[row][col].neighbor_mines = mines_count


    def count_neighbor_mines(self):
        for row in range(ROWS):
            for col in range(COLS):
                if not self.board[row][col].has_mine:
                    self._assign_neighboring_mines_count(row, col)

    
    def reveal_empty_cells(self, row, col):
        clicked_cell = self.board[row][col]

        #jeśli pole jest odkryte lub ma flage - przerwanie 
        if clicked_cell.is_revealed or clicked_cell.has_flag:
            return
        
        clicked_cell.is_revealed = True

        #jeśli komórka sąsiaduje z miną(ma cyferke), fala ma się zatrzymać
        if clicked_cell.neighbor_mines > 0:
            return
        
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS:
                    self.reveal_empty_cells(neighbor_row, neighbor_col)


    def check_win(self):
        revealed_count = 0
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].is_revealed and not self.board[row][col].has_mine:
                    revealed_count += 1
                    
        safe_cells = (ROWS * COLS) - MINES_COUNT
        remaining = safe_cells - revealed_count # Obliczamy ile zostało
        
        if remaining == 0:
            self.game_over = True
            pygame.display.set_caption("WYGRANA! Wciśnij 'R', aby zagrać ponownie.")
        else:
            pygame.display.set_caption(f"Minesweeper | Pozostało do odkrycia: {remaining}")


    def reset_game(self):
        self.game_over = False
        self.board = self.create_board()
        self.place_mines()
        self.count_neighbor_mines()
        self.check_win()