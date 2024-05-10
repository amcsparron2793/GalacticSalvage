from pygame import mixer


class Sounds:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.blaster = mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.player_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')
        self.missed_asteroid = mixer.Sound('../Misc_Project_Files/sounds/MissedAsteroid.mp3')
        self.asteroid_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomAsteroid.mp3')
        self.mx = mixer.find_channel()
        self._is_muted = None

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
