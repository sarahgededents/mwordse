import numpy as np
import simpleaudio as sa

NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


class NoteError(Exception):
    pass


def note_to_frequency(note, octave=0):
    note = note.upper()
    if note[-1].isdigit():
        octave, note = int(note[-1]) - 4, note[:-1]
    try:
        note_index = NOTES.index(note)
        if note_index >= 3:
            octave -= 1
        half_steps = note_index + 12 * octave
    except ValueError:
        raise NoteError(f"'{note}' is not a note")
    return 440 * pow(2, half_steps / 12)


class AudioBuilder:
    def __init__(self, tick_duration, sample_rate=44100):
        self.audio = []
        self.tick_duration = tick_duration
        self.sample_rate = sample_rate

    def _ticks_to_num_samples(self, ticks):
        return int(ticks * self.tick_duration * self.sample_rate)

    def _sine_wave(self, freq, ticks):
        duration = ticks * self.tick_duration
        num_samples = self._ticks_to_num_samples(ticks)
        t = np.linspace(0, duration, num_samples, False)
        return np.sin(freq * t * 2 * np.pi)

    def append_frequency(self, freq, ticks):
        self.audio += self._sine_wave(freq, ticks).tolist()

    def append_note(self, note, ticks):
        freq = note_to_frequency(note)
        self.append_frequency(freq, ticks)

    def append_silence(self, ticks):
        self.audio += [0] * self._ticks_to_num_samples(ticks)

    def build(self):
        audio = np.asarray(self.audio)
        audio = audio * (2 ** 15 - 1) / np.max(np.abs(audio))
        return audio.astype(np.int16)

    def play(self):
        audio = self.build()
        return sa.play_buffer(audio, num_channels=1, bytes_per_sample=2, sample_rate=self.sample_rate)

    def lstrip(self):
        start = 0
        while start < len(self.audio) and not self.audio[start]:
            start += 1
        self.audio = self.audio[start:]
        return self

    def rstrip(self):
        end = len(self.audio) - 1
        while end >= 0 and not self.audio[end]:
            end -= 1
        self.audio = self.audio[:end+1]
        return self

    def strip(self):
        return self.lstrip().rstrip()


def audio_morse(sentence, tick_duration=.15, note='C6', **kwargs):
    audio = AudioBuilder(tick_duration, **kwargs)
    for i in sentence:
        if i == '.':
            audio.append_note(note, 1)
            audio.append_silence(1)
        elif i == '-':
            audio.append_note(note, 3)
            audio.append_silence(1)
        elif i == '/':
            audio.append_silence(7)
        elif i == ' ':
            audio.append_silence(3)
        else:
            for _ in range(6):
                audio.append_note(note, 1)
                audio.append_silence(1)
            print("Something went wrong!")
    audio.strip()
    return audio


def test_ntf(note, frequency):
    return round(note_to_frequency(note), 2) == frequency


assert test_ntf('A', 440)
assert test_ntf('A4', 440)
assert test_ntf('B4', 493.88)
assert test_ntf('C4', 261.63)
assert test_ntf('E0', 20.60)
assert test_ntf('F8', 5587.65)