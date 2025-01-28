from machine import Pin
import time

# Sequencer setup
channels = 6
steps = 16
bpm = 120
current_step = 0
current_channel = 0
pattern = [[0 for _ in range(steps)] for _ in range(channels)]
last_tap_time = 0

# GPIO setup
led_pins = [2, 6, 7, 22, 20, 18]  # Specific GPIO pins for channel LEDs
leds = [Pin(pin, Pin.OUT) for pin in led_pins]
metronome_led = Pin(10, Pin.OUT)  # Metronome LED on GP10 (pin 14)
buttons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(11, 14)]  # Buttons on GP11-13 (pins 15-17)

def next_channel():
    global current_channel
    current_channel = (current_channel + 1) % channels

def toggle_step():
    pattern[current_channel][current_step] = 1 - pattern[current_channel][current_step]

def clear_channel():
    pattern[current_channel] = [0 for _ in range(steps)]

def tap_tempo():
    global last_tap_time, bpm
    current_time = time.ticks_ms()
    
    if last_tap_time != 0:
        interval = time.ticks_diff(current_time, last_tap_time)
        if interval > 2000:  # If more than 2 seconds have passed, start over
            last_tap_time = current_time
            return
        
        new_bpm = int(60000 / interval)  # Calculate BPM based on time between taps
        bpm = new_bpm
    
    last_tap_time = current_time

def update_leds():
    for i, led in enumerate(leds):
        led.value(pattern[i][current_step])

def handle_button_presses():
    shift = not buttons[0].value()  # Button 1 acts as shift key
    
    if not buttons[1].value():  # Button 2
        if shift:
            tap_tempo()
        else:
            next_channel()
    
    if not buttons[2].value():  # Button 3
        if shift:
            clear_channel()
        else:
            toggle_step()

def main():
    global current_step
    metronome_counter = 0
    
    while True:
        start_time = time.ticks_ms()
        
        update_leds()
        handle_button_presses()
        
        # Metronome LED logic
        if metronome_counter == 0:
            metronome_led.on()
        elif metronome_counter == 1:
            metronome_led.off()
        
        while time.ticks_diff(time.ticks_ms(), start_time) < 60000 / (bpm * 4):
            handle_button_presses()
        
        current_step = (current_step + 1) % steps
        metronome_counter = (metronome_counter + 1) % 4

if __name__ == "__main__":
    main()

