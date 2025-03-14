# About the Sequencer

Our main.py sequencer runs on the Raspberry Pi Pico W on your badge and allows you to live-record rhythmic patterns onto up to six Satisfying Senseless Sonic Add On's (SSSAO's) using the three badge buttons (ABC).

By default the sequencer run in a looping two bar pattern, with sixteen steps per bar (but this can be changed in the code).

# How to Upload Sequencer Code to Your Badge

1. First flash the supercon badge image following the process described [here](https://github.com/fablabnk/Satisfying-Senseless-Sonic-Add-On-SSSAO-Workshop/tree/main/badge_image)

2. Now download [Thonny](https://thonny.org/) and open it. We will use it to copy our sequencer main.py over to the Pi Pico W on your badge

3. In the top left file-browser panel of Thonny, navigate to the [/sequencer](https://github.com/fablabnk/Satisfying-Senseless-Sonic-Add-On-SSSAO-Workshop/tree/main/sequencer) folder.

4. Connect your conference badge to your PC using a data-enabled USB cable. You should see the files that are currently on the badge in the bottom left file-browser panel of Thonny. If not, click the STOP button in the Thonny icon bar. 

5. Right click on main.py in the top left panel and select "upload to /" to replace the main.py on your badge shown in the bottom left panel. You may wish to rename the main.py on the badge if you want to switch back to normal functionality later

# Instructions for Use

Once the sequencer code is flashed to the badge, you should plug in at least two sound-making proto-petal SAOs (preferably in badge slots 1 and 2). Be sure to plug them facing outwards!

We control our SSSAO sequencer using the three buttons on the badge (ABC), which allow you to do things such as: 
- select an SSSAO
- record notes to the selected SSSAO
- set the global tempo of all SSSAO's

Note that we currently don't do any badge detection, so all SSSAO's are considered available, even if nothing is plugged in the slot, so any SSSAO's that aren't connected will need to be 'skipped over'.

Each SSSAO has two LEDS: a METRONOME LED and a RECORDED NOTES LED. The METRONOME LED is just for visual reference, whereas the RECORDED NOTES LED is synced to the turning on and off of the sound-making motor attached to the SSSAO. 

On each SSSAO, there is also:
- a push button (for manual playback)
- a potentiometer, which allows you to adjust the motor intensity via PWM (and also shows on the brightness of the RECORDED NOTES LED). Make sure this is turned up when getting started!

On badge-startup all SSSAO's will come on for a few seconds and may sound constantly - this is normal (though we don't know yet why it happens). After this the firmware properly kicks-in and both the METRONOME LED and a RECORDED NOTES LED will blink in a standard 4-to-the-floor pattern. We did this so that you get some instant sonic gratification when connecting the badge. If you don't like the pattern, clear it and record your own (more on which below)

## More About The Badge Buttons

The function of the buttons is as follows:

Button A:
	- simply a SHIFT button

Button B:
	- without SHIFT								SSSAO SELECT: selects the next SSSAO (from 1-6, then looping back to 1)
	- with SHIFT 								TAP TEMPO: two subsquent taps will set the time between two beats (1/4 of a bar)
	- without SHIFT and HELD for 2 seconds		DOUBLE TEMPO (up to max of 240 BPM)
	- with SHIFT and HELD for 2 seconds			HALVE TEMPO (down to min of 40 BPM)

Button C:
	- without SHIFT:							RECORD NOTE: live records a note on the selected SSSAO for as long as held
	- with SHIFT								CLEAR NOTES: clears all notes on the selected SSSAO

## More About The SAO LEDs

Each SSSAO has two LEDs:
	- a SAO SELECT / METRONOME LED (which you soldered on yourself, in the centre of the SSSAO)
	- a NOTES LED (the pre-soldered SMT LED, at the bottom of the SSSAO)

### SSSAO SELECT / METRONOME LED:
	- gives a visual reference for the current tempo
	- only blinks on the currently selected SSSAO
	- blinks momentarily when the SAO SELECT button is pressed, to help you see where you are

### RECORDED NOTES LED:
	- blinks according to the pattern you record using Button C