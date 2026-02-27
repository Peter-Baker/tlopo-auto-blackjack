import mss
import numpy as np
import time
import threading
import pyautogui
from pynput import keyboard
import pytesseract
from PIL import Image
import os

running = False
stop_program = False

def detect_number(left, top, width, height):
    # Capture the screen region where the blackjack total appears.
    # Top-left corner (1267, 1169), bottom-right corner (1313, 1199).
    # Returns an integer if a number is detected, otherwise None.
    try:
        with mss.mss() as sct:
            monitor = {
                "left": left,
                "top": top,
                "width": width - left,
                "height": height - top,
            }
            img = np.array(sct.grab(monitor))
    except Exception:
        # if screen capture fails return None
        return None

    # convert to PIL image for processing
    img_pil = Image.fromarray(img)

    # preprocess: grayscale and upscale for better OCR
    gray = img_pil.convert("L")
    # ANTIALIAS was removed in recent Pillow versions, use LANCZOS or Resampling.LANCZOS
    try:
        resample_filter = Image.LANCZOS
    except AttributeError:
        # fallback for very new versions
        resample_filter = Image.Resampling.LANCZOS
    gray = gray.resize((gray.width * 2, gray.height * 2), resample_filter)

    # perform OCR limiting to digits only
    custom_config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(gray, config=custom_config)

    # try to extract a whole number
    import re
    match = re.search(r"\d+", text)
    if match:
        try:
            return int(match.group())
        except ValueError:
            return None
    return None

def worker():
    global running, stop_program

    while not stop_program:
        if running:
            # Detect normal 1267, 1169), bottom-right corner (1313, 1199).
            card_total = detect_number(1167, 1169, 1313, 1199) # Normal Left, bottom right corner
            if card_total is None:
                # If card total is not found, check to the right (1316, 1179) bottom right corner (____, ____)#
                # Click 5: 1324, 1166 Click 6: 1363, 1205
                card_total_right = detect_number(1324, 1166, 1363, 1205)
                if card_total_right != None:
                    card_total = card_total_right
                else:
                    pyautogui.moveTo(1592, 1448)
                    pyautogui.click()
                    pyautogui.moveTo(1578,1531)
                    pyautogui.click()
            elif card_total == 2:
                # Click the "Bid 2" button at 1578, 1531
                pyautogui.moveTo(1578,1531)
                pyautogui.click()
            elif card_total >= 17:
                # Click Hold 1394,1447
                pyautogui.moveTo(1394,1447)
                pyautogui.click()       

            else:
                # Click Hit 1592, 1448
                pyautogui.moveTo(1592, 1448)
                pyautogui.click()

            print(f"{card_total} is the card total.")
            time.sleep(2)
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

def main():
    print("Press any key to start / stop checking.")
    print("Press ESC to exit.")

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()

# PRESS ESC TO END PROGRAM