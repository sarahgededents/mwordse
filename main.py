from audio import audio_morse
from translate import text_to_morse, morse_to_text

if __name__ == '__main__':
    sentence = input()
    morse = text_to_morse(sentence)
    audio_morse(morse, tick_duration=.15, note="C6").play() # TODO: save later