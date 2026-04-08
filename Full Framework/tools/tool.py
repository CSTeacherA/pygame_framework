import pygame

class Tool():
    def __init__(self, game, level_creator, shortcut = ""):
        self.game = game
        self.level_creator = level_creator
        self.keysup = {
            pygame.K_p:True,
            "mouse0":True
            }
        self.shortcut = shortcut
        
    def activate(self, gridIndex = None):
        pass

    def shortcut_activate(self):
        pass