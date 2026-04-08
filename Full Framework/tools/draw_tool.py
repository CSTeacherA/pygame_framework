from tools.tool import Tool
from game_object import GameObject
from helpers import *

class DrawTool(Tool):

    def activate(self, gridIndex):
        exact_index = gridIndex + (self.level_creator.current_layer,)
        gridPos = self.level_creator.grid.get_position(gridIndex)
        current_tile = self.level_creator.current_tile

        if exact_index in self.level_creator.level.keys():
            if self.level_creator.level[exact_index].spritesheet_name != current_tile.spritesheet_name or self.level_creator.level[exact_index].current_row != current_tile.current_row or self.level_creator.level[exact_index].current_column != current_tile.current_column:
                print("removing old part")
                self.level_creator.level[exact_index].kill()
                del self.level_creator.level[exact_index]

        object_type = self.game.ALL_OBJECTS[self.level_creator.object_type]

        if object_type and exact_index not in self.level_creator.level.keys(): #or self.level_creator.level[gridIndex].spritesheet_name != current_tile.spritesheet_name:
            part = object_type(self.game, gridPos[0],gridPos[1], current_tile.spritesheet_name,current_tile.animator.rows, current_tile.animator.columns, collision_groups=[self.level_creator.current_group], layer=self.level_creator.current_layer, current_row=current_tile.current_row, current_column=current_tile.current_column)
            self.level_creator.level[exact_index] = part
            print("creating new part type", self.level_creator.object_type)
            return True
        elif object_type == None:
            print("No object type")
        elif exact_index in self.level_creator.level.keys():
            print("existing part in level")
        return False
            

    def shortcut_activate(self):
        self.level_creator.set_tool("draw")