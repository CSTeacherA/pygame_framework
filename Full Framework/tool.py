import pygame

class Tool():
    def __init__(self, game, level_creator):
        self.game = game
        self.level_creator = level_creator
        self.keysup = {
            pygame.K_p:True,
            "mouse0":True
            }
        
    def Activate(self, gridIndex):
        pass