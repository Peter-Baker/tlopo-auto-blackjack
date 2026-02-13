
# This program will allow you to get pixel cords of where ever you click

import pyautogui
from pynput import mouse, keyboard

points = []

print("Click twice to record two positions.")
print("Press any key after that to stop the program.\n")

def on_click(x, y, button, pressed):
    if pressed:
        points.append((x, y))
        print(f"Click {len(points)}: {x}, {y}")

        if len(points) == 2:
            print("\nNow press any key to exit.")

def on_press(key):
    print("\nStopping...")
    return False   # stop keyboard listener

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()

print("\nRecorded points:")
for i, p in enumerate(points, 1):
    print(f"{i}: {p}")
