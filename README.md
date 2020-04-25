# midi-livecode

This is a live-coding environment for MIDI composition with support for Ableton Link.

 * Install a MIDI loop driver 
   * Windows: https://www.nerds.de/en/loopbe1.html 
   * Mac: Create an [IAC bus using "Audio MIDI
     Setup"](https://help.ableton.com/hc/en-us/articles/209774225-How-to-setup-a-virtual-MIDI-bus)
 * Set your DAW to listen to the MIDI loop
 * [Download the latest version of Python](https://www.python.org/downloads/)
 * Clone or download this repository
 * Run these commands to install:
     * `python -m venv env`
     * On Windows: `.\env\Scripts\activate`
     * On Linux / Mac: `source env/bin/activate`
     * (Note: you will need to re-activate each time you open your terminal)
     * `pip install -r requirements.txt`
 * Put timelines in `timelines.py`
 * Put sequences in `sequences.py`
 * Change settings at the top of `livecode.py`:
   * `midi_in_port` - the name of your MIDI loop input.
   * `midi_out_port` - the name of your MIDI loop output.
   * `live_reload` - True/False, whether to automatically reload the program when the source is changed.
   * `use_ableton_link` - True/False, whether to enable Ableton Link support.
   * `carabiner_path` - For Ableton Link support, download the latest release of
     [Carabiner](https://github.com/Deep-Symmetry/carabiner/releases) and place
     `Carabiner.exe` in the same directory. Update `carabiner_path` if the name
     or location differs on your system.
   * `default_bpm` - The beats per minute to use if *not* using Ableton Link.
   * `nudge_time` - Start playback earlier than otherwise, to correct for
     constant-time delay (seconds).
 * Run `python livecode.py` and it will autoreload on save

## Isobar

Isobar is forked from https://github.com/ideoforms/isobar and several
modifications are made herein. [Please follow the isobar LICENSE
terms](isobar/LICENSE.md)

## Live reload

When changes are detected in the source files, the program automatically
restarts. This may be different than other live-coding environments you may be
familiar with, that are built to introduce changes to the music without
restarting. My use-case is for composition, not live concerts, so restarting
makes sense for me.

## Ableton Link

Ableton Link is optional, and will sync the transport play/stop/rec button of
your DAW or other connected apps, to your main timeline start/stop. Ableton Link
is not Ableton Live specific, and any app can use this protocol for
synchronization. If your DAW has no support for Ableton Link, or if you wish to
turn this off, set `use_ableton_link = False` in livecode.py, and the program
will just output midi immediately (regardless of your current DAW transport
state).

When Ableton Link is enabled, the bpm of your timeline is automatically set to
the one in your connected DAW or other app. **This only works when the timeline
is stopped.** There is currently no support to change the bpm once playback has
started. Furthermore, there is no accounting for timing drift (this is not
expected to happen with a midi loopback.) To correct for constant-time delay,
set `nudge_time`.
