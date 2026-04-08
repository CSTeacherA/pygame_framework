from tools.tool import Tool

class Load_Tool(Tool):
        
    def shortcut_activate(self, gridIndex = None):
        self.level_creator.load()
