import pygame
from physics_object import PhysicsObject
from player import Player
from helpers import *
from game_object import GameObject
class NPC(PhysicsObject):
    def __init__(self, game, x, y, image, rows = 1,columns =1, layer=1):
        super().__init__(game, x, y, image, rows, columns, ["NPC"])
        self.direction = [1,0]
        self.is_right = True
        self.speed = 100
        
    
    def check_ledge(self, right = 1):
        grid_index = self.game.grid.get_index(self.rect.x, self.rect.y) + (self.layer,)
        down_step = (grid_index[0] + right, grid_index[1] - 1, grid_index[2])
        
        obj = self.game.level_data[down_step]
        if obj and isinstance(obj, GameObject):
            for group in self.collision_groups:
                if self.game.collides_with(group, obj.collision_groups):
                    
                    return True
        return False

    def update(self, dt):
        dx = 0
        dy = 0

        dx += self.direction[0] * self.speed * dt
        if self.direction[0] > 0:
            self.is_right = True
        elif self.direction[0] < 0:
            self.is_right = False
        else:
            dx = 0


        
    