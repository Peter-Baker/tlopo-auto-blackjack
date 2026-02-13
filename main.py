import mss
import numpy as np
import time
import threading
import pyautogui
from pynput import keyboard

# I didnt account for things combining
# I think its clicking before switching cords?

# Left Hexagon 1390, 199
# Left Hexagon BGR RED: (51, 50, 108)
# Left Hexagon BGR BLUE: (248, 191, 22)
# Left Hexagon BGR GREEN: (78, 129, 155)

# Right Hexagon 1478, 262
# Right Hexagon BGR RED: (83, 88, 168)
# Right Hexagon BGR BLUE: (182, 88, 14)
# Right Hexagon BGR GREEN: (29, 80, 72)

running = False
stop_program = False

def detect_number():
    # Soon to be
    print("Guess number")

def worker():
    global running, stop_program

    while not stop_program:
        if running:
            detect_number()
            time.sleep(2)
            pyautogui.moveTo(1430, 338)
        else:
            time.sleep(0.1)

def on_press(key):
    global running, stop_program

    # toggle with any key
    if key == keyboard.Key.esc:
        print("Exiting...")
        stop_program = True
        return False

    running = not running

    if running:
        print("Started checking every 2 seconds...")
    else:
        print("Stopped checking.")

print("Press any key to start / stop checking.")
print("Press ESC to exit.")

t = threading.Thread(target=worker, daemon=True)
t.start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# PRESS ESC TO END PROGRAM