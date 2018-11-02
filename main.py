import pygame

BG_COLOR = (0, 0, 0)
TEAM1_COLOR = (255, 0, 0)
TEAM2_COLOR = (255, 255, 0)

class Grid(object):
        def __init__(self, n_rows, n_cols, color=(0, 0, 255)):
            self.n_rows = n_rows
            self.n_cols = n_cols
            self.color = color

            self._fichas = []

        def add_ficha(self, ficha):
            if not isinstance(ficha, Ficha): raise TypeError("Ur a dumbass")
            
            self._fichas.append(ficha)

        def draw(self, surface):
            def draw_cell(rect, offset):
                pygame.draw.rect(surface, self.color, rect)
                ellipse_rect = pygame.Rect(rect.x + rect.width * offset, rect.y + rect.height * offset, rect.width * (1 - 2*offset), rect.height * (1 - 2*offset))
                pygame.draw.ellipse(surface, BG_COLOR, ellipse_rect)

            #calculate shit
            offset_percent = 0.05
            surface_w, surface_h = surface.get_size()
            grid_rect = pygame.Rect(surface_w * offset_percent, surface_h * offset_percent, surface_w * (1 - 2*offset_percent),  surface_h * (1 - 2*offset_percent))
            cell_w, cell_h = int(grid_rect.width / self.n_cols), int(grid_rect.height / self.n_rows)

            #draw shit
            for x in range(grid_rect.left, grid_rect.right - cell_w, cell_w):
                for y in range(grid_rect.top, grid_rect.bottom - cell_h, cell_h):
                    draw_cell(pygame.Rect(x, y, cell_w, cell_h), 0.05)

        def map_coords(self, x, y):
            pass


class Ficha(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


main_surface = pygame.display.set_mode((800, 800))
g = Grid(500, 500)
g.draw(main_surface)
pygame.display.update()
while True: pass
