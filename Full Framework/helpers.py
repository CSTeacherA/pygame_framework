import pygame
import sys
import os
import copy

def is_two_surfaces_equal(surface1: pygame.Surface, surface2: pygame.Surface):
    # Check if dimensions and format are the same
    if surface1.get_size() != surface2.get_size() or surface1.get_bitsize() != surface2.get_bitsize():
        return False
    # Compare raw pixel data
    return surface1.get_view().raw == surface2.get_view().raw

def calculate_grid_size(image, cell_width, cell_height):
    return (image.get_width() // cell_width, image.get_height() // cell_height)

def deep_copy_pygame(obj):
    if isinstance(obj, dict):
        return {k: deep_copy_pygame(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [deep_copy_pygame(i) for i in obj]

    elif isinstance(obj, tuple):
        return tuple(deep_copy_pygame(i) for i in obj)

    elif isinstance(obj, pygame.Surface):
        return obj.copy()

    elif isinstance(obj, pygame.Rect):
        return obj.copy()
    elif isinstance(obj, pygame.Font):
        return obj.copy()

    elif hasattr(obj, "__dict__"):
        new_obj = obj.__class__.__new__(obj.__class__)
        for k, v in obj.__dict__.items():
            setattr(new_obj, k, deep_copy_pygame(v))
        return new_obj

    else:
        return copy.copy(obj)  # shallow copy fallback (NOT deepcopy)

def get_most_recent_file(folder_path):
    # Get full paths for all files in the folder
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        return None

    # Get the file with the most recent modification time
    most_recent = max(files, key=os.path.getmtime)
    return most_recent

def get_target_groups(game, collision_groups):
    targetGroups = []
    for group in collision_groups:
        if group in game.collision_matrix.keys():
            targetGroups += game.collision_matrix[group]
    return targetGroups

def get_oldest_file(folder_path):
    # Get full paths for all files in the folder
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        return None

    # Get the file with the oldest modification time
    most_recent = min(files, key=os.path.getmtime)
    return most_recent

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def load_folder (path, extention = ".png",  full_depth = False):
    if not os.path.exists(path):
        print(f"[WARNING] folder '{path}' not found.")
        return
    
    files = {}

    for filename in os.listdir(path):
        if full_depth and os.path.isdir(os.path.join(path, filename)):
            files |= load_folder(os.path.join(path, filename), extention, full_depth)

        if filename.lower().endswith(extention):
            cur_path = os.path.join(path, filename)

            try:
                image = pygame.image.load(cur_path).convert_alpha()
                key = os.path.splitext(filename)[0]
                files[key] = image
                print(f"[LOADED] {filename}")

            except Exception as e:
                print(f"[ERROR] Could not load {filename}: {e}")
    return files


KEY_MAP = {
    "mouse01": [0],
    "ctrl": [pygame.K_LCTRL, pygame.K_RCTRL],
    "shift": [pygame.K_LSHIFT, pygame.K_RSHIFT],
    "alt": [pygame.K_LALT, pygame.K_RALT],
    "enter": [pygame.K_RETURN],
    "p": [pygame.K_p],
    "s": [pygame.K_s],
    "l": [pygame.K_l],
    "z": [pygame.K_z],
    "y": [pygame.K_y],
}

def is_combo_pressed(combo_str):
    mouse = pygame.mouse.get_pressed()
    
    split_string = combo_str.split("+")
    if split_string[0] == "mouse01":
        return mouse[KEY_MAP[split_string[0]]]


    keys = pygame.key.get_pressed()
    combo = [KEY_MAP[k.strip().lower()] for k in split_string]

    return all(any(keys[key] for key in key_group) for key_group in combo)