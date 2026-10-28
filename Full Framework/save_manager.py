from game_object import GameObject
import json
import os
from helpers import *
from datetime import datetime

MAX_SAVES_PER_FOLDER = 25

class SaveManager():
    def __init__(self):
        self.folder =  os.path.dirname(os.path.abspath(__file__))
        
        
    def load_level(self, game, level_name="level01", level_folder = "levels"):
        if level_name == None or level_name == "":
            print("no file to load")
            return
        
        
        new_level_dict = {}
        folder_dir =os.path.join(os.path.join(self.folder, level_folder), level_name)
        
        cur_file = get_most_recent_file(folder_dir)

        root, ext = os.path.splitext(cur_file)
        if ext == "":
            cur_file = cur_file + ".json" # add .json if not there
        

        try:
            with open(cur_file, "r") as f:
                loaded_data = json.load(f)

                new_level_dict = self.json_to_dictionary(game, loaded_data)

            print(f"Level loaded from {level_name}")
            return new_level_dict

        except FileNotFoundError:
            print("Save file", level_name, "not found. Starting with empty level.")
            return {}

    def json_to_dictionary(self, game, json_data):
        new_level_dict = {}
        for key_str, val in json_data.items():
            # Convert string "0,1" back to tuple (0, 1)
            coords = tuple(map(int, key_str.split(',')))
            
            object_type = val["object_type"]
            # Recreate the GameObject
            if object_type.lower() in game.ALL_OBJECTS.keys():
                object_type = game.ALL_OBJECTS[object_type.lower()]
            else: 
                object_type = GameObject
            
            collision_groups = ["default"]
            if "collision_groups" in val.keys():
                collision_groups = val["collision_groups"]
            elif "collisionGroups" in val.keys():
                collision_groups = val["collisionGroups"]
            else:
                print("[ERROR] no value for collision_groups")
                print(val)
            obj = object_type(
                game,
                x=val["x"],
                y=val["y"],
                spritesheet=val["spritesheet_name"],
                rows=val["rows"],
                columns=val["columns"],
                collision_groups = collision_groups,
                layer=val["layer"],
                current_row=val["current_row"],
                current_column=val["current_column"]
            )
            
            new_level_dict[coords] = obj

        return new_level_dict
    def dictionary_to_json(self, dictionary):
        data_to_save = {}
        for (grid_x, grid_y, grid_layer), obj in dictionary.items():
            # JSON keys must be strings
            key_str = f"{grid_x},{grid_y},{grid_layer}"
            
            # Extract the necessary data to recreate the object
            data_to_save[key_str] = {
                "x": obj.rect.centerx,
                "y": obj.rect.centery,
                "spritesheet_name": obj.spritesheet_name if hasattr(obj, 'spritesheet_name') else None,
                "rows": obj.animator.rows if hasattr(obj, 'animator') else 1,
                "columns": obj.animator.columns if hasattr(obj, 'animator') else 1,
                "collision_groups": obj.collision_groups if hasattr(obj, "collision_groups") else obj.collisionGroups,
                "layer": obj.layer if hasattr(obj, 'layer') else 0,
                "current_row": obj.current_row,
                "current_column": obj.current_column,
                "object_type": obj.__class__.__name__
            }
        return data_to_save

    def save_level(self, level_dict, level_name="level01",level_folder ="levels"):
        folder_dir =os.path.join(os.path.join(self.folder, level_folder), level_name)
 
        os.makedirs(folder_dir, exist_ok=True)

        data_to_save = self.dictionary_to_json(level_dict)
        
        now = str(datetime.now())
        now = now.replace(":","_")
        file_dir = os.path.join(folder_dir, level_name + "_" + now)
        with open(file_dir, "w") as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Level saved to {level_name}")
        
        files = [
            os.path.join(folder_dir, f)
            for f in os.listdir(folder_dir)
            if os.path.isfile(os.path.join(folder_dir, f))
        ]
        if len(files) > MAX_SAVES_PER_FOLDER:
            print("max saves reached, removing old files")
            file = get_oldest_file(folder_dir)
            os.remove(file)

        
