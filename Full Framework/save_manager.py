from game_object import GameObject
import json
import os

class SaveManager():
    def __init__(self):
        self.folder =  os.path.dirname(os.path.abspath(__file__))
        
    def load_level(self, game, filename="level_data.json"):
        if filename == None or filename == "":
            print("no file to load")
            return
        
        root, ext = os.path.splitext(filename)
        if ext == "":
            filename = filename + ".json" # add .json if forgotten
        
        new_level_dict = {}
        file_dir =os.path.join(self.folder, filename)
        try:
            with open(file_dir, "r") as f:
                loaded_data = json.load(f)

            for key_str, val in loaded_data.items():
                # Convert string "0,1" back to tuple (0, 1)
                coords = tuple(map(int, key_str.split(',')))
                
                object_type = val["object_type"]
                # Recreate the GameObject
                if object_type.lower() in game.ALL_OBJECTS.keys():
                    object_type = game.ALL_OBJECTS[object_type.lower()]
                else: 
                    object_type = GameObject
                

                obj = object_type(
                    game,
                    x=val["x"],
                    y=val["y"],
                    spritesheet=val["spritesheet_name"],
                    rows=val["rows"],
                    columns=val["columns"],
                    collisionGroups=val["collisionGroups"],
                    layer=val["layer"],
                    current_row=val["current_row"],
                    current_column=val["current_column"]
                )
                
                new_level_dict[coords] = obj

            print(f"Level loaded from {filename}")
            return new_level_dict

        except FileNotFoundError:
            print("Save file", filename, "not found. Starting with empty level.")
            return {}

    def save_level(self, level_dict, filename="level_data.json"):
        root, ext = os.path.splitext(filename)
        if ext == "":
            filename = filename + ".json"
        if root == "":
            print("no file name to save")
            return

        data_to_save = {}
        file_dir = os.path.join(self.folder, filename)

        for (grid_x, grid_y, grid_layer), obj in level_dict.items():
            # JSON keys must be strings
            key_str = f"{grid_x},{grid_y},{grid_layer}"
            
            # Extract the necessary data to recreate the object
            data_to_save[key_str] = {
                "x": obj.rect.centerx,
                "y": obj.rect.centery,
                "spritesheet_name": obj.spritesheet_name if hasattr(obj, 'spritesheet_name') else None,
                "rows": obj.animator.rows if hasattr(obj, 'animator') else 1,
                "columns": obj.animator.columns if hasattr(obj, 'animator') else 1,
                "collisionGroups": obj.collisionGroups,
                "layer": obj.layer if hasattr(obj, 'layer') else 0,
                "current_row": obj.current_row,
                "current_column": obj.current_column,
                "object_type": obj.__class__.__name__
            }
            # data_to_save[key_str].update(self.surface_to_json(obj.spritesheet))
            
        with open(file_dir, "w") as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Level saved to {filename}")
