import time
import sys
import select
import termios
import tty

# Sequencer setup
channels = 6
steps = 16
bpm = 120
current_step = 0
current_channel = 0
pattern = [['-' for _ in range(steps)] for _ in range(channels)]
last_tap_time = 0

def move_cursor(x, y):
    print(f"\033[{y};{x}H", end="")

def display_sequencer():
    move_cursor(1, 1)
    
    step_numbers = ''.join([str(i+1) if i < 9 else chr(ord('A') + i - 9) for i in range(steps)])
    print(' ' + ''.join(['\033[7m' + c + '\033[0m' if i == current_step else c for i, c in enumerate(step_numbers)]))
    
    for i, channel in enumerate(pattern):
        channel_display = ''.join(channel)
        play_state = '\033[7m[x]\033[0m' if pattern[i][current_step] == 'x' else '[-]'
        if i == current_channel:
            print(f'\033[7m{i+1}\033[0m{channel_display} {play_state}')
        else:
            print(f'{i+1}{channel_display} {play_state}')
    
    print(f"BPM: {bpm:<3}\033[K")
    print("Controls: 's' (next channel), 'd' (tap tempo), 'f' (toggle step), 'g' (clear channel), 'q' (quit)")
    
    for _ in range(2):
        print("\033[K")

def toggle_step():
    pattern[current_channel][current_step] = 'x' if pattern[current_channel][current_step] == '-' else '-'

def clear_channel():
    pattern[current_channel] = ['-' for _ in range(steps)]

def next_channel():
    global current_channel
    current_channel = (current_channel + 1) % channels

def tap_tempo():
    global last_tap_time, bpm
    current_time = time.time()
    
    if last_tap_time != 0:
        interval = current_time - last_tap_time
        if interval > 2:  # If more than 2 seconds have passed, start over
            last_tap_time = current_time
            return
        
        new_bpm = int(60 / interval)  # Calculate BPM based on time between taps
        bpm = new_bpm
    
    last_tap_time = current_time


def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def get_char():
    if is_data():
        return sys.stdin.read(1)
    return None

def main():
    global current_step
    
    print("\033[2J", end="")
    print("\033[?25l", end="")
    
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        
        while True:
            display_sequencer()
            
            start_time = time.time()
            while time.time() - start_time < 60 / (bpm * 4):
                char = get_char()
                if char:
                    if char == 'q':
                        return
                    elif char == 's':
                        next_channel()
                    elif char == 'd':
                        tap_tempo()
                    elif char == 'f':
                        toggle_step()
                    elif char == 'g':
                        clear_channel()
            
            current_step = (current_step + 1) % steps
    
    finally:
        print("\033[?25h", end="")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
