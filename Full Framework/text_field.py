import pygame
from grid import Grid
from game_object import GameObject
from physics_object import PhysicsObject

class TextField(GameObject):


    def __init__(self, game, x = 0, y = 0, spritesheet=None, rows=1, columns=1, collisionGroups=[], callback=None, FontSize=10, layer = 10):
        super().__init__(game, x, y, None,rows, columns, collisionGroups, layer=10)
        self.game = game
        self.game.add(self, layer)
        self.x = x
        self.y = y
    
        self.callback = callback
        self.game.subscribe_keydown(self)
        self.active = True

        self.text = ""

        self.render_text()


    def render_text(self):
        # 1. Create the new surface
        display_string = self.text if self.text != "" else "Type here..."
        self.image = self.game.system_font.render(display_string, True, (255, 255, 255))
        
        # 2. Capture the current center before we replace the rect
        current_center = self.rect.center if hasattr(self, 'rect') else (self.x, self.y)
        
        # 3. Create the new rect from the new image
        self.rect = self.image.get_rect()
        
        # 4. Put it back where it belongs
        self.rect.center = current_center

        self.game.screen.blit(self.image, [self.rect.centerx,self.rect.centery])

        # print(f"Text: {self.text} | Rect: {self.rect} | Center: {self.rect.center}")

    def on_key_down(self, event):    
        if not self.active: return

        if event.key == pygame.K_RETURN:
            if self.callback: self.callback(self.text)
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        
        self.render_text()

    def update(self, dt):
        pass

    def kill(self):
        self.game.unsubscribe_keydown(self)
        super().kill()

    