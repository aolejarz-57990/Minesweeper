import pygame
from settings import WHITE, CELL_SIZE, GRAY, BLACK, NUMBER_COLORS, RED
# Inicjujemy moduł czcionek z Pygame, żeby móc rysować tekst
pygame.font.init()
FONT = pygame.font.SysFont('arial', 24, bold=True)

class Cell:
    def __init__(self):
        self.is_revealed = False
        self.has_mine = False
        self.has_flag = False
        self.neighbor_mines = 0

    def draw(self, screen, x, y):
        # Obliczamy środek kratki (przyda się do równego rysowania kółek i tekstu)
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2

        if self.is_revealed:
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

            if self.has_mine:
                pygame.draw.circle(
                screen,
                BLACK, 
                #promień koła
                (center_x, center_y), CELL_SIZE // 4
                )
                

            elif self.neighbor_mines > 0:
                #black jest zabezpieczeniem przy get
                text_color = NUMBER_COLORS.get(self.neighbor_mines, BLACK)
                
                #funckja render przyjmuje tylko i wyłącznie str, wygladzenie krawędzi, kolor
                text_surface = FONT.render(str(self.neighbor_mines), True, text_color)
                
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

            if self.has_flag:
                # Jeśli gracz postawił flagę, rysujemy małe czerwone kółko 
                pygame.draw.circle(
                    screen,
                    RED,
                    (center_x, center_y), CELL_SIZE // 6
                    )

