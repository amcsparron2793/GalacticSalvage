from pathlib import Path
from pygame import mixer, image, transform


class Sounds:
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
        self._configure_music()
        self._load_sound_effects()
        self.mute_image = transform.scale_by(image.load(self.MUTE_IMAGE_PATH), self.MUTE_IMAGE_SCALE)

        if self.settings.sound_muted:
            self._mute()
        else:
            self._unmute()

        self.sfx_audio_channel.set_volume(self.settings.sfx_volume)
        self.music_mixer.set_volume(self.settings.music_volume)

    @property
    def is_muted(self):
        return self.sfx_audio_channel.get_volume() == 0

    def _configure_music(self):
        self.music_mixer = mixer.music
        self.music_mixer.load(self.BACKGROUND_MUSIC_PATH)

    def _load_sound_effects(self):
        self.sfx_audio_channel = mixer.find_channel()
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
        self.sfx_audio_channel.set_volume(0)
        self.music_mixer.set_volume(0)

    def _unmute(self):
        self.sfx_audio_channel.set_volume(self.settings.sfx_volume)
        self.music_mixer.set_volume(self.settings.music_volume)

    def draw_mute_img(self, screen):
        mute_rect = self.mute_image.get_rect()
        screen.blit(self.mute_image, (self.settings.screen_width - 50, 10))