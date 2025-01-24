Write me a Python script for a 6-channel 16-step sequencer, which has no sound output. The code will eventually run on a Raspberry Pi Pico running Micropython and will address 6 GPIO output pins, but for now will just produce ASCII graphical output, of the form:

 12345678ABCDEFGH
1x---x---x---x---
2x-x-x-x-x-x-x-x-
3--x---x---x---x-
4x---------------
5-x-x----x-x-x-x-
6x--x--x--x--x--x

Here the top line represents the 16 steps and each of the six subsequent lines represents a drum channel. On each channel an 'x' means the step is playing and a '-' means the step is silent.

The currently playing step should be shown on the top line by inverting the corresponding character i.e an inverted '1' means we're on the first step and an inverted 'A' means we're on the 9th step

The currently chosen drum channel should be shown by inverting the first character of one of the six subsequent lines.

When the program starts:
1. The sequencer should start running at 120BPM
2. Drum channel 1 should be selected by default

The sequencer is controlled with the 'a' 's' and 'd' keys. When the 'a' is key is held it acts as a SHIFT function for the 's' and 'd' keys, so that:
- when the 'a' is not pressed and the 's' key is depressed, the timing between two subsequent presses sets the tempo between quarter notes (i.e. the time between four steps)
- when the 'a' key is depressed and the 's' key is depressed, select the next drum channel (when at channel 6, wrap back to channel 1)
- when the 'a' is not pressed and the 'd' key is depressed, add a 'x' at this step
- when the 'a' key is depressed and the 'd' key is depressed, clear the channel so that all steps are silent ('-')

Do you need any clarifications before getting started on the code?
