import os
import re
import isobar as ib
import logging

log = logging.getLogger(os.path.basename(__file__))

def molecular_music_box(seed, scale=ib.Scale.major, loops=4, bars=4, beats_per_bar = 4, scale_rule=None):
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

    loop_notes = []
    loop_durations = []
    times = {}
    beats = 0

    log.info("Key: {key} {scale}".format(key=key, scale=scale.name))
    transpose = ib.Note.names.index(key)
    scale_index = 0

    if scale_rule is None:
        def scale_rule(scale_index, mod_time, times, swapped):
            return scale_index + 1

    for loop in range(loops):
        log.info("loop: {}".format(loop))
        if loop == 0:
            loop_notes.append([scale.get(scale_index) + transpose])
            notes = loop_notes[0]
            last_note = notes[0]
            loop_durations.append([dur1])
            durations = loop_durations[0]
            log.info("beats:{beats} note:{note} name:{name} dur:{dur}".format(
                beats=beats, note=last_note, name=ib.Note.names[last_note % 12], dur=dur1))
            last_duration = dur1
            swap_duration = dur2
            beats += dur1
            times[0] = 1
        else:
            notes = []
            loop_notes.append(notes)
            durations = []
            loop_durations.append(durations)
        beats_per_loop = beats_per_bar * bars
        while beats < beats_per_loop * (loop+1):
            mod_time = beats % (bars * beats_per_bar)
            if mod_time in times:
                dur = swap_duration
                swapped = True
                last_duration, swap_duration = swap_duration, last_duration
            else:
                swapped = False
                dur = last_duration
            if not len(notes) and beats % beats_per_loop != 0:
                # insert rest
                notes.append(None)
                durations.append(beats % beats_per_loop)
            scale_index = scale_rule(scale_index, mod_time, times, swapped)
            log.info(scale_index)
            last_note = scale.get(scale_index) + transpose
            notes.append(last_note)
            log.info("beats:{beats} note:{note} name:{name} dur:{dur} mod_time:{mod_time} swapped:{swapped}".format(
                beats=beats, note=last_note, name=ib.Note.names[last_note % 12], dur=dur, mod_time=mod_time, swapped=swapped))
            durations.append(dur)
            beats += dur
            times[mod_time] = times.get(mod_time, 0) + 1
    log.info(loop_notes)
    log.info(loop_durations)

    for i in range(len(loop_notes)):
        loop_notes[i] = ib.PSeq(loop_notes[i])
        loop_durations[i] = ib.PSeq(loop_durations[i])
    return (loop_notes, loop_durations)
