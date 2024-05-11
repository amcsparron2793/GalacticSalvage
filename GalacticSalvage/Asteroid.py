from os import listdir
from os.path import isfile, join

from pygame import Surface, SRCALPHA, draw, transform, image, time, display
from pygame.sprite import Sprite
import random


class Asteroid(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        if not isfile('../Misc_Project_Files/images/SingleAsteroid.png'):
            self.image = Surface((self.width, self.height), SRCALPHA)
            draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        else:
            self.image = image.load('../Misc_Project_Files/images/SingleAsteroid.png')
            self.image = transform.scale_by(self.image, random.uniform(
                self.settings.asteroid_scale_min, self.settings.asteroid_scale_max))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = random.randint(self.settings.asteroid_speed_min, self.settings.asteroid_speed_max)
        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1)  # Random rotation speed

    def update(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed

        # Limit the rotation angle within a range (-180 to 180 degrees)
        # if self.angle > 180:
        #     self.angle -= 360
        # elif self.angle < -180:
        #     self.angle += 360
        #
        # self.image = transform.rotate(self.image, self.angle)


class Explosion(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        frame_dir = '../Misc_Project_Files/images/ExplosionPNG/'
        self.animation_frames = [image.load(join(frame_dir, x)) for x in listdir(frame_dir)]

    def play_animation(self):
        # frame_duration = 50  # Duration of each frame in milliseconds
        for frame in self.animation_frames:
            rect = frame.get_rect()
            display.update(rect)
            self.settings.screen.blit(transform.scale_by(frame, 1.5), (rect.x, rect.y))  # Display the current frame
            # time.wait(frame_duration)  # Pause for the frame duration
