import pygame as pg
import pygame.sndarray as sndarray
import numpy as np
import time

class Synthesizer:
    def __init__(self, sampling_rate=44100):
        pg.init()
        pg.mixer.init(buffer=1024)
        self.sampling_rate = sampling_rate

    def synth(self, frequency, duration=1, release_duration=0.1):
        frames = int(duration * self.sampling_rate)
        release_frames = int(release_duration * self.sampling_rate)

        t = np.linspace(0, duration, frames, endpoint=False)

        harmonics = [
            0.2 * np.sin(2 * np.pi * frequency * t),
            0.1 * np.sin(2 * np.pi * 2 * frequency * t),
            0.05 * np.sin(2 * np.pi * 3 * frequency * t),
            0.025 * np.sin(2 * np.pi * 4 * frequency * t),
            0.0125 * np.sin(2 * np.pi * 5 * frequency * t),
        ]

        arr = np.sum(harmonics, axis=0)

        sustain_env = np.ones(frames)

        sound = np.asarray([32767 * arr * sustain_env, 32767 * arr * sustain_env]).T.astype(np.int16)
        sound = sndarray.make_sound(sound.copy())

        return sound

    def play_sound(self, frequency):
        sound = self.synth(frequency)
        sound.play()
    
