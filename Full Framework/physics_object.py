from game_object import GameObject
import pygame

GRAVITY = 1200                # pixels per second²
AIR_FRICTION_COEFF = 1.0      # air drag strength
SURFACE_FRICTION_COEFF = .01  # sliding friction


class PhysicsObject(GameObject):
    def __init__(self,game, x, y, spritesheet, rows=1, columns =1, collisionGroups = [],layer = 1):
        super().__init__(game, x, y, spritesheet,rows, columns, collisionGroups, layer)
        
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.mass = 1
        self.grounded = False

        self.targetGroups = []
        for group in collisionGroups:
            if group in self.game.collides_with.keys():
                self.targetGroups += self.game.collides_with[group]
            
    # ------------------------
    # Force System
    # F = m * a → a = F / m
    # ------------------------
    def apply_force(self, force):
        self.acceleration += force / self.mass

    # ------------------------
    # Physics Update
    # ------------------------
    def update(self, dt):
        super().update(dt)
        # Reset grounded state
        self.grounded = False

        # Apply gravity
        self.acceleration.y += GRAVITY

        # Apply air friction (drag)
        air_drag = -AIR_FRICTION_COEFF * self.velocity
        self.acceleration += air_drag / self.mass

        # Integrate velocity
        self.velocity += self.acceleration * dt

        # Move X
        self.rect.centerx += self.velocity.x * dt
        self.handle_collisions("x")

        # Move Y
        self.rect.centery += self.velocity.y * dt
        self.handle_collisions("y")

        # Apply surface friction only if grounded
        if self.grounded:
            self.apply_surface_friction(dt)

        # Reset acceleration each frame
        self.acceleration = pygame.Vector2(0, 0)

    # ------------------------
    # Surface Friction
    # ------------------------
    def apply_surface_friction(self, dt):
        if abs(self.velocity.x) < 1:
            self.velocity.x = 0
            return

        normal_force = self.mass * GRAVITY
        friction_force = SURFACE_FRICTION_COEFF * normal_force

        friction_direction = -1 if self.velocity.x > 0 else 1

        friction_accel = (friction_force / self.mass) * friction_direction

        self.velocity.x += friction_accel * dt

        # Prevent overshooting past zero
        if (self.velocity.x > 0 and friction_direction == 1) or \
           (self.velocity.x < 0 and friction_direction == -1):
            self.velocity.x = 0

    # ------------------------
    # Collision Handling
    # ------------------------
    def handle_collisions(self, direction):
        
        for t_group in self.targetGroups:
            collided_objects = pygame.sprite.spritecollide(self, self.game.get_collision_group(t_group), False)
            
            if collided_objects:
                for sprite in collided_objects:
                    if direction == "x":
                        if self.velocity.x > 0:
                            self.rect.right = sprite.rect.left
                        elif self.velocity.x < 0:
                            self.rect.left = sprite.rect.right
                        self.velocity.x = 0

                    if direction == "y":
                        if self.velocity.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.grounded = True
                        elif self.velocity.y < 0:
                            self.rect.top = sprite.rect.bottom
                        self.velocity.y = 0