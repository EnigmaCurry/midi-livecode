import os
import re
import isobar as ib
import logging

log = logging.getLogger(os.path.basename(__file__))

def molecular_music_box(seed, scale=ib.Scale.major, loops=4, bars=4, beats_per_bar = 4, scale_rule=None, duration_rule=None):
    "The Molecular Music Box - https://youtu.be/3Z8CuAC_-bg"

    ## The Molecular Formula:
    ### Choose a seed:
    ## - Choose a note duration (4)
    ## - Choose a starting note pitch (E)
    ## - Choose another note duration (3)
    ### Seed example string: "4E3"
    ## - Start a live-looper for 4 bars
    ## - Play the first note for the first duration
    ## - Follow the rule for the subsequent notes:
    ##    After the last note has finished, play another note for the same
    ##    duration, but on one note higher in scale, unless the new note is played at
    ##    the same time in the loop as any previous note, in which case, change
    ##    the duration of the new note to the other chosen duration.

    m = re.match("([0-9]*[.]?[0-9]+)([A-Ga-g][#]?)([0-9]*[.]?[0-9]+)", seed)
    dur1, key, dur2 = m.groups()
    dur1 = float(dur1) if float(dur1) - int(float(dur1)) > 0 else int(dur1)
    dur2 = float(dur2) if float(dur2) - int(float(dur2)) > 0 else int(dur2)

    times = {}
    beats = 0

    log.info("Key: {key} {scale}".format(key=key, scale=scale.name))
    transpose = ib.Note.names.index(key)
    scale_index = 0

    if scale_rule is None:
        def scale_rule(scale_index, mod_time, times, swapped, n_loop_notes):
            return scale_index + 1

    if duration_rule is None:
        def duration_rule(mod_time, times, last_duration, swap_duration):
            if mod_time in times:
                return (swap_duration, last_duration, True)
            else:
                return (last_duration, swap_duration, False)

    note_loops = []

    duration = dur1
    swap_duration = dur2
    last_note = None
    loop_beats = bars * beats_per_bar
    for loop in range(loops):
        note_loop = []
        n_loop_notes = 0
        while beats < loop_beats*(loop+1):
            mod_time = beats % loop_beats
            duration, swap_duration, swapped = duration_rule(mod_time=mod_time,
                                                              times=times, last_duration=duration, swap_duration=swap_duration)
            log.info("duration:{} swapped:{}".format(duration, swapped))
            if last_note is None:
                note = last_note = 0 + transpose
            else:
                scale_index = scale_rule(scale_index=scale.indexOf(last_note),
                                         mod_time=mod_time, times=times, swapped=swapped, n_loop_notes=n_loop_notes)
                note = last_note = scale.get(scale_index) + transpose
            # Create one-note loop with rest:
            time_left = loop_beats - duration
            note_loop.append({'note':(note, None), 'dur':(duration, time_left), 'delay': beats})
            n_loop_notes += 1
            beats += duration
            times[mod_time] = times.get(mod_time, 0) + 1
        note_loops.append(note_loop)
    return note_loops
