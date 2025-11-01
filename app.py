import os
import re
import subprocess
import time

import cv2
import keyboard
import mss
import numpy as np

from utils import to_ansi_ascii, send_key

window_title = os.environ.get("WINDOW_TITLE", "Minecraft 1.21.10")

def find_window_coords(title):
    try:
        output = subprocess.check_output(["xwininfo", "-root", "-tree"]).decode()
    except FileNotFoundError:
        raise RuntimeError("xwininfo not found. install it through xorg-xwininfo")

    for line in output.splitlines():
        if title.lower() in line.lower():
            # ищем window id в начале строки
            id_match = re.match(r"\s*(0x[0-9a-fA-F]+)", line)
            # ищем координаты и размеры
            coord_match = re.search(r"(\d+)x(\d+)\+\d+\+\d+\s+\+(\d+)\+(\d+)", line)
            if id_match and coord_match:
                window_id = id_match.group(1)
                width = int(coord_match.group(1))
                height = int(coord_match.group(2))
                left = int(coord_match.group(3))
                top = int(coord_match.group(4))
                return left, top, width, height, window_id
    return None

coords = find_window_coords(window_title)
if not coords:
    raise RuntimeError("Window not found\nTIP: Set environment variable WINDOW_TITLE")

left, top, width, height, window_id = coords

def handle_keypress(event):
    send_key(window_id, event.name)

keyboard.on_press(handle_keypress)

while True:
    if os.environ.get("CLEAR") == "1":
        os.system("clear")
    with mss.mss() as sct:
        full = np.array(sct.grab(sct.monitors[1]))
        full = cv2.cvtColor(full, cv2.COLOR_BGRA2BGR)
        crop = full[top:top + height, left:left + width]
        print(to_ansi_ascii(crop))
    if os.environ.get("CLEAR") == "1":
        time.sleep(0.03)
