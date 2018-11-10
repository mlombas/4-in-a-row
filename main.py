#Author: mocoma

#for you to remember dumbass
# 1 = team red (1)
# -1 = team blue (2)
# 0 = no team

import pygame

#TODO add errors

class Grid(object):
    gravity = pygame.math.Vector2(0, 1)
    
    surfaces = {}     

    def __init__(self, n_cols, n_rows, width=800, height=800, color=(0, 0, 255)):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid_rect = pygame.Rect(0, 0, width, height)
        self.cell_w = int(width / n_rows)
        self.cell_h = int(width / n_cols)

        self._fichas = []

        self.surfaces["cell"] = pygame.transform.scale(pygame.image.load("cell.png"), (self.cell_w, self.cell_h))
        self.surfaces["team1"] = pygame.transform.scale(pygame.image.load("red_ficha.png"), (self.cell_w, self.cell_h))
        self.surfaces["team-1"] = pygame.transform.scale(pygame.image.load("blue_ficha.png"), (self.cell_w, self.cell_h))

    def add_ficha_ip(self, col, row, team):
        ficha = Ficha(pygame.Rect(col * self.cell_w, row * self.cell_h, self.cell_w, self.cell_h), self.surfaces[f"team{team}"])
        self.add_ficha(ficha)

    def add_ficha(self, ficha): 
        if not isinstance(ficha, Ficha): raise TypeError("Ur a dumbass, ficha should be an instance of Ficha")
            
        self._fichas.append(ficha)

    def draw(self, surface):
        for ficha in self._fichas:
            ficha.draw(surface)

        #calculate shit
        cell_w, cell_h = int(self.grid_rect.width / self.n_cols), int(self.grid_rect.height / self.n_rows)

        #draw shit
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                surface.blit(self.surfaces["cell"], (x * cell_w, y * cell_h))
    
    #TODO update
    #TODO anyone_moving
    #TODO get_grid_status
    #TODO highlight_row, highlight_col
    #TODO is_ended 

class Ficha(object):
    def __init__(self, rect, surface):
        self.rect = rect
        self.surface = pygame.transform.scale(surface, rect.size)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
 
    #TODO update
    
    def __repr__(self):
        return f"Ficha({self.rect}, {self.color})"


main_surface = pygame.display.set_mode((800, 800))
g = Grid(7, 7)
g.add_ficha_ip(3, 2, 1)
g.add_ficha_ip(0, 0, -1)
g.add_ficha_ip(5, 3, -1)
g.draw(main_surface)
pygame.display.update()
while True: pass
