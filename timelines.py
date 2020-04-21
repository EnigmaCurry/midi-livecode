import os, sys
import logging
log = logging.getLogger(os.path.basename(__file__))

import isobar as ib
from isobar.io.midifile import MidiFileOut
from livecode import create_timeline, midi_reset
import sequences

def main():
    "Main timeline - Call your timeline here"
    #rhythm_phase()

    # Create timeline that outputs to a midi file
    #midi_file = MidiFileOut("output.mid")
    #timeline_file = ib.Timeline(250, midi_file)

    # custom rules for molecular music box::
    def scale_rule1(scale_index, mod_time, times, swapped, n_loop_notes):
        if swapped:
            if times.get(mod_time, 0) % 3 == 0:
                return scale_index + 2
            else:
                return scale_index - 1
        else:
            if n_loop_notes % 2 == 0:
                return scale_index + 1
            else:
                return scale_index - 4

    timeline = create_timeline(240)
    molecular_music_box("4E9", loops=18, bars=4, octave=3, delay=True,
                        channels=4, scale=ib.Scale.dorian, timeline=timeline, scale_rule=scale_rule1)

def rhythm_phase():
    timeline = create_timeline(100)
    melody = ib.PSeq([ -7, -5, 0, 2, 3, -5, -7, 2, 0, -5, 3, 2 ])
    rhythm = ib.PSeq([ 2, 2, 4, 1, 1 ])
    timeline.sched({ 'note': melody + 84, 'dur': rhythm * 0.25 })
    timeline.run()

def molecular_music_box(seed="4E3", loops=4, bars=4, scale=ib.Scale.major,
                        octave=3, delay=True, scale_rule=None,
                        duration_rule=None, gate=0.99, channels=1,
                        timeline=None, beats_per_bar=4):
    if timeline is None:
        timeline = create_timeline(120)
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
            seq = ib.PSeq(loop['note'])  + octave*12
            if seq.nextn(1)[0] < 128: # protect against too high midi notes
                timeline.sched({'note': seq, 'dur':
                                ib.PSeq(loop['dur']), 'gate': gate, 'channel': l %
                                channels}, delay=d)

    timeline.run()

