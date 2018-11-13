#Author: mocoma

#for you to remember dumbass
# 1 = team red (1)
# -1 = team blue (2)
# 0 = no team

import pygame
import sys
import time

class GridError(Exception):
    pass

class Grid(object):
    gravity = pygame.math.Vector2(0, 980)
    
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
        if self.anyone_moving():
            raise GridError("cant add ficha when anyone is moving")
        
        if self.get_grid_status()[col][row] != 0:
            raise GridError("cant add ficha in top of another")

        ficha = Ficha(pygame.Rect(col * self.cell_w, row * self.cell_h, self.cell_w, self.cell_h), self.surfaces[f"team{team}"], team)
        self.add_ficha(ficha)

    def add_ficha(self, ficha): 
        if not isinstance(ficha, Ficha): raise TypeError("Ur a dumbass, ficha should be an instance of Ficha")
            
        self._fichas.append(ficha)

    def get_fichas(self):
        return tuple(self._fichas)

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), surface.get_rect())

        for ficha in self._fichas:
            ficha.draw(surface)

        #draw shit
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                surface.blit(self.surfaces["cell"], (x * self.cell_w, y * self.cell_h))
    
    def update(self, dt):
        for ficha in self._fichas: 
            ficha.update(dt, self)
    
    def anyone_moving(self):
        return any(f.is_moving() for f in self._fichas)

    def get_grid_status(self):
        if self.anyone_moving():
           raise GridError("cant get status if anyone moving dumbass")

        representation = [[0 for y in range(self.n_rows)] for x in range(self.n_cols)]
        for ficha in self._fichas:
            x, y = ficha.rect.center
            col = int(x / self.cell_w)
            row = int(y / self.cell_h)

            representation[col][row] = ficha.team
        
        return representation
    
    def is_ended(self):
        status = self.get_grid_status()
 
        for x in range(self.n_cols):
            curr_count = 0
            last_team = 0
            for y in range(self.n_rows):
                if status[x][y] != last_team:
                    last_team = status[x][y]
                    curr_count = 1
                else: curr_count += 1

                if curr_count == 4 and last_team != 0: return last_team

        for y in range(self.n_rows):
            curr_count = 0
            last_team = 0
            for x in range(self.n_cols):
                if status[x][y] != last_team:
                    last_team = status[x][y]
                    curr_count = 1
                else: curr_count += 1
            
                if curr_count == 4 and last_team != 0: return last_team
        
        #TODO fix this
        for ry in range(-self.n_rows, 1):
            for x in range(self.n_cols):
                y = ry + x
                if y > 0:
                    if status[x][y] != last_team:
                        last_team = status[x][ry]
                        curr_count = 1
                    else: curr_count += 1
            
                    if curr_count == 4 and last_team != 0: return last_team

        for ry in range(-self.n_rows, 1):
            for x in range(self.n_cols - 1, -1, -1):
                y = ry + x
                if y > 0:
                    if status[x][y] != last_team:
                        last_team = status[x][ry]
                        curr_count = 1
                    else: curr_count += 1
            
                    if curr_count == 4 and last_team != 0: return last_team

        return 0

class Ficha(object):
    def __init__(self, rect, surface, team):
        self.rect = rect
        self.vel = pygame.math.Vector2(0, 0)
        self.surface = pygame.transform.scale(surface, rect.size)
        self.team = team

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
 
    def update(self, dt, grid):
        self.vel += grid.gravity * dt
        offset = self.vel * dt
        next_move = self.rect.move(offset.x, offset.y)

        collides_with_ficha = any(next_move.colliderect(other.rect) for other in grid.get_fichas() if other != self.rect)
        is_in_grid = bool(grid.grid_rect.contains(next_move))
        if collides_with_ficha or not is_in_grid:
            self.vel = pygame.math.Vector2(0, 0)
        else:
            self.rect = next_move

    def is_moving(self):
        return self.vel.length() > 1e2

    def __repr__(self):
        return f"Ficha({self.rect}, {self.color})"


main_surface = pygame.display.set_mode((800, 800))
g = Grid(7, 7)

last_time = time.clock()
while True:
    dt = time.clock() - last_time
    last_time = time.clock()

    for evt in pygame.event.get():
        if evt.type == pygame.MOUSEBUTTONUP and not g.anyone_moving():
            x, y = evt.pos
            col = int(x / g.cell_w)
            row = int(y / g.cell_h)
            
            try:
                g.add_ficha_ip(col, row, 1 if evt.button == 1 else -1)
            except GridError:
                pass
    
        if evt.type == pygame.QUIT:
            sys.exit()

    if not g.anyone_moving():
        v = g.is_ended()
        if v != 0:
            print(v)
            sys.exit()
        
    g.update(dt)
    g.draw(main_surface)
    pygame.display.update()

while True: pass
