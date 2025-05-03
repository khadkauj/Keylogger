## 🔐 Telegram Keylogger (For Educational Use Only)

A Python-based keylogger that logs keystrokes and sends them to Telegram every 10 minutes, along with a screenshot.

## ⚠️ Disclaimer:
This tool is intended strictly for educational purposes in a controlled, personal lab environment only.
Unauthorized use to monitor others without consent is illegal and unethical.

## Overview
- This Python script captures:

- Keystrokes on your system.

- Screenshots of the screen every 10 minutes.

- It sends both to a Telegram bot:

- Keystrokes are sent as a formatted message.

- Screenshots are sent as compressed JPEG images.

## Features
-  Real-time keystroke logging (with buffer handling)

-  Screenshot capture every 10 minutes (resized for efficiency)

-  Sends all data to a private Telegram bot

-  Automatically deletes screenshots after successful upload

-  No third-party storage like Firebase—only Telegram is used

-  Runs silently in the background using multithreading

##  🚀 Setup Instructions
1. Clone or Download the Script

git clone https://github.com/yourusername/telegram-keylogger
cd telegram-keylogger
Or just create a Python file (keylogger.py) and paste the code.

2. Create a Telegram Bot
Open Telegram and search @BotFather

Use /newbot and follow prompts to get your bot token

Save your token for later

3. Get Your Telegram Chat ID
Start a chat with your bot

Visit the following URL in your browser:

https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
Send a message to the bot, then refresh the URL

Look for "chat":{"id":123456789,...} — that’s your chat ID

4. Install Dependencies
Make sure you're using Python 3.9+ (for zoneinfo) and have the following libraries:


`pip install pynput Pillow requests`

5. Configure the Script
Edit these lines in the script:

`TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"`
`TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"`

6. Run the Script

`python keylogger.py`

The script will:

Start listening to keystrokes

Every 10 minutes:

Send the buffered keystrokes as a message

Take and send a screenshot

Clear local logs and screenshot afterward

🛑 Safety Tips
Do not run this script on shared, public, or unauthorized machines.

Do not distribute this code without including this README and disclaimer.

Always respect privacy and cyber laws.

📜 License
This project is for educational purposes only and does not come with any license for malicious use.