import pygame
from game_object import GameObject
from physics_object import PhysicsObject
from helpers import *

# from player import Player
class Ladder(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collision_groups=[], layer = 0, current_row=0,current_column=0):
        super().__init__(game, x, y,  spritesheet=spritesheet,rows=rows, columns=columns, collision_groups=collision_groups, layer=layer, current_row=current_row, current_column=current_column)
        
        self.ladder_speed = -1000
        self.targetGroups = get_target_groups(game, collision_groups) # get all groups we should collide with
    
    
    def update(self, dt):
        for target_group in self.targetGroups:

            # get all of the objects in this target group that we are currently colliding with
            collided_objects = pygame.sprite.spritecollide(self, self.game.get_collision_group(target_group), False)
            
            for obj in collided_objects: 
                if isinstance(obj, PhysicsObject): # if any of these objects are a physics object then apply some force to them
                    obj.velocity[1] += dt * self.ladder_speed # move the object up

    
