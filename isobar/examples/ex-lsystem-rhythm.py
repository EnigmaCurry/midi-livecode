#!/usr/bin/env python

#------------------------------------------------------------------------
# isobar: ex-lsystem-rhythm
#
# Generates a rhythm line based on an L-system sprouting structure,
# sending output over MIDI.
#------------------------------------------------------------------------

from isobar import *
from isobar.io.midi import *

import logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

import random
import time

#------------------------------------------------------------------------
# Generate a set of pitches based on an l-system, with recursive depth 4.
# symbols:
#  N = generate note node
#  + = transpose up one semitone
#  - = transpose down one semitone
#  [ = enter recursive branch
#  ] = leave recursive branch
#------------------------------------------------------------------------
notes = PLSys("N+[+N+N--N+N]+N[++N]", depth = 4)
notes = notes + 60

#------------------------------------------------------------------------
# use another l-system to generate time intervals.
# take absolute values so that intervals are always positive.
#------------------------------------------------------------------------
times = PLSys("[N+[NN]-N+N]+N-N+N", depth = 3)
times = PAbs(PDiff(times)) * 0.25

#------------------------------------------------------------------------
# ...and another l-system for amplitudes.
#------------------------------------------------------------------------
velocity = (PLSys("N+N[++N+N--N]-N[--N+N]") + PWhite(-4, 4)) * 8
velocity = PAbs(velocity)

timeline = Timeline(120)
timeline.sched({ 'note' : notes, 'amp' : velocity, 'dur' : times })
timeline.run()
