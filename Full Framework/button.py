import pygame
from grid import Grid
from game_object import GameObject
from physics_object import PhysicsObject

class Button(GameObject):

    
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], callback=None, layer = 10):
        super().__init__(game, x, y, spritesheet, rows, columns, collisionGroups, layer=10)    
        self.callback = callback
        self.game.subscribe_event(self)
        self.active = True


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if self.rect.collidepoint(event.pos):
                    if self.callback:
                        self.callback()
        

    def update(self, dt):
        pass

    def kill(self):
        self.game.unsubscribe_event(self)
        super().kill()

    