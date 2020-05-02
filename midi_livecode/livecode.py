#!/usr/bin/env python

import os
import time
import re
import threading
import click
import logging
logging.basicConfig(level=logging.INFO)

import isobar as ib
import mido
from . import LinkToPy
import watchgod

## Settings:
midi_in_port = "01. Internal MIDI"
midi_out_port = "02. Internal MIDI"
live_reload = True
use_ableton_link = True
default_bpm = 120 # BPM to use when not using ableton link
carabiner_path = "Carabiner.exe"
nudge_time = 0.03

log = logging.getLogger(os.path.basename(__file__))
logging.getLogger("edn_format").setLevel(logging.WARN)
logging.getLogger("isobar.io.midi").setLevel(logging.WARN)

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

def create_timeline(output, bpm=120, reset=True):
    log.info("New timeline: bpm={bpm}".format(bpm=bpm))
    if reset:
        for ch in range(16):
            output.all_notes_off(ch)
    return ib.Timeline(bpm, output)

def timeline_main(out=None, use_ableton_link=False, timeline_func=None, timeline_args={}):
    from . import timelines
    try:
        timeline_func = getattr(timelines, timeline_func)
    except TypeError:
        timeline_func = timelines.main
    if out is None:
        output = get_midi_output()
        reset = True
    else:
        output = ib.io.midifile.MidiFileOut(out)
        use_ableton_link = False
        reset = False

    if use_ableton_link:
        ableton_link = LinkToPy.LinkInterface()
        timeline = create_timeline(output, ableton_link.bpm_, reset)
        timelines.main(timeline)

        ableton_link.status(callback=lambda msg_data: print(msg_data))
        def ableton_transport_stop(msg_data):
            nonlocal timeline
            print(msg_data)
            playing = msg_data.get("playing", False)
            if playing and not timeline.started:
                beat_time = (60 / msg_data['bpm'])
                delay_time = (4*beat_time) - (beat_time * (msg_data['beat'] % 4)) - nudge_time
                if delay_time > 0:
                    time.sleep(delay_time)
                timeline.background()
            elif not playing and timeline.started:
                timeline.stop()
                timeline = create_timeline(output, ableton_link.bpm_, reset)
                timelines.main(timeline)
            elif not playing:
                # Updates timeline bpm if changed when not playing:
                timeline = create_timeline(output, ableton_link.bpm_, reset)
                timeline_func(timeline, **timeline_args)

        ableton_link.status(callback=ableton_transport_stop)
        try:
            ableton_link.thread.join()
        except KeyboardInterrupt:
            log.info("Keyboard interrupt!")
    else:
        timeline = create_timeline(output, bpm=999, reset=reset)
        timeline_func(timeline, **timeline_args)
        try:
            log.info("Recording midi file in real-time, please wait, or press Ctrl-C to stop.")
            log.info(f"Running timeline:{timeline_func.__name__}")
            timeline.run()
            print("done")
        except KeyboardInterrupt:
            log.info("Keyboard interrupt!")
        finally:
            if out is not None:
                output.write()
                log.info(f"midi file written: {out}")

class CodeWatcher(watchgod.DefaultWatcher):
    def should_watch_file(self, entry):
        return entry.name.endswith(('.py', '.pyx', '.pyd')) and not entry.name.startswith(".")

def main(out=None, ableton_link=False, live_reload=False, timeline=None, timeline_args={}):
    #live coding devloop:
    if ableton_link:
        carabiner_thread = threading.Thread(target=lambda : os.system(carabiner_path + " > carabiner.log"))
        carabiner_thread.start()
    if type(out) == str:
        out = open(out,"wb")
    args = (out, ableton_link, timeline, timeline_args)
    if live_reload:
        import rtmidi
        watchgod.run_process(os.curdir, timeline_main, args=args, watcher_cls=CodeWatcher)
    else:
        timeline_main(*args)

@click.command()
@click.option('--out', default=None, help="name of midi file to output")
@click.option('--ableton-link/--no-ableton-link', default=use_ableton_link)
@click.option('--live-reload/--no-live-reload', default=live_reload)
@click.option('--timeline', default=None)
def command(out, ableton_link, live_reload, timeline):
    main(out=out, ableton_link=ableton_link, live_reload=live_reload, timeline=timeline)

if __name__ == "__main__":
    command()
