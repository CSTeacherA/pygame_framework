from tool import Tool
from game_object import GameObject
import pygame
from helpers import *

class Eraser(Tool):
    def Activate(self, gridIndex):
        exact_index = gridIndex + (self.level_creator.current_layer,)

        if exact_index in self.level_creator.level.keys():
            # print("removing block", self.level_creator.level[gridIndex].image)
            self.level_creator.level[exact_index].kill() # remove the part from game
            del self.level_creator.level[exact_index] # remove grid index
        