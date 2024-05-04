from pygame import Surface, SRCALPHA, draw, transform, Rect
import random
from pygame.sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.screen = self.settings.screen

        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        self.rect = Rect(0, 0, self.width, self.height)
        self.x = random.randint(0, self.settings.screen_width - self.width)
        self.y = -self.height  # Start above the screen
        self.speed = random.randint(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Random rotation speed

    def move(self):
        self.y += self.speed
        self.angle += self.rotation_speed

    def draw(self, screen):
        # Create a surface for the asteroid and rotate it
        #asteroid_surface = Surface((self.width, self.height), SRCALPHA)
        #draw.rect(asteroid_surface, self.color, (0, 0, self.width, self.height))
        # pygame.draw.polygon(asteroid_surface, self.color, (polys), self.width)#, self.height))
        rotated_surface = transform.rotate(asteroid_surface, self.angle)
        # Get the rect of the rotated surface and set its center to the asteroid's position
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        # Draw the rotated surface onto the screen
        screen.blit(rotated_surface, rotated_rect)

    # TODO: fix this was just copied as a skeleton
    def update(self):
        """ Move the bullet up the screen. """
        # update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        pygame.draw.rect(self.screen, self.color, self.rect)
