from pygame import mixer, image, transform


class Sounds:
    """
    This module contains the `Sounds` class, which is responsible for handling the game's sound effects.

    Attributes:
        settings (Settings): The game settings object.
        blaster (Sound): The sound effect for the blaster shooting.
        player_boom (Sound): The sound effect for the player's ship explosion.
        missed_asteroid (Sound): The sound effect for a missed asteroid.
        asteroid_boom (Sound): The sound effect for an asteroid explosion.
        GameOver (Sound): The sound effect for the game over screen.
        LevelUp (Sound): The sound effect for leveling up.
        SavedBrokenShip (Sound): The sound effect for saving a broken ship.
        mx (Channel): The audio channel used for playing the sounds.

    Methods:
        is_muted: A property that returns whether the sound is muted or not.
        ToggleMute: Toggles the mute state of the sound.
        _mute: Mutes the sound.
        _unmute: Unmutes the sound.
        draw_mute_img: Draws the mute image on the screen.

    """
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.blaster = mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.player_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')
        self.missed_asteroid = mixer.Sound('../Misc_Project_Files/sounds/MissedAsteroid.mp3')
        self.asteroid_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomAsteroid.mp3')
        self.GameOver = mixer.Sound('../Misc_Project_Files/sounds/GameOver.mp3')
        self.LevelUp = mixer.Sound('../Misc_Project_Files/sounds/LevelUp.mp3')
        self.SavedBrokenShip = mixer.Sound('../Misc_Project_Files/sounds/SavedBrokenShip.mp3')
        self.mx = mixer.find_channel()

        self._is_muted = None
        self.mute_symbol = image.load('../Misc_Project_Files/images/sound-off.png')
        self.mute_symbol = transform.scale_by(self.mute_symbol, 0.05)

        if self.settings.sound_muted:
            self._mute()
        else:
            self._unmute()

    @property
    def is_muted(self):
        return self._is_muted

    @is_muted.getter
    def is_muted(self):
        if self.mx.get_volume() == 0:
            self._is_muted = True
        else:
            self._is_muted = False
        return self._is_muted

    def ToggleMute(self):
        if self.is_muted:
            self._unmute()
        else:
            self._mute()

    def _mute(self):
        self.mx.set_volume(0)

    def _unmute(self):
        self.mx.set_volume(100)

    def draw_mute_img(self, screen):
        # Load the image onto a surface
        mute_surface = self.mute_symbol

        # Set the position of the mute image
        mute_rect = mute_surface.get_rect()

        #mute_rect.topright = (self.settings.screen_width, (self.settings.screen_height - mute_rect.height))
        #print(mute_rect.topright)

        # Blit the mute image onto the screen
        screen.blit(mute_surface, (self.settings.screen_width - 50, 10))
