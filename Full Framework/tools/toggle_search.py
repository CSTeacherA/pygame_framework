from tools.tool import Tool

class Toggle_Search(Tool):
        
    def shortcut_activate(self, gridIndex = None):
        self.level_creator.toggle_search()