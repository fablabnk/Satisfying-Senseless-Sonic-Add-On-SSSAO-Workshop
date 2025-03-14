# REMEMBER THAT: LEDs are ACTIVE LOW, so led_metro_pins[current_channel].off() means ON and vice versa
# LEDs will light when first connected and only stop lighting when channel select chooses them

import uasyncio as asyncio
from machine import Pin
import time

# Initialize pins

button_shift = Pin(8, Pin.IN, Pin.PULL_UP)
button_2 = Pin(9, Pin.IN, Pin.PULL_UP)
button_3 = Pin(28, Pin.IN, Pin.PULL_UP)

led_note_pins = [Pin(6, Pin.OUT), Pin(4, Pin.OUT), Pin(2, Pin.OUT), Pin(21, Pin.OUT), Pin(19, Pin.OUT), Pin(17, Pin.OUT)]
led_metro_pins = [Pin(7, Pin.OUT), Pin(5, Pin.OUT), Pin(3, Pin.OUT), Pin(22, Pin.OUT), Pin(20, Pin.OUT), Pin(18, Pin.OUT)]

bpm = 120
steps_per_bar = 8  # Number of steps per bar
steps_per_beat = steps_per_bar / 4  # Number of steps per beat
num_bars = 2  # Number of bars for the sequence
total_steps = steps_per_bar * num_bars  # Total number of steps in the sequence
channel_select_led_duration = 0.1  # Duration to light the metronome LED when changing channels (in seconds)
hold_time = 2  # Hold time for double/half tempo (in seconds)

# Sequencer state
channels = 6
steps = [[1 if i % steps_per_beat == 0 else 0 for i in range(total_steps)] for _ in range(channels)]  # Initialize steps array
current_step = 0
current_channel = 0

for channel in range(channels):
    led_metro_pins[channel].on()
    led_note_pins[channel].on()

async def metronome():
    global current_step, bpm, interval
    while True:
        interval = 60 / bpm / steps_per_beat  # Interval for each step (dynamic BPM, 4 steps per beat)
        if current_step % steps_per_beat == 0:  # Light UP the LED every 4 steps (1 beat)
            led_metro_pins[current_channel].off()
            await asyncio.sleep(interval)
            led_metro_pins[current_channel].on()
        else:
            await asyncio.sleep(interval)  # Wait for the full interval if not a beat
        current_step = (current_step + 1) % total_steps

async def note_display():
    while True:
        for channel in range(channels):
            if steps[channel][current_step] == 1:
                led_note_pins[channel].off()
            else:
                led_note_pins[channel].on()
        await asyncio.sleep(0.01)  # Check the note status frequently

async def record_note():
    while True:
        if button_3.value() == 0 and button_shift.value() == 1:
            steps[current_channel][current_step] = 1
        await asyncio.sleep(0.01)  # Check the button status frequently

async def clear_notes():
    global steps
    button_was_pressed = False
    while True:
        if button_3.value() == 0 and button_shift.value() == 0:
            if not button_was_pressed:
                steps[current_channel] = [0] * total_steps
                button_was_pressed = True
            await asyncio.sleep(0.5)  # Debounce
        else:
            button_was_pressed = False
        await asyncio.sleep(0.01)  # Check the button status frequently

async def tap_tempo():
    global bpm
    last_press = time.ticks_ms()
    button_was_pressed = False
    while True:
        if button_2.value() == 0 and button_shift.value() == 0:
            if not button_was_pressed:
                now = time.ticks_ms()
                tap_interval = now - last_press
                if tap_interval > 0:
                    new_bpm = 60000 / tap_interval
                    if 40 <= new_bpm <= 240:
                        bpm = new_bpm
                        print(f"BPM: {bpm}")
                last_press = now
                button_was_pressed = True
            await asyncio.sleep(0.05)  # Shorter debounce
        else:
            button_was_pressed = False
        await asyncio.sleep(0.01)  # Check the button status frequently

async def half_tempo():
    global bpm
    test_bpm = bpm / 2
    if test_bpm < 40 or test_bpm > 240:
        print(f"BPM out of range")
    else:
        bpm = test_bpm
        print(f"Tempo halved: {bpm} BPM")

async def double_tempo():
    global bpm
    test_bpm = bpm * 2
    if test_bpm < 40 or test_bpm > 240:
        print(f"BPM out of range")
    else:
        bpm = test_bpm
        print(f"Tempo doubled: {bpm} BPM")

async def select_channel():
    global current_channel
    button_was_pressed = False
    button_held = False
    hold_start = 0
    while True:
        if button_2.value() == 0 and button_shift.value() == 1:
            if not button_was_pressed:
                hold_start = time.ticks_ms()
                button_was_pressed = True
            elif time.ticks_diff(time.ticks_ms(), hold_start) >= hold_time * 1000 and not button_held:
                button_held = True
                await half_tempo()
        elif button_2.value() == 1 and button_was_pressed:
            if not button_held:
                led_metro_pins[current_channel].on()  # Turn off the current channel's metronome LED
                current_channel = (current_channel + 1) % channels
                led_metro_pins[current_channel].off()  # Light the new channel's metronome LED
                await asyncio.sleep(interval)  # Keep it on for the specified duration
                led_metro_pins[current_channel].on()
            button_was_pressed = False
            button_held = False
        await asyncio.sleep(0.01)  # Check the button status frequently

async def tap_tempo_or_double_tempo():
    global bpm
    button_was_pressed = False
    button_held = False
    hold_start = 0
    last_press = time.ticks_ms()
    while True:
        if button_2.value() == 0 and button_shift.value() == 0:
            if not button_was_pressed:
                hold_start = time.ticks_ms()
                button_was_pressed = True
            elif time.ticks_diff(time.ticks_ms(), hold_start) >= hold_time * 1000 and not button_held:
                button_held = True
                await double_tempo()
        elif button_2.value() == 1 and button_was_pressed:
            if not button_held:
                now = time.ticks_ms()
                interval = now - last_press
                if interval > 0:
                    new_bpm = 60000 / interval
                    if 40 <= new_bpm <= 240:
                        bpm = new_bpm
                        print(f"BPM: {bpm}")
                last_press = now
            button_was_pressed = False
            button_held = False
        await asyncio.sleep(0.01)  # Check the button status frequently

async def main():
    await asyncio.gather(metronome(), select_channel(), note_display(), record_note(), clear_notes(), tap_tempo_or_double_tempo())

# Run the event loop
asyncio.run(main())