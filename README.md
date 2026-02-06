# 🤖 God Mode Agent (OS Control Bot)

An AI-powered agent that allows you to remotely control and monitor your Windows PC using **Telegram**. It uses **Google Gemini 2.0 Flash** to understand natural language commands and analyze your screen.

## ✨ Features

* **👁️ Computer Vision:** Ask the bot to "read screen" and it will send you a screenshot + an AI explanation of what is open.
* **🚀 App Launcher:** Open applications remotely (e.g., "Open Notepad", "Open Calculator").
* **🔋 System Monitor:** Check battery levels, CPU usage, and system health.
* **🔒 Security:** Lock your workstation remotely or put the PC to sleep.
* **🧠 AI Chat:** Chat with the Gemini AI for general assistance.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/challakalyan1729/OS-Control-Agent.git](https://github.com/challakalyan1729/OS-Control-Agent.git)
    cd OS-Control-Agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install pyTelegramBotAPI pyautogui google-generativeai psutil requests python-dotenv
    ```

3.  **Setup Keys:**
    * Create a file named `keys.py` in the project folder.
    * Add your API keys like this:
        ```python
        TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
        GEMINI_KEY = "YOUR_GEMINI_API_KEY"
        ```

## 🎮 Usage

Run the bot:
```bash
python start.py
