import pygame
from app.desktop.graphical_interface import GraphicalInterface
from app.minesweeper.cell import MineCell
from app.settings import CELL_SIZE, MAP_WIDTH, MAP_HEIGHT, ROWS, COLS, WHITE, BLACK, GRAY, NUMBER_COLORS, RED
from app.minesweeper.minesweeper import Minesweeper

pygame.font.init()
FONT = pygame.font.SysFont('arial', 24, bold=True)

class PygameUI(GraphicalInterface):
    def __init__(self):
        pygame.init()

        super().__init__()

        self.screen = pygame.display.set_mode(
            (MAP_WIDTH, MAP_HEIGHT)
        )

        pygame.display.set_caption("Minesweeper")

        self.minesweeper = Minesweeper()

    def get_events(self):
        clicked_buttons = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_buttons.append(event.button)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.minesweeper.init_game()

        return clicked_buttons

    def handle_mouse_click(self, button):
        if self.minesweeper.game_over:
            return
        
        x, y = pygame.mouse.get_pos()
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if button == 3:
            self.minesweeper.flag_cell(row, col)
        elif button == 1:
            self.minesweeper.reveal_cell(row, col)

    def draw_map(self):
        self.screen.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                self.draw_cell(self.screen, x, y, self.minesweeper.board[row][col])

    def draw_cell(self, screen, x, y, cell):
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2

        if cell.is_revealed:
            self._draw_revealed_background(x, y)

            if isinstance(cell, MineCell):
                self._draw_mine(center_x, center_y)
                
            elif cell.neighbor_mines > 0:
                self._draw_number(center_x, center_y, cell.neighbor_mines)
        else:
            self._draw_hidden_background(x, y)

            if cell.has_flag:
                self._draw_flag(center_x, center_y)

    def update_display(self):
            
        if self.minesweeper.game_over:
            if self.minesweeper.game_won:
                pygame.display.set_caption("WYGRANA! Wciśnij 'R', aby zagrać ponownie.")
            else:
                pygame.display.set_caption("PRZEGRANA :( Wciśnij 'R', aby zresetować.")
        else:
            pygame.display.set_caption(f"Minesweeper | Pozostało do odkrycia: {self.minesweeper.remaining}")

        pygame.display.update()

    def close(self):
        pygame.quit()


    def _draw_revealed_background(self, x, y):
        pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def _draw_hidden_background(self, x, y):
        pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def _draw_mine(self, center_x, center_y):
        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), CELL_SIZE // 4)

    def _draw_flag(self, center_x, center_y):
        pygame.draw.circle(self.screen, RED, (center_x, center_y), CELL_SIZE // 6)

    def _draw_number(self, center_x, center_y, number):
        text_color = NUMBER_COLORS.get(number, BLACK)
        text_surface = FONT.render(str(number), True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)