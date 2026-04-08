from tools.tool import Tool
from game_object import GameObject
import pygame
from helpers import *

class Eraser(Tool):
    def activate(self, gridIndex):
        exact_index = gridIndex + (self.level_creator.current_layer,)

        if exact_index in self.level_creator.level.keys():
            # print("removing block", self.level_creator.level[gridIndex].image)
            self.level_creator.level[exact_index].kill() # remove the part from game
            del self.level_creator.level[exact_index] # remove grid index
            return True
        
        return False
    
    def shortcut_activate(self):
        self.level_creator.set_tool("eraser")
        