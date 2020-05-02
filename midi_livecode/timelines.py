import os, sys
import time
import logging
log = logging.getLogger(os.path.basename(__file__))

import isobar as ib
from isobar.io.midifile import MidiFileOut
from .livecode import create_timeline, get_midi_output
from . import sequences

def main(timeline):
    "Your main timeline goes here"
    def scale_rule_1(scale_index, mod_time, times, swapped, n_loop_notes):
        if not swapped:
            return scale_index + 2
        elif n_loop_notes > 1:
            return scale_index - 2
        else:
            return scale_index

    molecular_music_box(timeline, "14C3", key="C", scale=ib.Scale.dorian,
                        loops=4, bars=8, octave=3, length_multiplier=1,
                        delay=True, channels=1, amp=32, gate=0.9, repeats=4+2)
    #test1(timeline)

def test1(timeline):
    melody = ib.PSeq([ 0, 0, 2, 4, 7, 9, 9, 7, 0, 4, 4, 2, 2, 0, None], repeats=1)
    rhythm = ib.PSeq([ 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 0 ])
    timeline.sched({ 'note': melody + 84, 'dur': rhythm * 0.25, 'gate': 0.9}, delay=0)

def molecular_music_box(timeline, seed="4E3", loops=4, bars=4, key="C", scale=ib.Scale.major,
                        octave=3, delay=True, scale_rule=None,
                        duration_rule=None, gate=0.99, channels=1, channel_offset=0,
                        beats_per_bar=4, amp=64, length_multiplier=1, repeats=sys.maxsize):
    note_loops = sequences.molecular_music_box( seed, loops=loops, scale=scale,
                                                scale_rule=scale_rule, key=key, duration_rule=duration_rule, bars=bars,
                                                beats_per_bar=beats_per_bar)

    print("delay", delay)
    if delay:
        print("length", bars*loops)
    else:
        print("length", bars)
    for l in range(len(note_loops)):
        note_loop = note_loops[l]
        for n in range(len(note_loop)):
            loop = note_loop[n]
            d = loop['delay']
            if not delay:
                d = loop['delay'] - (bars * beats_per_bar * l)
            seq = ib.PSeq(loop['note'], repeats=repeats) + octave*12
            for note in seq:
                if note and note > 127:
                    raise ValueError("These settings create midi notes higher than 128, maybe try fewer bars or loops")
            seq.reset()
            timeline.sched({'note': seq, 'dur': ib.PSeq(loop['dur'], repeats=repeats) * length_multiplier,
                            'gate': gate, 'channel': (l % channels) +
                            channel_offset, 'amp': amp}, delay=d)
