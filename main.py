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

def detect_number_ocr(x, y, width=15, height=15):
    """Detect a number 1-21 in a small screen region using OCR"""
    with mss.mss() as sct:
        # Capture the region
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        
        # Convert to PIL Image for pytesseract
        image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        
        # Upscale for better OCR accuracy
        image = image.resize((image.width * 4, image.height * 4))
        
        # Extract text
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        try:
            number = int(text.strip())
            if 1 <= number <= 21:
                return number
        except ValueError:
            pass
    return None

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