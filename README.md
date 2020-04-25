# midi-livecode

This is a live-coding environment for MIDI composition.

 * Install a MIDI loop driver - https://www.nerds.de/en/loopbe1.html
 * Set your DAW to listen to the MIDI loop
 * Create virtualenv and Install deps in requirements.txt
 * Put timelines in `timelines.py`
 * Put sequences in `sequences.py`
 * Change settings at the top of `livecode.py`:
   * `midi_in_port` - the name of your MIDI loop input.
   * `midi_out_port` - the name of your MIDI loop output.
   * `live_reload` - True/False whether to automatically reload the program when the source is changed.
   * `use_ableton_link` - True/False whether to enable Ableton Link support.
   * `carabiner_path` - For Ableton Link support, download the latest release of
     [Carabiner](https://github.com/Deep-Symmetry/carabiner/releases) and place
     `Carabiner.exe` in the same directory. Update `carabiner_path` if the name
     or location differs on your system.
   * `default_bpm` - The beats per minute to use if *not* using Ableton Link.
 * Run `livecode.py` and it will autoreload on save
