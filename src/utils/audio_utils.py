import numpy as np
import soundfile as sf

def fade_in(audio_data, fade_duration, sample_rate):
    fade_samples = int(fade_duration * sample_rate)
    fade = np.linspace(0, 1, fade_samples)
    audio_data[:fade_samples] *= fade
    return audio_data

def fade_out(audio_data, fade_duration, sample_rate):
    fade_samples = int(fade_duration * sample_rate)
    fade = np.linspace(1, 0, fade_samples)
    audio_data[-fade_samples:] *= fade
    return audio_data

def load_sound(file_path):
    audio_data, sample_rate = sf.read(file_path)
    return audio_data, sample_rate