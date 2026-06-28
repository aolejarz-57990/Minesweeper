import pygame
from settings import CELL_SIZE, MAP_WIDTH, MAP_HEIGHT, ROWS, COLS, WHITE, BLACK, GRAY


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        self.running = True
        self.revealed = self.create_revealed_map()

    def draw_map(self):
        #rysuje pola
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                if self.revealed[row][col]:
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

        self.revealed[row][col] = True
        print(row, col)

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

    #buduje plansze z wartosciami False
    def create_revealed_map(self):
        revealed = []

        #tworze plansze dla zmiennej revealed, jaki jest stan pola w pamieci gry
        for row in range(ROWS):
            row_list = []

            for col in range(COLS):
                row_list.append(False)

            revealed.append(row_list)

        return revealed