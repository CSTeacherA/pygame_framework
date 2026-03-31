from game_object import GameObject
from physics_object import PhysicsObject
import pygame

class Player(PhysicsObject):
    def __init__(self, game, x, y, image, rows = 1,columns =1, layer=1):
        super().__init__(game, x, y, image, rows, columns, ["Player"])
        self.speed = 300  # pixels per second
        self.jump_force = -500
        self.animator.play(0, column_limit=1) # play idle animation
        self.keyUp = True
        self.is_right = True
        

    def update(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        
        # move the player left and right and play the running animation 
        if keys[pygame.K_LEFT]:
            dx = -1
            self.is_right = False
            if self.grounded:
                self.animator.play(1, 12)
        elif keys[pygame.K_RIGHT]:
            dx = 1
            self.is_right = True
            if self.grounded:
                self.animator.play(1, 12)
        else:
            dx = 0
            if self.grounded:
                self.animator.play(0)
                self.velocity.x += -self.velocity.x  * 10 * dt

        # have the player jump
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.keyUp  and self.grounded:
            self.keyUp = False
            dy = self.jump_force
            self.animator.play_reset(2, 2) # play and reset the current column 
        elif not keys[pygame.K_UP]:
            self.keyUp = True
        

        # custom animation override to stop the jumping animation 
        if self.animator.current_row == 2 and self.animator.current_col == 2 and self.animator.playing:
            self.animator.stop()
            self.animator.set_current_column(2)

         # transition to the falling state of the jump animation whey your y velocity is negitive 
        if self.animator.current_row == 2 and self.animator.current_col == 2 and self.velocity[1] < 0: 
            self.animator.set_current_column(3)
        
        # find the current animation 
        newFrame = self.animator.get_current_frame()
        if newFrame != self.image:
            # flip animation frame if you are facing left 
            if not self.is_right:
                newFrame = pygame.transform.flip(newFrame, True, False)
            
            self.image = newFrame # set the new frame to be our new image

        self.velocity.x += dx * self.speed * dt
        self.velocity.y += dy 
        
        super().update(dt)
        