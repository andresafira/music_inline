from typing import *
from constants import *
import os
from pydub import AudioSegment


def get_oct_mod(s: str) -> Tuple[str, int]:
    oct_add = 0
    s_ = ''
    for modifier in s:
        if modifier in OCTAVE_MODIFIER.keys():
            oct_add += OCTAVE_MODIFIER[modifier]
        else:
            s_ += modifier
    return s_, oct_add


def get_note(repr: str, octave: int = 0) -> Union[int, None]:
    if repr not in NOTES.keys():
        raise ValueError('Invalid note representation')
    if not (-5 <= octave <= 5):
        raise ValueError('Octave must be between -5 and 5, included')

    if NOTES[repr] is None:
        return None
    return NOTES[repr] + 12*(octave + MID_OCTAVE)


def get_slice(s: str, keyword_begin: str, keyword_end: str = None) -> Union[str, None]:
    if keyword_end is None:
        keyword_end = keyword_begin
    first = s.find(f'{keyword_begin}[')
    if first == -1:
        return None
    first += len(f'{keyword_begin}[')
    last = s.find(f']{keyword_end}')
    if last == -1:
        return None
    return s[first: last]


def midi_to_mp3(midi_file):
    soundfont = '../../../../Downloads/GeneralUser_GS_1.471'
    # Convert MIDI to WAV using fluidsynth
    wav_file = midi_file.replace('.mid', '.wav')
    mp3_file = midi_file.replace('.mid', '.mp3')
    os.system(f'fluidsynth -ni {soundfont} {midi_file} -F {wav_file} -r 44100')

    # Convert WAV to MP3 using pydub
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format='mp3')

    # Remove temporary WAV file
    os.remove(midi_file)
    os.remove(wav_file)
    