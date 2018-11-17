#Author: mocoma

#for you to remember dumbass
# 1 = team red (1)
# -1 = team blue (2)
# 0 = no team

import pygame
import sys
import time
import powerups

class GridError(Exception):
    pass

class Grid(object):
    gravity = pygame.math.Vector2(0, 980)

    _powerups = []

    _highlighted = (-1, -1) #(x, y), the direction is determined by the gravity

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
        ficha.vel += self.gravity * 0.25
        self.add_ficha(ficha)    

    def add_ficha(self, ficha): 
        if not isinstance(ficha, Ficha): raise TypeError("Ur a dumbass, ficha should be an instance of Ficha")
            
        self._fichas.append(ficha)

    def get_fichas(self):
        return tuple(self._fichas)

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), surface.get_rect())
        
        if self._highlighted != (-1, -1):
            if self.gravity.dot(pygame.math.Vector2(1, 0)) != 0:
                for x in range(self.n_cols):
                    #create shade of grey based on gravity
                    if self.gravity.x < 0:
                        color = [int(100 + 100 * (1 - x / self.n_cols))] * 3 
                    else:
                        color = [int(100 + 100 * x / self.n_cols)] * 3 

                    to_highlight = pygame.Rect(x * self.cell_w, self._highlighted[1] * self.cell_h, self.cell_w, self.cell_h)
                    pygame.draw.rect(surface, color, to_highlight)

            elif self.gravity.dot(pygame.math.Vector2(0, 1)) != 0:
                for y in range(self.n_rows):
                    #create shade of grey based on gravity
                    if self.gravity.y < 0:
                        color = [int(100 + 100 * (1 - y / self.n_rows))] * 3 
                    else:
                        color = [int(100 + 100 * y / self.n_rows)] * 3 

                    to_highlight = pygame.Rect(self._highlighted[0] * self.cell_h, y * self.cell_h, self.cell_w, self.cell_h)
                    pygame.draw.rect(surface, color, to_highlight)

            
        for ficha in self._fichas:
            ficha.draw(surface)

        for powerup in self._powerups:
            powerup.draw(surface)
            
        #draw shit
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                cell_rect = pygame.Rect(x * self.cell_w, y * self.cell_h, self.cell_w, self.cell_h)
                surface.blit(self.surfaces["cell"], cell_rect)
    
    def update(self, dt):
        for ficha in self._fichas: 
            ficha.update(dt, self)

        for powerup in self._powerups:
            powerup.update(dt, self)

        self._powerups = [powerup for powerup in self._powerups if not powerup.used]
    
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
        
        for dx in range(-self.n_cols, self.n_cols):
            curr_count = 0
            last_team = 0
            for dy in range(self.n_rows):
                x = dx + dy
                y = dy
                if self.valid_coords(x, y):
                    if status[x][y] != last_team:
                        last_team = status[x][y]
                        curr_count = 1
                    else: curr_count += 1

                    if curr_count == 4 and last_team != 0: return last_team

        for dx in range(0, 2 * self.n_cols):
            curr_count = 0
            last_team = 0
            for dy in range(self.n_rows):
                x = dx - dy
                y = dy
                if self.valid_coords(x, y):
                    if status[x][y] != last_team:
                        last_team = status[x][y]
                        curr_count = 1
                    else: curr_count += 1

                    if curr_count == 4 and last_team != 0: return last_team

        return 0

    def valid_coords(self, x, y):
        return x >= 0 and x < self.n_cols and y >= 0 and y < self.n_rows

    def transform_coords(self, x, y):
        return (int(x / self.cell_w), int(y / self.cell_h))
    
    def highlight(self, x, y):
        if not self.valid_coords(x, y):
            self.de_highlight()

        self._highlighted = (x, y)
    def de_highlight(self):
        self._highlighted = (-1, -1)

    def g_rotate_left(self):
        if self.anyone_moving():
            raise GridError("Cant change gravity while moving boi")
        self.gravity.rotate_ip(-90)
    def g_rotate_right(self):
        if self.anyone_moving():
            raise GridError("Cant change gravity while moving boi")
        self.gravity.rotate_ip(90)

    def add_powerup(self, powerup):
       self._powerups.append(powerup) 

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

pw = powerups.GravityPowerup(pygame.Rect(3 * g.cell_w, 3 * g.cell_h, g.cell_w, g.cell_h), pygame.image.load("gravity_powerup.png"))
g.add_powerup(pw)

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
        
        if evt.type == pygame.KEYDOWN and not g.anyone_moving():
            if evt.unicode == "q": g.g_rotate_left()
            elif evt.unicode == "e": g.g_rotate_right()

        if evt.type == pygame.QUIT:
            sys.exit()

    if not g.anyone_moving():
        v = g.is_ended()
        if v != 0:
            print(v)
            sys.exit()
    
    if pygame.mouse.get_focused() != 0:
        m_pos = g.transform_coords(*pygame.mouse.get_pos())
        g.highlight(*m_pos)
    else: g.de_highlight()

    g.update(dt)
    g.draw(main_surface)
    pygame.display.update()

while True: pass
