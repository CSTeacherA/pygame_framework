import pygame
import os

class SpriteLoader:
    def __init__(self, folder="sprites"):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(self.script_dir, folder)

        # self.folder = folder
        self.sprites = {}
        self.load_sprites(self.folder)


    def create_sprite(self, name, surface):
        try:
            # Ensure the filename ends in .png
            if not name.lower().endswith('.png'):
                name += '.png'
            pygame.image.save(surface, self.folder + "/" + name)
            print(f"Successfully saved to {name}")
        except pygame.error as e:
            print(f"Failed to save image: {e}")

        self.sprites[name] = surface
        
    # loads all sprites in folder 
    def load_sprites(self, folder):
        if not os.path.exists(folder):
            print(f"[WARNING] Sprite folder '{folder}' not found.")
            return

        for filename in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, filename)):
                self.load_sprites(os.path.join(folder, filename))
 
            if filename.lower().endswith(".png"):
                path = os.path.join(folder, filename)

                try:
                    image = pygame.image.load(path).convert_alpha()
                    key = os.path.splitext(filename)[0]
                    self.sprites[key] = image
                    print(f"[LOADED] {filename}")

                except Exception as e:
                    print(f"[ERROR] Could not load {filename}: {e}")

    # gets sprite by name
    def get(self, name):
        return self.sprites.get(name, None)

    # get image directly sprites["player"]
    def __getitem__(self, name):
        return self.get(name)