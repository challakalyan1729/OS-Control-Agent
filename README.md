# 🤖 God Mode Agent (OS Control Bot)

An AI-powered automation agent that lets you **monitor and control a Windows PC remotely via Telegram**.  
The system uses **Python automation** combined with **Google Gemini (2.0 Flash)** to interpret natural-language commands and analyze on-screen content.

---

## 🚀 Key Capabilities

### 🖥️ Screen Understanding
- Capture screenshots on demand
- Use Gemini Vision to generate a contextual explanation of what is visible on the screen

### 📂 Application Control
- Launch desktop applications remotely  
  (e.g., Notepad, Calculator, Browser)

### 🔋 System Monitoring
- Battery status
- CPU and memory usage
- Basic system health metrics

### 🔒 System Security
- Lock the workstation remotely
- Put the system to sleep

### 🧠 AI Assistant
- Chat with Gemini for general assistance and command interpretation

---

## 🛠️ Tech Stack

- **Python**
- **PyAutoGUI** – OS automation
- **Telegram Bot API** – Remote command interface
- **Google Gemini 2.0 Flash** – Natural language & vision understanding
- **psutil** – System metrics
- **python-dotenv** – Environment management

---

## 🧩 How It Works (High-Level)

1. User sends a command via Telegram  
2. Telegram bot receives and parses the message  
3. Gemini interprets intent (and screen content when required)  
4. Python automation executes the action on the Windows system  
5. Response (text or screenshot) is sent back to Telegram  

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/challakalyan1729/OS-Control-Agent.git
cd OS-Control-Agent
