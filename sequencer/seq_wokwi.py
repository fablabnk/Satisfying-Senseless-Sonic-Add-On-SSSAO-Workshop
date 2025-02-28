from machine import Pin
import utime

# SAO select LEDs
sao1_P1_led = Pin(7, Pin.OUT)
sao2_P1_led = Pin(5, Pin.OUT)
sao3_P1_led = Pin(3, Pin.OUT)
sao4_P1_led = Pin(22, Pin.OUT)
sao5_P1_led = Pin(20, Pin.OUT)
sao6_P1_led = Pin(18, Pin.OUT)

# GPIO Gate LEDs
sao1_P2_led = Pin(6, Pin.OUT)
sao2_P2_led = Pin(4, Pin.OUT)
sao3_P2_led = Pin(2, Pin.OUT)
sao4_P2_led = Pin(21, Pin.OUT)
sao5_P2_led = Pin(19, Pin.OUT)
sao6_P2_led = Pin(17, Pin.OUT)

# Buttons
button_channel = Pin(8, Pin.IN, Pin.PULL_DOWN)
button_tempo = Pin(28, Pin.IN, Pin.PULL_DOWN)

# Create a list of LED objects
leds = [sao1_P1_led, sao2_P1_led, sao3_P1_led, sao4_P1_led, sao5_P1_led, sao6_P1_led]

# Variables for LED selection and tempo
current_led = 0
bpm = 120
led_on_time_ms = 50
last_press_time = 0
debounce_time = 50  # Debounce time in milliseconds

# Variables for non-blocking LED control
led_state = False
last_blink_time = 0
last_tempo_button_state = False
last_channel_button_state = False

# Turn off all LEDs initially
for led in leds:
    led.off()

# Turn on the first LED
leds[current_led].on()

def update_bpm():
    global last_press_time, bpm
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) > debounce_time:
        if last_press_time != 0:
            interval = utime.ticks_diff(current_time, last_press_time)
            new_bpm = int(60000 / interval)
            bpm = min(max(new_bpm, 30), 300)  # Limit BPM between 30 and 300
            print(f"New BPM: {bpm}")
        last_press_time = current_time

def update_led():
    global led_state, last_blink_time
    current_time = utime.ticks_ms()
    period_ms = 60000 / bpm
    
    if led_state and utime.ticks_diff(current_time, last_blink_time) >= led_on_time_ms:
        leds[current_led].off()
        led_state = False
    elif not led_state and utime.ticks_diff(current_time, last_blink_time) >= period_ms:
        leds[current_led].on()
        led_state = True
        last_blink_time = current_time

def change_channel():
    global current_led
    leds[current_led].off()
    current_led = (current_led + 1) % len(leds)
    leds[current_led].on()
    utime.sleep_ms(20)  # Flash for 20ms
    leds[current_led].off()
    print(f"Channel changed to LED {current_led + 1}")

while True:
    current_tempo_button_state = button_tempo.value()
    if current_tempo_button_state and not last_tempo_button_state:
        update_bpm()
    last_tempo_button_state = current_tempo_button_state
    
    current_channel_button_state = button_channel.value()
    if current_channel_button_state and not last_channel_button_state:
        change_channel()
    last_channel_button_state = current_channel_button_state
    
    update_led()
    utime.sleep_ms(1)  # Small delay to prevent excessive CPU usage


from machine import Pin
import utime


# Variables for LED selection and tempo
current_led = 0
bpm = 120
led_on_time_ms = 50
last_press_time = 0
debounce_time = 50  # Debounce time in milliseconds

# Variables for non-blocking LED control
led_state = False
last_blink_time = 0
last_tempo_button_state = False
last_channel_button_state = False
last_channel_change_time = 0
channel_debounce_time = 300  # Longer debounce time for channel button (in milliseconds)

# [Keep the LED initialization code the same]

# [Keep update_bpm() and update_led() functions the same]

def change_channel():
    global current_led, last_channel_change_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_channel_change_time) > channel_debounce_time:
        leds[current_led].off()
        current_led = (current_led + 1) % len(leds)
        leds[current_led].on()
        utime.sleep_ms(20)  # Flash for 20ms
        leds[current_led].off()
        print(f"Channel changed to LED {current_led + 1}")
        last_channel_change_time = current_time

while True:
    current_tempo_button_state = button_tempo.value()
    if current_tempo_button_state and not last_tempo_button_state:
        update_bpm()
    last_tempo_button_state = current_tempo_button_state
    
    current_channel_button_state = button_channel.value()
    if current_channel_button_state and not last_channel_button_state:
        change_channel()
    last_channel_button_state = current_channel_button_state
    
    update_led()
    utime.sleep_ms(1)  # Small delay to prevent excessive CPU usage
