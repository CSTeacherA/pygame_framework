import pygame
from game_object import GameObject
from physics_object import PhysicsObject
# from player import Player
class Ladder(GameObject):
    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collision_groups=[], layer = 0, current_row=0,current_column=0):
        super().__init__(game, x, y,  spritesheet=spritesheet,rows=rows, columns=columns, collision_groups=collision_groups, layer=layer, current_row=current_row, current_column=current_column)
        self.ladder_speed = -1000
        self.targetGroups = []
        for group in collision_groups:
            if group in self.game.collision_matrix.keys():
                self.targetGroups += self.game.collision_matrix[group]
    
    def update(self, dt):
        for t_group in self.targetGroups:
            collided_objects = pygame.sprite.spritecollide(self, self.game.get_collision_group(t_group), False)
            for obj in collided_objects:
                if isinstance(obj, PhysicsObject):
                    obj.velocity[1] += dt * self.ladder_speed 

    