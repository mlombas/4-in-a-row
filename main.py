import pygame

class Grid(object):
    gravity = pygame.math.Vector2(0, 1)
    
    surfaces = {} #TODO add surfaces instead of fucking colors
    
    def __init__(self, n_cols, n_rows, width=800, height=800, color=(0, 0, 255)):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid_rect = pygame.Rect(0, 0, width, height)
        self.cell_w = width / n_rows
        self.cell_h = width / n_cols

        self.color = color

        self._fichas = []

    def add_ficha_ip(self, col, row, team):
        ficha = Ficha(col * self.cell_w, row * self.cell_h, min(self.cell_w, self.cell_h), self.colors[f"TEAM{team}"])
        self.add_ficha(ficha)

    def add_ficha(self, ficha): 
        if not isinstance(ficha, Ficha): raise TypeError("Ur a dumbass, ficha should be an instance of Ficha")
            
        self._fichas.append(ficha)

    def draw(self, surface):
        def draw_cell(rect, offset):
            ellipse_rect = pygame.Rect(rect.x + rect.width * offset, rect.y + rect.height * offset, rect.width * (1 - 2*offset), rect.height * (1 - 2*offset))
            draw_anticircle(surface, ellipse_rect.center, ellipse_rect.width / 2, self.colors["BG"])

        for ficha in self._fichas:
            ficha.draw(surface)

        #calculate shit
        cell_w, cell_h = int(self.grid_rect.width / self.n_cols), int(self.grid_rect.height / self.n_rows)

        #draw shit
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                draw_cell(pygame.Rect(x * cell_w, y * cell_h, cell_w, cell_h), 0.05)
    
    #TODO highlight, update, moving methods...

class Ficha(object):
    def __init__(self, x, y, radius, color):
        self.rect = pygame.Rect(x, y, 2*radius, 2*radius)
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def __repr__(self):
        return f"Ficha({self.rect}, {self.color})"


main_surface = pygame.display.set_mode((800, 800))
g = Grid(7, 7)
g.draw(main_surface)
g.add_ficha_ip(3, 2, 1)
pygame.display.update()
while True: pass
