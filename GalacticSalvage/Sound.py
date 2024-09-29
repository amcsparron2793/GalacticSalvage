from pathlib import Path

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
        game_over (Sound): The sound effect for the game over screen.
        level_up (Sound): The sound effect for leveling up.
        saved_broken_ship (Sound): The sound effect for saving a broken ship.
        mx (Channel): The audio channel used for playing the sounds.
    Methods:
        is_muted: A property that returns whether the sound is muted or not.
        toggle_mute: Toggles the mute state of the sound.
        _mute: Mutes the sound.
        _unmute: Unmutes the sound.
        draw_mute_img: Draws the mute image on the screen.
    """

    BLASTER_SOUND_PATH = Path('../Misc_Project_Files/sounds/blaster.mp3')
    PLAYER_BOOM_SOUND_PATH = Path('../Misc_Project_Files/sounds/BoomPlayer.mp3')
    MISSED_ASTEROID_SOUND_PATH = Path('../Misc_Project_Files/sounds/MissedAsteroid.mp3')
    ASTEROID_BOOM_SOUND_PATH = Path('../Misc_Project_Files/sounds/BoomAsteroid.mp3')
    GAME_OVER_SOUND_PATH = Path('../Misc_Project_Files/sounds/GameOver.mp3')
    LEVEL_UP_SOUND_PATH = Path('../Misc_Project_Files/sounds/LevelUp.mp3')
    SAVED_BROKEN_SHIP_SOUND_PATH = Path('../Misc_Project_Files/sounds/SavedBrokenShip.mp3')
    BACKGROUND_MUSIC_PATH = Path('../Misc_Project_Files/sounds/8BitSpaceBackground.mp3')
    MUTE_IMAGE_PATH = Path('../Misc_Project_Files/images/sound-off.png')
    MUTE_IMAGE_SCALE = 0.05

    def __init__(self, gs_game):
        self.settings = gs_game.settings

        self.music_mx = mixer.music
        self.music_mx.load(self.BACKGROUND_MUSIC_PATH)

        self._load_sfx()
        self.mx = mixer.find_channel()
        self._is_muted = None
        self.mute_symbol = image.load(self.MUTE_IMAGE_PATH)
        self.mute_symbol = transform.scale_by(self.mute_symbol, self.MUTE_IMAGE_SCALE)

        #self.mx.play(self.background_music)
        if self.settings.sound_muted:
            self._mute()
        else:
            self._unmute()
        self.music_mx.play(-1)


    @property
    def is_muted(self):
        self._is_muted = self.mx.get_volume() == 0
        return self._is_muted

    def _load_sfx(self):
        self.blaster = mixer.Sound(self.BLASTER_SOUND_PATH)
        self.player_boom = mixer.Sound(self.PLAYER_BOOM_SOUND_PATH)
        self.missed_asteroid = mixer.Sound(self.MISSED_ASTEROID_SOUND_PATH)
        self.asteroid_boom = mixer.Sound(self.ASTEROID_BOOM_SOUND_PATH)
        self.game_over = mixer.Sound(self.GAME_OVER_SOUND_PATH)
        self.level_up = mixer.Sound(self.LEVEL_UP_SOUND_PATH)
        self.saved_broken_ship = mixer.Sound(self.SAVED_BROKEN_SHIP_SOUND_PATH)

    def toggle_mute(self):
        if self.is_muted:
            self._unmute()
        else:
            self._mute()

    def _mute(self):
        self.mx.set_volume(0)
        self.music_mx.set_volume(0)

    def _unmute(self):
        self.mx.set_volume(100)
        self.music_mx.set_volume(100)

    def draw_mute_img(self, screen):
        # Load the image onto a surface
        mute_surface = self.mute_symbol
        # Set the position of the mute image
        mute_rect = mute_surface.get_rect()
        # Blit the mute image onto the screen
        screen.blit(mute_surface, (self.settings.screen_width - 50, 10))