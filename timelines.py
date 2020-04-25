import os, sys
import time
import logging
log = logging.getLogger(os.path.basename(__file__))

import isobar as ib
from isobar.io.midifile import MidiFileOut
from livecode import create_timeline, get_midi_output
import sequences
import LinkToPy

def main(timeline):
    "main timeline goes here"
    # molecular_music_box( timeline, "4E10", loops=18, bars=4,
    #                      octave=2, length_multiplier=1, delay=True, channels=1,
    #                      scale=ib.Scale.major, amp=64)

    rhythm_phase(timeline)

def rhythm_phase(timeline):
    melody = ib.PSeq([ -7, -5, 0, 2, 3, -5, -7, 2, 0, -5, 3, 2 ])
    rhythm = ib.PSeq([ 2, 2, 4, 1, 1 ])
    timeline.sched({ 'note': melody + 84, 'dur': rhythm * 0.25 })

def molecular_music_box(timeline, seed="4E3", loops=4, bars=4, scale=ib.Scale.major,
                        octave=3, delay=True, scale_rule=None,
                        duration_rule=None, gate=0.99, channels=1, channel_offset=0,
                        beats_per_bar=4, amp=64, length_multiplier=1):
    note_loops = sequences.molecular_music_box( seed, loops=loops, scale=scale,
                                                scale_rule=scale_rule, duration_rule=duration_rule, bars=bars,
                                                beats_per_bar=beats_per_bar)

    for l in range(len(note_loops)):
        note_loop = note_loops[l]
        for n in range(len(note_loop)):
            loop = note_loop[n]
            d = loop['delay']
            if not delay:
                d = loop['delay'] - (bars * beats_per_bar * l)
            seq = ib.PSeq(loop['note']) + octave*12
            if seq.nextn(1)[0] < 128: # protect against too high midi notes
                timeline.sched({'note': seq, 'dur': ib.PSeq(loop['dur']) * length_multiplier,
                                'gate': gate, 'channel': (l % channels) +
                                channel_offset, 'amp': amp}, delay=d)
