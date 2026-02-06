import telebot
import pyautogui
import time
import os
import requests
import base64
import psutil
import subprocess
import ctypes

# --- IMPORT KEYS FROM YOUR PYTHON FILE ---
try:
    from keys import TELEGRAM_TOKEN, GEMINI_KEY
except ImportError:
    print("❌ ERROR: keys.py not found!")
    print("👉 Create a file named 'keys.py' and put your tokens there.")
    exit()

bot = telebot.TeleBot(TELEGRAM_TOKEN)
conversation_history = []

# 2. UNIVERSAL AUTO-DISCOVERY
def get_best_model():
    print("\n🔍 SCANNING: Asking Google for available models...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "models" in data:
            for model in data["models"]:
                if "generateContent" in model.get("supportedGenerationMethods", []):
                    if "flash" in model['name']:
                        print(f"✅ FOUND BEST MODEL: {model['name']}")
                        return model['name']
            print(f"✅ FOUND MODEL: {data['models'][0]['name']}")
            return data['models'][0]['name']
        return "models/gemini-1.5-flash"
    except:
        return "models/gemini-pro"


ACTIVE_MODEL = get_best_model()


# 3. CONTEXT CHAT ENGINE
def talk_to_google(user_text):
    global conversation_history
    url = f"https://generativelanguage.googleapis.com/v1beta/{ACTIVE_MODEL}:generateContent?key={GEMINI_KEY}"

    conversation_history.append({"role": "user", "parts": [{"text": user_text}]})
    if len(conversation_history) > 10: conversation_history = conversation_history[-10:]

    data = {"contents": conversation_history}

    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            reply = response.json()['candidates'][0]['content']['parts'][0]['text']
            conversation_history.append({"role": "model", "parts": [{"text": reply}]})
            return reply
        else:
            if response.status_code == 429: return "⚠️ Too fast! Wait 2 mins."
            return f"Google Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Failed: {e}"


# 4. VISION ENGINE
def analyze_image(prompt, image_path):
    url = f"https://generativelanguage.googleapis.com/v1beta/{ACTIVE_MODEL}:generateContent?key={GEMINI_KEY}"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    data = {
        "contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/png", "data": image_data}}]}]}
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Vision Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Vision Error: {e}"


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text.lower()

    # --- POWER COMMANDS ---
    if "shutdown" in text:
        bot.reply_to(message, "⚠️ Shutting Down in 5 seconds...")
        os.system("shutdown /s /t 5")
        return

    if "restart" in text:
        bot.reply_to(message, "⚠️ Restarting System...")
        os.system("shutdown /r /t 5")
        return

    if "sleep" in text and "time" not in text:
        bot.reply_to(message, "💤 Going to Sleep...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return

    # --- OTHER COMMANDS ---
    if text.startswith("open "):
        app_name = text.replace("open ", "")
        bot.reply_to(message, f"🚀 Opening {app_name}...")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        return

    if "battery" in text:
        battery = psutil.sensors_battery()
        if battery:
            bot.reply_to(message, f"🔋 {battery.percent}%")
        else:
            bot.reply_to(message, "❌ No Battery Sensor.")
        return

    if "system" in text:
        cpu = psutil.cpu_percent()
        bot.reply_to(message, f"💻 CPU: {cpu}%")
        return

    if "lock" in text:
        bot.reply_to(message, "🔒 Locking...")
        ctypes.windll.user32.LockWorkStation()
        return

    if "wifi" in text and "off" in text:
        subprocess.run('netsh wlan disconnect', shell=True)
        return

    if "mute" in text:
        pyautogui.press('volumemute')
        return

    if "volume" in text:
        pyautogui.press('volumeup') if "up" in text else pyautogui.press('volumedown')
        return

    if "read screen" in text:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        pyautogui.screenshot("vision.png")
        analysis = analyze_image(f"User: {text}. Explain screen.", "vision.png")
        bot.reply_to(message, analysis)
        if os.path.exists("vision.png"):
            os.remove("vision.png")
        return

    if "clear memory" in text:
        global conversation_history
        conversation_history = []
        bot.reply_to(message, "🧠 Memory Wiped.")
        return

    # --- CHAT ---
    bot.send_chat_action(message.chat.id, 'typing')
    reply = talk_to_google(message.text)
    bot.reply_to(message, reply)


print(f"\n🚀 GOD MODE AGENT ONLINE")
bot.infinity_polling()