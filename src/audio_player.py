import numpy as np
import sounddevice as sd

class AudioPlayer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.current_stream = None
        self.is_playing = False
        self.current_frequency = None
        self.buffer_size = 4096
        self.phase = 0  # Mantener la fase de la onda
        
        # Notas musicales para "Cumpleaños Feliz"
        self.frequencies = {
            "dedos_0": 0.00,      # Silencio
            "dedos_1": 261.63,    # Do4 (C4)
            "dedos_2": 293.66,    # Re4 (D4)
            "dedos_3": 329.63,    # Mi4 (E4)
            "dedos_4": 349.23,    # Fa4 (F4)
            "dedos_5": 392.00,    # Sol4 (G4)
            "other": None
        }

        # Inicializar stream de audio
        self.stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._audio_callback,
            blocksize=self.buffer_size
        )
        self.stream.start()

    def generate_tone(self, frequency, frames):
        if frequency is None or frequency == 0:
            self.phase = 0
            return np.zeros(frames)

        t = (np.arange(frames) + self.phase) / self.sample_rate
        tone = np.sin(2 * np.pi * frequency * t)
        tone += 0.5 * np.sin(4 * np.pi * frequency * t)
        tone += 0.25 * np.sin(6 * np.pi * frequency * t)
        
        # Actualizar la fase para el siguiente chunk
        self.phase += frames
        
        return tone * 0.3

    def _audio_callback(self, outdata, frames, time, status):
        if not self.is_playing or self.current_frequency is None:
            outdata.fill(0)
            return

        try:
            # Generar directamente los frames necesarios
            tone = self.generate_tone(self.current_frequency, frames)
            outdata[:] = tone.reshape(-1, 1)
        except Exception as e:
            print(f"Error en callback: {e}")
            outdata.fill(0)

    def play_sound(self, gesture):
        freq = self.frequencies.get(gesture)
        if freq != self.current_frequency:
            self.current_frequency = freq
            self.is_playing = freq is not None and freq > 0
            if freq == 0:  # Reset phase only when silence
                self.phase = 0

    def stop_sound(self):
        self.is_playing = False
        self.current_frequency = None

    def __del__(self):
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()