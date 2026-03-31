import pygame
from animator import Animator


class GameObject(pygame.sprite.Sprite):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], layer = 0, current_row=0,current_column=0):
        super().__init__()
        self.layer = layer
        self.spritesheet = spritesheet
        self.current_row = current_row
        self.current_column = current_column
        self.game = game
        

        self.collisionGroups = collisionGroups
        for group in collisionGroups:
            game.add_to_collision_group(group, self) # add self to all marked groups

        self.image = None
        self.spritesheet_name  = "default"
        if type(spritesheet) is str:
            split = spritesheet.split("-")
            self.spritesheet_name = spritesheet

            if len(split) > 2:
                 self.spritesheet_name = split[0]
                 self.current_row = int(split[1])
                 self.current_column = int(split[2])

            
            self.spritesheet = self.game.sprite_loader[self.spritesheet_name]

        # add Animator 
        if self.spritesheet:
            self.animator = Animator(self.spritesheet, rows, columns)
            self.image = self.animator.get_frame(self.current_row,self.current_column)

        if self.image:
            self.rect = self.image.get_rect(center=(x, y))

        self.game.add(self, layer)

    def update(self, dt):
        if hasattr(self, "animator"):
            self.animator.update(dt)
            # self.image = self.animator.get_current_frame()

    def camera_update(self, dx, dy, dt):
        self.rect.x += dx * dt
        self.rect.y += dy * dt

    