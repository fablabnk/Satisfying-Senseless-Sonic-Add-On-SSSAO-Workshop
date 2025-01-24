# What would be involved to sequence up to 6 badges over I2C?

Check if SAO addresses exist i.e.

0x00 Kick drum
0x01 Hi Hat
0x02 Snare
0x03 Tamborine
0x04 Kalimba
0x05 TomTom

How do we know their position? Does it matter?

# What are we trying to activate

Send a 'gate pulse' with viable duty cycle
High means on, low means off
For this we only need a GPIO, nothing more
So do we need I2C at all here? Maybe we don't 
- For SAO slot 1, we configure P1 (pin 10, GP7) as output
- We send sequence pulses to it
- CH32V003 receives them on a digital input pin. This would be the equivalent to pressing the button on the analog circuit

# Three buttons sequencer:

LED on proto petal lights to represent the gate
How many bars? 1
How to show current tempo?
1. Add a master LED on main badge
2. 

Button 1: Pin 11 / GP8
shift - hold to active shift function
DOUBLE TAP - switch between free running and 32 step quantise. Shown where?

Button 2: Pin 12 / GP9
tap tempo - timing between two taps of the button will set the tempo (space between beats)
SELECT - selects the next clockwise available SAO. LED will be solidly lit for 2 seconds

Button 3: Pin 34 / GP28
record - tap to overdub. Gate length is also recorded.
CLEAR - clear the pattern for the selected SAO

# Sequencing in MicroPython

# How do the other SAO's register/communicate over I2C?

# CH32V003 as I2C Slave

https://github.com/cnlohr/ch32v003fun/tree/master/examples/i2c_slave

# Micropython Sequencer Code Example:

```
from machine import Pin
import utime

# Define your GPIO pins
pins = [Pin(i, Pin.OUT) for i in range(8)]  # Adjust range as needed

# Define your patterns (0 for low, 1 for high)

patterns = [
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    # Add more patterns as needed
]

def play_pattern(pattern, step_time):
    for step in pattern:
        start_time = utime.ticks_us()
        for pin, value in zip(pins, step):
            pin.value(value)
        
        # Calculate remaining time and sleep
        elapsed = utime.ticks_diff(utime.ticks_us(), start_time)
        if elapsed < step_time:
            utime.sleep_us(step_time - elapsed)

step_time = 125000  # 125ms per step, adjust as needed

while True:
    for pattern in patterns:
        play_pattern(pattern, step_time)
```

# How does mutable grids work?