from pygame import mixer, Surface, SRCALPHA, draw, transform
import random

class Asteroid:
    def __init__(self):
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        self.x = random.randint(0, Settings.SCREEN_WIDTH - self.width)
        self.y = -self.height  # Start above the screen
        self.speed = random.randint(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Random rotation speed
        self.boom = mixer.Sound('../Misc_Project_Files/sounds/BoomAsteroid.mp3')

    def move(self):
        self.y += self.speed
        self.angle += self.rotation_speed

    def draw(self, screen):
        # Create a surface for the asteroid and rotate it
        asteroid_surface = pygame.Surface((self.width, self.height), SRCALPHA)
        draw.rect(asteroid_surface, self.color, (0, 0, self.width, self.height))
        # pygame.draw.polygon(asteroid_surface, self.color, (polys), self.width)#, self.height))
        rotated_surface = transform.rotate(asteroid_surface, self.angle)
        # Get the rect of the rotated surface and set its center to the asteroid's position
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        # Draw the rotated surface onto the screen
        screen.blit(rotated_surface, rotated_rect)
