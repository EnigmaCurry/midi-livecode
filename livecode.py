#!/usr/bin/env python

import os
import re
import logging
logging.basicConfig(level=logging.INFO)

import isobar as ib
import rtmidi
import mido
import timelines
import watchgod

midi_in_port = "01. Internal MIDI"
midi_out_port = "02. Internal MIDI"

log = logging.getLogger(os.path.basename(__file__))

def get_midi_output():
    ports = mido.get_output_names()
    for p in ports:
        if re.match(midi_out_port, p):
            port = mido.open_output(p, autoreset=True)
            port.close()
            out = ib.io.midi.MidiOut(target=p)
            return out
    else:
        raise RuntimeError("Midi out port not found")

def midi_reset(port=None):
    if port is None:
        port = get_midi_output()
    else:
        port.reset()

def create_timeline(bpm=120, output=None):
    if output is None:
        output = get_midi_output()
    return ib.Timeline(bpm, output)

if __name__ == "__main__":
    #live coding devloop:
    try:
        watchgod.run_process(os.curdir, timelines.main, args=())
    finally:
        midi_reset()
