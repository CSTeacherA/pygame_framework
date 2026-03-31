import pygame
import sys
from sprite_loader import SpriteLoader
from save_manager import SaveManager
from game_object import GameObject
from player import Player
from ladder import Ladder
from goal import Goal
from spawn_player import SpawnPlayer
class Game:
    # all objects types with string names for saving/using object data
    ALL_OBJECTS = {"gameobject": GameObject, "ladder": Ladder, "player": Player, "goal":Goal, "spawnplayer":SpawnPlayer}

    def __init__(self,name=["[Game Name]"], width=800, height=600, levels=None):
        pygame.init()
        
        self.system_font = pygame.font.SysFont('Arial', 15, bold=False, italic=False)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)

        self.levels = levels

        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.sprite_loader = SpriteLoader()
        self.collision_groups = {
            "Default": pygame.sprite.LayeredUpdates(),
            "Background": pygame.sprite.LayeredUpdates(),
            "Player": pygame.sprite.LayeredUpdates(),
            "PhysicsObject": pygame.sprite.LayeredUpdates(),
            "Bounds": pygame.sprite.LayeredUpdates(),
            "Triggers": pygame.sprite.LayeredUpdates()
        } 

        self.collides_with = {
            "Player":["Bounds", "PhysicsObject", "Default"],
            "PhysicsObject":["Player", "PhysicsObject"],
            "Triggers":["Player"]
        }

        self.key_listeners = []
        self.event_listeners = []

        self.save_manager = SaveManager()
        self.current_level = 0
        self.level_data = {}
        if self.levels:
            self.level_data = self.save_manager.load_level(self, self.levels[self.current_level])

    def add(self, obj, layer):
        self.all_sprites.add(obj, layer=layer)

     # use a dictionary to manage groups with names
    def add_to_collision_group(self, name, obj):
        if name not in self.collision_groups.keys():
            self.collision_groups[name] = pygame.sprite.Group() # add any missing groups
        self.collision_groups[name].add(obj)

    def get_collision_group(self, name):
        if name in self.collision_groups.keys():
            return self.collision_groups[name]
        print("sprite group does not exist:", name)
        return self.all_sprites # return all sprites as a default to not cause an error
    
    def clear_groups(self, excludes = []):
        for sprite in self.all_sprites.sprites():
            in_excludes = False
            for exclude_group in excludes:
                if sprite in self.collision_groups[exclude_group]:
                    in_excludes = True

            if not in_excludes:
                sprite.kill()

    def load_next_level(self):
        self.clear_groups(["LevelCreator"])
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.current_level = 0

        self.save_manager.load_level(self, self.levels[self.current_level])

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()


        pygame.quit()
        sys.exit()


    def subscribe_keydown(self, obj):
        if obj not in self.key_listeners:
            self.key_listeners.append(obj)

    def unsubscribe_keydown(self, obj):
        if obj in self.key_listeners:
            self.key_listeners.remove(obj)

    def subscribe_event(self, obj):
        if obj not in self.event_listeners:
            self.event_listeners.append(obj)

    def unsubscribe_event(self, obj):
        if obj in self.event_listeners:
            self.event_listeners.remove(obj)

    def handle_events(self):
        for event in pygame.event.get():
            for listener in self.event_listeners:
                if hasattr(listener, 'on_event'):
                    listener.on_event(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                for listener in self.key_listeners:
                    # We check if the method exists to prevent crashes
                    if hasattr(listener, 'on_key_down'):
                        listener.on_key_down(event)
            
    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()