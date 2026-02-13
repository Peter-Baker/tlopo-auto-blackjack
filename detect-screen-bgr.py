# click_pixel_bgr.py


# 1390, 199
# 1478, 262
import mss
import numpy as np
from pynput import mouse, keyboard

print("Click anywhere to read that pixel's BGR value.")
print("Press any key to stop.\n")

def on_click(x, y, button, pressed):
    if not pressed:
        return

    # IMPORTANT: create mss inside the callback thread
    with mss.mss() as sct:
        monitor = {
            "left": 1324,
            "top": 167,
            "width": 1,
            "height": 1
        }

        img = np.array(sct.grab(monitor))
        b, g, r, a = img[0, 0]

        print(f"LEFT SIDE: Click at (1390, 199) -> BGR = ({b}, {g}, {r})")

        monitor = {
            "left": 1439,
            "top": 256,
            "width": 1,
            "height": 1
        }

        img = np.array(sct.grab(monitor))
        b, g, r, a = img[0, 0]

        print(f"RIGHT SIDE: Click at (1229, 621) -> BGR = ({b}, {g}, {r})")

        print()

def on_press(key):
    print("\nStopping...")
    return False

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()
