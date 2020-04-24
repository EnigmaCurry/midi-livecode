#!/usr/bin/env python

import os
import re
import threading
import logging
logging.basicConfig(level=logging.INFO)

import isobar as ib
import rtmidi
import mido
import LinkToPy
import watchgod

midi_in_port = "01. Internal MIDI"
midi_out_port = "02. Internal MIDI"
carabiner_path = "Carabiner.exe"

log = logging.getLogger(os.path.basename(__file__))
logging.getLogger("edn_format").setLevel(logging.WARN)


def get_midi_input():
    ports = mido.get_input_names()
    for p in ports:
        if re.match(midi_in_port, p):
            port = mido.open_input(p, autoreset=True)
            port.close()
            inp = ib.io.midi.MidiIn(target=p)
            return inp
    else:
        raise RuntimeError("Midi in port not found")

def get_midi_output():
    ports = mido.get_output_names()
    for p in ports:
        if re.match(midi_out_port, p):
            # port = mido.open_output(p, autoreset=True)
            # port.close()
            out = ib.io.midi.MidiOut(target=p)
            return out
    else:
        raise RuntimeError("Midi out port not found")

def create_timeline(output, bpm=120):
    for ch in range(16):
        output.all_notes_off(ch)
    return ib.Timeline(bpm, output)


def main():
    #live coding devloop:
    # carabiner_thread = threading.Thread(target=lambda : os.system(carabiner_path + " > carabiner.log"))
    # carabiner_thread.start()
    import timelines
    watchgod.run_process(os.curdir, timelines.main, args=())

if __name__ == "__main__":
    main()
