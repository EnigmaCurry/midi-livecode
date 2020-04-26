import isobar as ib
import re

names = [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ]
flat_names = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B" ]

def note_value(name):
    if re.match("[A-Ga-g](#b)?", name):
        name = name[0].upper() + name[1:]
        try:
            if name.endswith("b"):
                return flat_names.index(name)
            else:
                return names.index(name)
        except ValueError:
            raise ValueError(f"{name} is not a valid note name")
    else:
        raise ValueError(f"Could not parse note name: {name}")
