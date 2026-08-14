import pygame
from settings import CELL_SIZE, MAP_WIDTH, MAP_HEIGHT, ROWS, COLS, WHITE, BLACK, GRAY, NUMBER_COLORS, RED
from minesweeper import Minesweeper

pygame.font.init()
FONT = pygame.font.SysFont('arial', 24, bold=True)

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        self.running = True

        self.minesweeper = Minesweeper()

    def draw_map(self):
        #rysuje pola
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                self.draw_cell(self.screen, x, y, self.minesweeper.board[row][col])

    def draw_cell(self, screen, x, y, cell):
        # Obliczamy środek kratki (przyda się do równego rysowania kółek i tekstu)
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2

        if cell.is_revealed:
            pygame.draw.rect(
                screen,
                WHITE,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            #1 to grubość ramki
            pygame.draw.rect(
                screen,
                GRAY, 
                (x, y, CELL_SIZE, CELL_SIZE), 1
            )

            if cell.has_mine:
                pygame.draw.circle(
                screen,
                BLACK, 
                #promień koła
                (center_x, center_y), CELL_SIZE // 4
                )
                

            elif cell.neighbor_mines > 0:
                #black jest zabezpieczeniem przy get
                text_color = NUMBER_COLORS.get(cell.neighbor_mines, BLACK)
                
                #funckja render przyjmuje tylko i wyłącznie str, wygladzenie krawędzi, kolor
                text_surface = FONT.render(str(cell.neighbor_mines), True, text_color)
                
                #gdzie bedzie teskt, bierze srodek ramki i umieszcza ja w cx i xy
                text_rect = text_surface.get_rect(center=(center_x, center_y))
                
                #nakładanie grafiki na "płótno"(co , na co)
                screen.blit(text_surface, text_rect)
        else:
            # szare tło dla zakrytego pola
            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, CELL_SIZE, CELL_SIZE)
                )
            
            #  czarną ramkę
            pygame.draw.rect(
                screen,
                BLACK,
                (x, y, CELL_SIZE, CELL_SIZE), 1
                )

            if cell.has_flag:
                # Jeśli gracz postawił flagę, rysujemy małe czerwone kółko 
                pygame.draw.circle(
                    screen,
                    RED,
                    (center_x, center_y), CELL_SIZE // 6
                    )
    
    def handle_mouse_click(self, button):
        if self.minesweeper.game_over:
            return
        
        #funckja pygame, która sprawdza aktualną pozycję myszki, zwraca x,y
        x, y = pygame.mouse.get_pos()

        #ile pikseli od lewej górnej strony okna, // dzielenie calkowite 
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if button == 3:
            self.minesweeper.flag_cell(row, col)

        elif button == 1:
            self.minesweeper.reveal_cell(row, col)


    def run(self):

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
                        self.minesweeper.init_game()

            if self.minesweeper.game_over:
                if self.minesweeper.game_won:
                    pygame.display.set_caption("WYGRANA! Wciśnij 'R', aby zagrać ponownie.")
                else:
                    pygame.display.set_caption("PRZEGRANA :( Wciśnij 'R', aby zresetować.")
            else:
                pygame.display.set_caption(f"Minesweeper | Pozostało do odkrycia: {self.minesweeper.remaining}")


            self.screen.fill(WHITE)
            self.draw_map()
            pygame.display.update()

        pygame.quit()