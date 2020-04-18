import os
import logging
log = logging.getLogger(os.path.basename(__file__))

import isobar as ib
from livecode import create_timeline
import sequences

def main():
    "Main timeline - Call your timeline here"
    #phases()
    #euclidean()
    #rhythm_phase()

    # custom rule for molecular music box::
    def scale_rule(scale_index, mod_time, times, swapped):
        if swapped:
            if times.get(mod_time, 0) % 2 == 0:
                return scale_index + 2
            else:
                return scale_index - 1
        else:
            return scale_index + 1
    molecular_music_box("9A#5", loops=8, bars=4, octave=3, scale=ib.Scale.dorian, bpm=250, delay=True, scale_rule=scale_rule)

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

def molecular_music_box(seed="4E3", loops=4, bars=4, scale=ib.Scale.major, octave=3, bpm=120, delay=True, scale_rule=None):
    timeline = create_timeline(bpm)
    loop_notes, loop_durations = sequences.molecular_music_box(seed, loops=loops, scale=scale, scale_rule=scale_rule)
    d = 0
    for i in range(len(loop_notes)):
        timeline.sched({ 'note': loop_notes[i] + octave*12, 'dur': loop_durations[i]}, delay=d)
        if delay:
            d += (4 * bars)
    timeline.run()
