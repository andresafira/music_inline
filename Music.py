from constants import *
from utils import *
from midiutil import MIDIFile
import os


class Music:
    def __init__(self, tempo: float = 100, volume: float = 100, channel: int = 0,
                 base_octave: int = 0, track: int = 0):
        self.tempo = tempo
        self.volume = max(min(volume, 127), 0)
        self.channel = channel
        self.base_octave = base_octave
        self.track = track
        self.title = 'sample'

        self.midi = MIDIFile(1)

        self.script_list = []
        self.key_factor = {}

    def def_key(self, s: Union[str, List[str]]):
        if type(s) is str:
            txt = s.replace('\n', ' ').split(' ')
            for element in txt:
                if len(element) == 0:
                    continue
                self.key_factor[element[0]] = 1 if element[1] == '#' else -1

    def add_note(self, note_info: str, oct_modifier: int, duration: float, time: float):
        note = get_note(note_info, self.base_octave + oct_modifier)
        if note is not None:
            if note_info[0] in self.key_factor.keys():
                note += self.key_factor[note_info[0]]
            self.midi.addNote(self.track, self.channel, note, time, duration, self.volume)
        else:
            self.midi.addNote(self.track, self.channel, 0, time, duration, 1)

    def make_song(self, s: str):
        txt = s.replace('\n', ' ').replace('\t', ' ')
        txt = txt.replace('[', '[ ').replace('(', '( ')
        txt = txt.replace(')', ' )').replace(']', ' ]').split(' ')

        time = 0
        constant_duration = None
        together = False
        together_max_duration = 0
        appog = None
        appog_oct = None

        for element in txt:
            should_continue = True
            if '[' in element:
                constant_duration = DURATION[element[:-1]]
            elif ']' in element:
                constant_duration = None
            elif len(element) == 0:
                pass
            elif element == '(':
                together_max_duration = 0
                together = True
            elif element == ')':
                together = False
                time += together_max_duration
            elif element == 'up':
                self.base_octave += 1
            elif element == 'down':
                self.base_octave -= 1
            elif 'volup_' in element:
                self.volume += int(element.replace('volup_', ''))
                self.volume = min(self.volume, 127)
                print(self.volume)
            elif 'voldown_' in element:
                self.volume -= int(element.replace('voldown_', ''))
                self.volume = max(self.volume, 0)
                print(self.volume)
            else:
                should_continue = False

            if should_continue:
                continue

            info = element.split('_')

            if '~' in info[0]:
                appog, info[0] = info[0].split('~')
                appog, appog_oct = get_oct_mod(appog)
            note_info, oct_modifier = get_oct_mod(info[0])

            if note_info not in NOTES.keys():
                raise Exception(f'Invalid note indicator: {note_info}')
            if len(info) > 1 and info[1] not in DURATION.keys():
                raise Exception(f'Invalid duration indicator: {info[1]}')

            duration = DURATION[info[1]] if constant_duration is None else constant_duration

            if appog is not None:
                self.add_note(appog, appog_oct, APPOGGIATURA_DURATION, time)
                self.add_note(note_info, oct_modifier, duration - APPOGGIATURA_DURATION, time + APPOGGIATURA_DURATION)
                appog, appog_oct = None, None
            else:
                self.add_note(note_info, oct_modifier, duration, time)

            if not together:
                time += duration
            else:
                together_max_duration = max(together_max_duration, duration)

    def read_file(self, path: str):
        with open(path, 'r') as file:
            txt = file.read()
        self.read_text(txt)

    def read_text(self, txt: str):
        key_slice = get_slice(txt, 'key')
        if key_slice is not None:
            self.def_key(key_slice)
        self.volume = 100

        title = get_slice(txt, 'title')
        if title is None:
            self.title = 'sample_song'
        else:
            self.title = title.strip().replace(' ', '_')

        bpm_slice = get_slice(txt, 'bpm')
        if bpm_slice is None or len(bpm_slice) == 0:
            self.tempo = 100
        else:
            self.tempo = int(bpm_slice)
            if not (0 < self.tempo < 1000):
                self.tempo = 100
        self.midi.addTempo(self.track, 0, self.tempo)

        song_slice = get_slice(txt, 'song')
        if song_slice is None:
            raise Exception('No song found, maybe you forgot to add song[ ]song')
        while song_slice is not None:
            self.make_song(song_slice)
            txt = txt.replace('song[' + song_slice + ']song', '')
            song_slice = get_slice(txt, 'song')

    def save_song(self, filename: str):
        mid_filename = filename.replace('.mp3', '.mid')
        with open(mid_filename, "wb") as output_file:
            self.midi.writeFile(output_file)
        midi_to_mp3(mid_filename)


if __name__ == '__main__':
    file = 'input/bbb.txt'
    m = Music()
    m.read_file(file)
    m.save_song(file.replace('in', 'out').replace('.txt', '.mp3'))
