import pygame
from game_object import GameObject
from player import Player
from helpers import *

class SpawnPlayer(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], layer = 0, current_row=0,current_column=0):
        super().__init__(game, x, y,  spritesheet=spritesheet,rows=rows, columns=columns, collisionGroups=collisionGroups, layer=layer, current_row=current_row, current_column=current_column)
        self.x = x
        self.y = y

        self.start_time = pygame.time.get_ticks()
        
       
    def update(self, dt):
        if pygame.time.get_ticks() - self.start_time > .5:
            image = self.game.sprite_loader["yehv2"]
            gridsize = calculate_grid_size(image, 16, 32) # use helper tool to calculate the grid size of the player sprite sheet automatically 

            myPlayer = Player(self.game, self.x, self.y, image, gridsize[1], gridsize[0], layer=5)
            self.kill()
    