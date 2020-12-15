import collections

MORSE_CODE = {'A': '.-',
              'B': '-...',
              'C': '-.-.',
              'D': '-..',
              'E': '.',
              'F': '..-.',
              'G': '--.',
              'H': '....',
              'I': '..',
              'J': '.---',
              'K': '-.-',
              'L': '.-..',
              'M': '--',
              'N': '-.',
              'O': '---',
              'P': '.--.',
              'Q': '--.-',
              'R': '.-.',
              'S': '...',
              'T': '-',
              'U': '..-',
              'V': '...-',
              'W': '.--',
              'X': '-..-',
              'Y': '-.--',
              'Z': '--..',
              ' ': '/',
              '0': '-----',
              '1': '.----',
              '2': '..---',
              '3': '...--',
              '4': '....-',
              '5': '.....',
              '6': '-....',
              '7': '--...',
              '8': '---..',
              '9': '----.',
              '.': '.-.-.-',
              ',': '--..--',
              '?': '..--..',
              "'": '.----.',
              '!': '-.-.--',
              '/': '-..-.',
              '(': '-.--.',
              ')': '-.--.-',
              '&': '.-...',
              ':': '---...',
              ';': '-.-.-.',
              '=': '-...-',
              '+': '.-.-.',
              '-': '-....-',
              '_': '..--.-',
              '"': '.-..-.',
              '$': '...-..-',
              '@': '.--.-.',
              'ç': '-.-..',
              'è': '.-..-',
              'é': '..-..',
              'û': '..--',
              'à': '.--.-'}

_TEXT_TO_MORSE_TABLE = {ord(char): morse + ' ' for char, morse in MORSE_CODE.items()}
_MORSE_TO_TEXT_TABLE = {morse: char for char, morse in MORSE_CODE.items()}


def text_to_morse(text, default=None):
    table = _TEXT_TO_MORSE_TABLE
    if default is not None:
        table = collections.defaultdict(lambda: MORSE_CODE[default], table)
    return text.upper().translate(table).strip()


class MorseError(Exception):
    pass


def morse_to_text(morse, strict=False):
    def code_to_text(code):
        try:
            return _MORSE_TO_TEXT_TABLE[code]
        except LookupError as e:
            if not strict:
                return code
            else:
                raise MorseError(f"{e} is not valid morse code")
    return ''.join(code_to_text(code) for code in morse.split())