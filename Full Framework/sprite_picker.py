import pygame
from animator import Animator
from game_object import GameObject
from empty_object import EmptyObject
class SpritePicker(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], layer = 0, grid = None, callback=None):
        super().__init__(game, x, y, None, rows, columns, collisionGroups, layer=10)

        self.spritesheet_name  = "default"
        if type(spritesheet) is str:
            print(spritesheet)
            self.spritesheet_name = spritesheet
            spritesheet = self.game.sprite_loader[self.spritesheet_name]
            
        self.animator = Animator(spritesheet, rows, columns)
        self.image = spritesheet
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grid = grid
        self.callback = callback

        # game.add(self, layer)
        
        

    def update(self, dt):
        # super().update(dt)
        mouse = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        gridIndex = self.grid.get_index(mousePos)       

        if mouse[0] and gridIndex[0] <= self.animator.rows and gridIndex[1] <= self.animator.columns:
            print("selecting tile")
            # image = self.animator.get_frame(int(gridIndex[1]),int(gridIndex[0]))
            tilename = self.spritesheet_name #+"-"+ str(gridIndex[1]) +"-"+ str(gridIndex[0])+"-"
            tile = EmptyObject(self.game, 0,0, tilename, self.animator.rows,self.animator.columns, currow=int(gridIndex[1]),curcolumn=int(gridIndex[0]))
            self.callback(tile)
            self.kill()
    