import pygame
from grid import Grid
from game_object import GameObject
from physics_object import PhysicsObject
from text_field import TextField
from sprite_picker import SpritePicker
from tools.draw_tool import DrawTool
import json
from helpers import *
from tools.eraser import Eraser
from empty_object import EmptyObject
from button import Button
from tools.fill_tool import FillTool
from tools.load import Load_Tool
from tools.toggle_palette import Toggle_Palette
from tools.toggle_search import Toggle_Search
from ladder import Ladder
import copy

from tools.save import Save_Tool




class LevelCreator(GameObject):
    COMMANDS = ["load", "setlayer", "setgroup", "help", "settool", "tileset", "setlevel", "setobject", "undo", "redo"]
    TOOLS = {"draw": DrawTool, "eraser":Eraser, "fill":FillTool}

    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collision_groups=[], layer=0, levels=None):
        super().__init__(game, x, y, spritesheet,rows, columns, collision_groups, layer=layer)
        self.grid = self.game.grid
        self.level = {}
        self.undo_stack = []
        self.redo_stack = []
        self.history_index = 0
        
        self.game.levels = levels

        self.text = ""
        self.current_layer = 0
        self.current_group = "Default"
        self.current_tool = DrawTool(game, self)
        self.tile_set = "agoria"
        self.object_type = "gameobject"

        self.current_level = "Level02"
        self.current_group_index = 0
        self.collision_group_names = list(self.game.collision_groups.keys())

        self.current_object_index = 0
        self.game_object_names = list(self.game.ALL_OBJECTS.keys())

        TOOL_BAR = [
            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "undo_icon", "callback": self.call_undo},
            {"image": "redo_icon", "callback": self.call_redo},
            # {"image": "spacer", "callback": None},
            

            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},
            {"image": "trash_icon", "callback": self.clear_level},


            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},
            {"image": "minus_icon", "callback": self.decrease_group},
            {"image": "group_icon", "callback": None},
            {"image": "plus_icon", "callback": self.increase_group},

            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "eraser_icon", "callback": self.set_tool_eraser},
            {"image": "draw_icon", "callback": self.set_tool_draw},
            {"image": "fill_icon", "callback": self.set_tool_fill},

            {"image": "palette_icon", "callback": self.toggle_palette},
            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "minus_icon", "callback": self.decrease_obj},
            {"image": "object_icon", "callback": None},
            {"image": "plus_icon", "callback": self.increase_obj},

            

            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "minus_icon", "callback": self.decrease_layer},
            {"image": "layer_icon", "callback": None},
            {"image": "plus_icon", "callback": self.increase_layer},

            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "palette_select_icon", "callback": self.toggle_palette_select},
            {"image": "level_select", "callback": self.toggle_level_select},

            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},

            {"image": "save", "callback": self.save},
            {"image": "spacer", "callback": None},
            {"image": "spacer", "callback": None},
            {"image": "load", "callback": self.load},
            ]

        end = 0
        for i, tool in enumerate(TOOL_BAR):
            image = game.sprite_loader[tool["image"]]
            button = Button(game, game.screen.get_width() - (self.grid.cell_size * i) - (self.grid.cell_size / 2), self.grid.cell_size / 2, image, callback=tool["callback"],collision_groups = ["LevelCreator"])
            end = i + 1

        print(range(end, game.screen.get_width() // self.grid.cell_size, 1))
        for i in range(end, game.screen.get_width() // self.grid.cell_size, 1):
            button = Button(game, game.screen.get_width() - (self.grid.cell_size * i) - (self.grid.cell_size / 2), self.grid.cell_size / 2, "spacer", callback=None, collision_groups = ["LevelCreator"])

        image = pygame.Surface((self.grid.cell_size,self.grid.cell_size))
        image.fill((100, 100, 100))

        if not self.game.sprite_loader.get("default_block"):
            self.game.sprite_loader.create_sprite("default_block", image)

        self.current_tile = EmptyObject(self.game,0,0, "default_block", layer=self.current_layer, collision_groups=self.current_group)

        self.search_bar = None
        self.picker = None

        self.lastRemoved = pygame.time.get_ticks()
        self.save_action()

        self.shortcut_tools = [Save_Tool(game, self, "ctrl+s"),
                             Load_Tool(game, self, "ctrl+l"),
                             Toggle_Palette(game, self, "ctrl+p"),
                             Toggle_Search(game, self, "ctrl+enter")]
        self.prev_press = ""

    
    def update(self, dt):
        action_complete = False
        mouse = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        gridIndex = self.grid.get_index(mousePos)
        gridPos = self.grid.get_position(gridIndex)


        
        if mouse[0] and mousePos[1] > 16 and  self.picker == None and pygame.time.get_ticks() - self.lastRemoved > 100:
            if self.current_tool.activate(gridIndex) and not action_complete:
                self.save_action()
                action_complete = True

        all_up = True
        for tool in self.shortcut_tools:
            if is_combo_pressed(tool.shortcut): 
                all_up = False
                if self.prev_press != tool.shortcut and not action_complete:
                    print("combo pressed")
                    tool.shortcut_activate(gridIndex)
                    self.prev_press = tool.shortcut
                    action_complete = True
        if all_up:
            self.prev_press = ""

        self.rect.centerx = gridPos[0]
        self.rect.centery = gridPos[1]

    def call_undo(self):
        self.on_text_return("undo")
    def undo(self):
        # """Revert to previous state."""

        # # move current state to redo stack
        # self.redo_stack.append(self.undo_stack.pop())

        # return safe_copy(self.undo_stack[-1])
        if len(self.undo_stack) <= 1:
            print("nothing to undo")
            return
        
        # json_level = self.undo_stack.pop() # get the last change 
        self.redo_stack.append(self.undo_stack.pop())

        # if json_level == self.game.save_manager.dictionary_to_json(self.level): # if this is the same as the current state update again
        #     self.redo_stack.append(json_level)
        #     json_level = self.undo_stack.pop() # remove the current state
        
        self.clear_level()
        self.level = self.game.save_manager.json_to_dictionary(self.game, self.undo_stack[-1]) # find last level change
        
        # self.redo_stack.append(json_level)
        if len(self.redo_stack) > 100:
            self.redo_stack.pop(0) # remove oldest
            

    def call_redo(self):
        self.on_text_return("redo")
    def redo(self):
        if len(self.redo_stack) <= 1:
            print("no actions to redo")
            return
        
        state = self.redo_stack.pop()
        self.undo_stack.append(state)

        # json_level = self.redo_stack.pop()
        # if json_level == self.game.save_manager.dictionary_to_json(self.level): # if this is the same as the current state update again
        #         self.undo_stack.append(json_level)
        #         json_level = self.redo_stack.pop() # remove the current state

        self.clear_level()
        self.level = self.game.save_manager.json_to_dictionary(self.game, self.redo_stack[-1]) # find last level change
        
            

    def on_new_tile(self, tile):
        self.current_tile = tile
        self.picker = None
        self.lastRemoved = pygame.time.get_ticks()


    def clear_level(self):
        self.game.clear_groups(["LevelCreator"])
        self.level = {}

    def save(self):
        print("saving...")
        self.game.save_manager.save_level(self.level, self.current_level)
    def load(self):
        print("Loading...")
        self.level = self.game.save_manager.load_level(self.game, self.current_level)

    def decrease_obj(self):
        self.current_object_index -= 1
        if self.current_object_index <= 0:
             self.current_object_index = 0
        self.set_object(self.game_object_names[self.current_object_index])



    def increase_obj(self):
        self.current_object_index += 1
        if self.current_object_index >= len(self.game_object_names):
             self.current_object_index = len(self.game_object_names) - 1
        self.set_object(self.game_object_names[self.current_object_index])

    def set_object(self, name):
        if name in self.game.ALL_OBJECTS.keys():
            print("setting object type to", name)
            self.object_type = name
        else:
            print("no object type", name)


    def increase_group(self):
        self.current_group_index += 1
        self.current_group_index = self.limit(self.current_group_index,0,len(self.collision_group_names) - 1)
        self.current_group = self.collision_group_names[self.current_group_index]
        print("current group:", self.current_group)

    

    def decrease_group(self):
        self.current_group_index -= 1
        self.current_group_index = self.limit(self.current_group_index,0,len(self.collision_group_names) - 1)
        self.current_group = self.collision_group_names[self.current_group_index]
        print("current group:", self.current_group)

    def increase_layer(self):
        self.current_layer += 1
        self.current_layer = self.limit(self.current_layer, 0, 10)
        print("current layer:", self.current_layer)

    def decrease_layer(self):
        self.current_layer -= 1
        self.current_layer = self.limit(self.current_layer, 0, 10)

        print("current layer:", self.current_layer)
    
    def limit(self, value, min, max):
        if value > max:
            value = max
        elif value < min:
            value = min
        return value
        

        

    def toggle_level_select(self):
        print("Enter level name.")
        self.search_bar = TextField(self.game, self.game.screen.get_width() / 2, 24, callback=self.on_text_return_level)
    def on_text_return_level(self, text):
        self.on_text_return("setlevel " + text)

    def toggle_palette_select(self):
        print("Enter tile set name.")
        self.search_bar = TextField(self.game, self.game.screen.get_width() / 2, 24, callback=self.on_text_return_palette)
    def on_text_return_palette(self, text):
        self.on_text_return("tileset " + text)

    def set_tool_eraser(self):
        self.set_tool("eraser")
    def set_tool_draw(self):
        self.set_tool("draw")
    def set_tool_fill(self):
        self.set_tool("fill")



    def set_tool(self, name):
        if name in self.TOOLS:
            self.current_tool = self.TOOLS[name](self.game, self)
        else:
            print("must select tool:", self.TOOLS, "not", name)
    def toggle_search(self):
        if self.search_bar == None:
            self.search_bar = TextField(self.game, self.game.screen.get_width() / 2, 24, callback=self.on_text_return)
        else:
            self.search_bar.kill()
            self.search_bar = None
            self.lastRemoved = pygame.time.get_ticks()

    def toggle_palette(self):
        
        if self.picker == None:
            print("Opening sprite picker")
            if type(self.tile_set) is str:
                image = self.game.sprite_loader[self.tile_set]

                columns = int(round(image.get_width() / self.grid.cell_size))
                rows =  int(round(image.get_height() / self.grid.cell_size))
                print("sprite picker rows", rows)
                self.picker = SpritePicker(self.game,0,0, self.tile_set ,rows=rows,columns=columns, grid=self.grid, callback=self.on_new_tile)
            else:
                print("tile_set must be a string")
        elif self.picker:
            print("Closing sprite picker")
            self.picker.kill()
            self.picker = None

    def parse_command(self, text):
        action = [text, ""]
        splitText = text.split(" ")
        print("command:", splitText)
        if len(splitText) >= 2:
            for command in self.COMMANDS:
                if command.lower() == splitText[0]:
                    action[0] = command.lower()
            
            action[1] = splitText[1].lower()

        return action
    
    def save_action(self):
        print("saving action")
        self.undo_stack.append(self.game.save_manager.dictionary_to_json(self.level))
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0) # remove oldest
        self.redo_stack.clear()

    def on_text_return(self, text):
        if self.search_bar != None:
            self.search_bar.kill()
            self.search_bar = None
            self.lastRemoved = pygame.time.get_ticks()

        action = self.parse_command(text)

        if action[0] == "load":
            if self.game.sprite_loader.get(action[1]):
                # self.current_tile = action[1]
                self.current_tile = EmptyObject(self.game,0,0, action[1], layer=self.current_layer, collision_groups=self.current_group)
                print("sprite " + action[1] + " found!!!")
            else:
                print("sprite " + action[1] + " not found")
        elif action[0] == "setlayer":
            self.current_layer = int(action[1])
        elif action[0] == "setgroup":
            self.current_group = action[1]
        elif action[0] == "setlevel":
            if action[1] == "":
                print("Enter value for level name")
            else:
              self.current_level = action[1]

        elif action[0] == "help":
            print(self.COMMANDS)
        elif action[0] == "settool":
            self.set_tool(action[1])
        elif action[0] == "tileset":
            if action[1] in self.game.sprite_loader.sprites:
                self.tile_set = action[1]
            else:
                print("no tile set ", action[1])
                for image in self.game.sprite_loader.sprites:
                    print(image)
        elif action[0] == "setobject":
            self.set_object(action[0])
        elif action[0] == "undo":
            self.undo()
        elif action[0] == "redo":
            self.redo()
            
        else:
            print("Command", action[0], "not found. type help to list all commands")

        self.game.screen.fill((30, 30, 30))

        if action[0] != "undo" and action[0] != "redo": 
            self.save_action()
            


    

   