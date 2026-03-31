import pygame
from animator import Animator
from game_object import GameObject

class EmptyObject(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], layer = 0, currow=0,curcolumn=0):
        self.game = game
        self.spritesheet = spritesheet
        self.current_row = currow
        self.current_column = curcolumn
        self.x = x
        self.y = y
        self.spritesheet_name  = "default"
        if type(spritesheet) is str:
            split = spritesheet.split("-")
            self.spritesheet_name = spritesheet

            if len(split) > 2:
                 self.spritesheet_name = split[0]
                 self.cur_row = int(split[1])
                 self.cur_column = int(split[2])

            
        self.spritesheet = self.game.sprite_loader[self.spritesheet_name]
        
        if self.spritesheet:
            self.animator = Animator(self.spritesheet, rows, columns)
            self.image = self.animator.get_frame(self.current_row,self.current_column)
        
        if self.image:
            self.rect = self.image.get_rect(center=(x, y))

        

       
    def update(self, dt):
        pass

    