from tools.tool import Tool

class Save_Tool(Tool):
        
    def shortcut_activate(self, gridIndex = None):
        self.level_creator.save()