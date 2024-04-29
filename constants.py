MID_OCTAVE = 5


NOTES = {
    'cb': -1,
    'c': 0,
    'c#': 1, 'db': 1,
    'd': 2,
    'd#': 3, 'eb': 3,
    'e': 4, 'fb': 4,
    'e#': 5, 'f': 5,
    'f#': 6, 'gb': 6,
    'g': 7,
    'g#': 8, 'ab': 8,
    'a': 9,
    'a#': 10, 'bb': 10,
    'b': 11,
    'b#': 12,
    'p': None  # means a pause
}

DURATION = {
    'sb': 4,
    'min': 2,
    'smin': 1,
    'col': 1/2,
    'scol': 1/4,
    'fus': 1/8,
    'sfus': 1/16
}

items = list(DURATION.items())

for key, value in items:
    DURATION['q' + key] = 2/3 * value

items = list(DURATION.items())

for key, value in items:
    DURATION[key + '.'] = 3 * value / 2

OCTAVE_MODIFIER = {
    '>': 1,
    '<': -1
}

APPOGGIATURA_DURATION = 1/16