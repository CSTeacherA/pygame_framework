from tool import Tool
from game_object import GameObject
from helpers import *

class FillTool(Tool):
    
    def inBounds(self, node):
        if node[0] < 0 or node[0] >= self.game.screen.get_width() // self.level_creator.grid.cell_size or node[1] <= 0 or node[1] >= self.game.screen.get_height() // self.level_creator.grid.cell_size:
            return False
        return True
    
    def check_neighbors(self, node):
        neighbors = []
        gridPos = self.level_creator.grid.get_position((node[0], node[1]))
        current_tile = self.level_creator.current_tile

        part = GameObject(self.game, gridPos[0],gridPos[1], current_tile.spritesheet_name,current_tile.animator.rows, current_tile.animator.columns, collisionGroups=[self.level_creator.current_group], layer=self.level_creator.current_layer, current_row=current_tile.current_row, current_column=current_tile.current_column)
        self.level_creator.level[node] = part
        self.closed.append(node)

        for x in range(-1,2):
            for y in range(-1,2):
                if abs(x) == 1 and abs(y) == 1:
                    continue # ignore diagonals 
                neighbor = (node[0] + x, node[1] + y, self.level_creator.current_layer)
                if neighbor not in self.closed and self.inBounds(neighbor):
                    neighbors.append(neighbor)

        for neighbor in neighbors:
            self.check_neighbors(neighbor)
        

    def Activate(self, gridIndex):
        start = gridIndex + (self.level_creator.current_layer,)
        self.closed = list(self.level_creator.level.keys())

        if start not in self.closed:
            self.check_neighbors(start)