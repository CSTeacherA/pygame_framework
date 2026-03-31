
class Grid:
    def __init__(self, cellSize):
        self.cell_size = cellSize

    def get_index(self, screenPos):
        x = (round(screenPos[0]) // self.cell_size)
        y = (round(screenPos[1]) // self.cell_size)
        return (x,y)



    def get_position(self, index):
        x = (index[0] * self.cell_size) + (self.cell_size / 2)
        y = (index[1] * self.cell_size) + (self.cell_size / 2)

        return (x,y)