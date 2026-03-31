import pygame
from game_object import GameObject
from player import Player
from helpers import *

class NPC(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], layer = 0, current_row=0,current_column=0):
        super().__init__(game, x, y,  spritesheet=spritesheet,rows=rows, columns=columns, collisionGroups=collisionGroups, layer=layer, current_row=current_row, current_column=current_column)


        
       
    def update(self, dt):
        pass
    