from tools.tool import Tool

class Toggle_Palette(Tool):
        
    def shortcut_activate(self, gridIndex = None):
        self.level_creator.toggle_palette()