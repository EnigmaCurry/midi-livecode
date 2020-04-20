import os, sys
import logging
log = logging.getLogger(os.path.basename(__file__))

import isobar as ib
from isobar.io.midifile import MidiFileOut
from livecode import create_timeline, midi_reset
import sequences

def main():
    "Main timeline - Call your timeline here"
    #phases()
    #euclidean()
    #rhythm_phase()

    # Create timeline that outputs to a midi file
    #midi_file = MidiFileOut("output.mid")
    #timeline_file = ib.Timeline(250, midi_file)

    # custom rules for molecular music box::
    def scale_rule1(scale_index, mod_time, times, swapped):
        if swapped:
            if times.get(mod_time, 0) % 2 == 0:
                return scale_index + 2
            else:
                return scale_index - 1
        else:
            return scale_index + 1

    timeline = create_timeline(120)
    molecular_music_box("4F5", loops=12, bars=4, octave=3, channels=4,
                        scale=ib.Scale.phrygian, delay=True, gate=0.9,
                        scale_rule=scale_rule1, forever=True, timeline=timeline)

def permute():
    timeline = create_timeline(120)
    timeline.sched({'note': ib.PSeq([0]) + 60, 'dur': 10, 'gate': 0.99})
    timeline.run()

def euclidean():
    timeline = create_timeline(120)

    timeline.sched({ 'note' : 45 * ib.PEuclidean(5, 8), 'dur' : 0.5 })
    timeline.sched({ 'note' : 47 * ib.PEuclidean(5, 13), 'dur' : 0.25 })
    timeline.sched({ 'note' : 50 * ib.PEuclidean(7, 15), 'dur' : 0.5 })

    timeline.run()

def phases():
    timeline = create_timeline(170)

    seq = ib.PSeq([ -7, -5, 0, 2, 3, -5, -7, 2, 0, -5, 3, 2 ])
    timeline.sched({ 'note': seq.copy() + 60, 'dur': 0.5 })
    timeline.sched({ 'note': seq.copy() + 72, 'dur': 0.5 * 1.01 })
    timeline.run()

def rhythm_phase():
    timeline = create_timeline(100)
    melody = ib.PSeq([ -7, -5, 0, 2, 3, -5, -7, 2, 0, -5, 3, 2 ])
    rhythm = ib.PSeq([ 2, 2, 4, 1, 1 ])
    timeline.sched({ 'note': melody + 84, 'dur': rhythm * 0.25 })
    timeline.run()

def molecular_music_box(seed="4E3", loops=4, bars=4, forever=False, scale=ib.Scale.major,
                        octave=3, delay=True, scale_rule=None,
                        gate=0.99, channels=1, timeline=None):
    if timeline is None:
        timeline = create_timeline(120)
    loop_notes, loop_durations = sequences.molecular_music_box(
        seed, loops=loops, scale=scale, scale_rule=scale_rule)
    kwargs = {'delay': 0}

    for i in range(len(loop_notes)):
        timeline.sched({ 'note': ib.PLoop(loop_notes[i] + octave*12, ), 'dur':
                         loop_durations[i], 'gate': gate, 'channel': i %
                         channels}, **kwargs)
        if delay:
            kwargs['delay'] += (4 * bars)
    timeline.run(stop_when_done=False)
