from game import Game
from game_object import GameObject
from physics_object import PhysicsObject
from player import Player
import pygame
from level_creator import LevelCreator
import sys
from helpers import *

sys.setrecursionlimit(5000) # need higher recursion limit for fill tool

# create the game in game mode, not in level edit mode
# game = Game("Framework",16 * 50, 16 *37,["Levels/Level01.json"])

#create the game without setting any levels 
game = Game("Framework",16 * 50, 16 *37)


# selection tool for level creator 
image = pygame.Surface((16, 16), pygame.SRCALPHA)
image.fill((0, 0, 0, 0))
pygame.draw.rect(image, (0, 0, 255, 255), (0, 0, 16, 16), 2)
myLevel = LevelCreator(game, 0, 0, image, layer=100, collisionGroups=["LevelCreator"], levels=["Levels/Level01.json"]) 

# load the starting level
myLevel.level = game.save_manager.load_level(game, "Levels/Level01.json") 

game.run()