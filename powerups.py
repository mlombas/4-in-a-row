import pygame
import random
from abc import ABC, abstractmethod

class Powerup(ABC):
    def __init__(self, rect, surface):
        self.rect = rect
        self.surface = pygame.transform.scale(surface, rect.size)

        self.used = False

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def update(self, dt, grid):
        if not grid.anyone_moving():
            grid_pos = grid.transform_coords(*self.rect.center)
            status = grid.get_grid_status()

            team = status[grid_pos[0]][grid_pos[1]] 
            if team != 0:
                self.do_power(grid, team)
    
    @abstractmethod
    def do_power(self, grid, team):
        pass

class GravityPowerup(Powerup):
    def do_power(self, grid, team):
        if random.randint(0, 1) == 0:
            grid.g_rotate_left()
        else:
            grid.g_rotate_right()

        self.used = True
