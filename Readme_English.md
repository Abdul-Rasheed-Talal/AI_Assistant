# 🤖 Jarvis Lite – Your Offline Personal AI Assistant

Jarvis Lite is a free and lightweight personal AI assistant project that works offline on your laptop, without requiring OpenAI or any paid APIs. This project is designed for people who have normal/budget laptops and want to create their own personal AI — one that can talk to you, remember your tasks, and give you reminders.

---

## 🧩 Project Highlights

- ✅ 100% Free & Offline
- ✅ Lightweight (2–3 GB Model)
- ✅ Voice Input & Output
- ✅ Task Memory (Reminders)
- ✅ Auto Online Upgrade Option (Future Feature)

---

## 💻 System Requirements

This project is optimized for low-end laptops.

| Requirement       | Minimum                   | Recommended               |
|-------------------|---------------------------|---------------------------|
| OS                | Windows 10 / Linux / macOS| Latest stable OS          |
| CPU               | Dual Core                 | Quad Core                 |
| RAM               | 6 GB                      | 8 GB or higher            |
| Disk Space        | 6 GB free                 | 10 GB free                |
| Internet          | Optional (for setup & updates) | Recommended for online mode |

---

## ⚙️ PHASE 1 – SYSTEM PREPARATION (No Coding Yet)

In this phase, we will only prepare the system — Python, tools, and AI model setup.

### 🧩 STEP 1 — Install Python

Go to 👉 https://www.python.org/downloads/

- Download Python 3.10+ version
- During installation, ✅ be sure to select the “Add Python to PATH” option

After installation, check:

```bash
python --version
If the version number is displayed → ✅ Success

🧩 STEP 2 — Install VS Code
Download 👉 https://code.visualstudio.com/

Install and open

Add the Python extension (search “Python” in VS Code)

Now the IDE is ready to run the project.

🧩 STEP 3 — Virtual Environment Setup
Create a folder jarvis-lite

Open the terminal inside that folder

Run:

bash
python -m venv venv
Activate the environment:

Windows: venv\Scripts\activate

Linux/macOS: source venv/bin/activate

🧩 STEP 4 — Install Basic Libraries
In the terminal, type:

bash
pip install pyttsx3 SpeechRecognition requests
These 3 free libraries are for Jarvis’s voice and input system.

🧩 STEP 5 — Install Ollama (Offline Model Runner)
Ollama is a free tool that runs AI models offline.

Visit 👉 https://ollama.com/download

Install according to your OS (Windows / Mac / Linux)

After installation, type in the terminal:

bash
ollama run llama2
If you get a response from the AI → ✅ Installation successful

🧩 STEP 6 — Download DeepSeek Model (Offline Brain)
This model will be Jarvis’s offline AI brain.
It’s a lightweight (2–3 GB) version, available for free.

In the terminal, type:

bash
ollama pull deepseek-coder:1.3b
Wait until the download completes.

Test run:

bash
ollama run deepseek-coder:1.3b
Type any message — if you get a reply → ✅ Model is ready

🧩 STEP 7 — Create Folder Structure
Create the project folder layout (for now, keep the files empty):

text
jarvis-lite/
├── main.py
├── core/
│   ├── voice.py
│   ├── ai_engine.py
│   └── memory.py
├── data/
│   ├── memory.json
│   └── settings.json
├── logs/
└── README.md
🧩 STEP 8 — Prepare Memory & Settings Files
data/memory.json

json
{
    "tasks": [],
    "name": "User",
    "preferences": {}
}
data/settings.json

json
{
    "voice_speed": 170,
    "voice_gender": "male",
    "model": "deepseek-coder:1.3b"
}
These files are for Jarvis’s “memory” and basic preferences.

🧩 STEP 9 — Audio System Check
Test the mic (via Sound Settings → “Test Mic”)

Test the speakers (System Sound → Output → Test)

Clear audio detection is required — Jarvis will use voice.

🧩 STEP 10 — Final Verification
Checklist:

Python installed

VS Code ready

Virtual Env active

Libraries installed

Ollama installed

DeepSeek model downloaded

Folder structure ready

Audio working

✅ Your system is now fully ready for the coding phase.

🧠 Jarvis System Readiness Check (Step-by-Step)
(This is a complete testing guide before starting coding)

🧩 1. Python Installation Check
Command:

bash
python --version
Expected Output:

text
Python 3.10.0  (or 3.11 / 3.12)
✅ If the version number appears → Python is installed and working.
❌ If “not recognized” appears → reinstall and tick “Add to PATH”.

🧩 2. VS Code Test
Open VS Code

Create a new file → test.py

Type:

python
print("VS Code Ready!")
Run (Ctrl + F5)

✅ If “VS Code Ready!” prints in the console → IDE is perfect.
❌ If an error occurs → check if the Python extension is installed.

🧩 3. Virtual Environment Check
Command:

bash
python -m venv venv
Then activate:

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

Check:
The prompt should show (venv).
✅ If it shows → Virtual Env is working.

To deactivate:

bash
deactivate
🧩 4. Libraries Installation Check
Command:

bash
pip list
Expected Installed Packages:

pyttsx3

SpeechRecognition

requests

✅ If all three are listed → perfect.
❌ If any are missing → reinstall:

bash
pip install pyttsx3 SpeechRecognition requests
🧩 5. Ollama Installation Check
Command:

bash
ollama --version
✅ If the version number is shown → Ollama is installed.
❌ If “command not found” or “not recognized” appears → reinstall from https://ollama.com/download.

🧩 6. Ollama Test Run
Command:

bash
ollama run llama2
The system will load for a few seconds.
Then type:

text
Hello
Expected Output:
AI reply in text form.
✅ If you get a reply → Ollama model runner is working.

🧩 7. DeepSeek Model Check
Command:

bash
ollama list
Expected Output:

text
deepseek-coder:1.3b
If listed → model is downloaded.

Extra test:

bash
ollama run deepseek-coder:1.3b
Then type:

text
What can you do?
✅ If you get a reply → DeepSeek model is ready and working offline.

🧩 8. Folder Structure Check
Open your project folder jarvis-lite/
Check if this structure exists:

text
jarvis-lite/
├── main.py
├── core/
│   ├── voice.py
│   ├── ai_engine.py
│   └── memory.py
├── data/
│   ├── memory.json
│   └── settings.json
└── logs/
✅ If all folders & files are present → structure is ready.

🧩 9. JSON Files Check
Open data/memory.json
✔️ File should contain:

json
{
    "tasks": [],
    "name": "User",
    "preferences": {}
}
Open data/settings.json
✔️ File should contain:

json
{
    "voice_speed": 170,
    "voice_gender": "male",
    "model": "deepseek-coder:1.3b"
}
✅ If both files are in correct JSON format → memory system is ready.

🧩 10. Audio System Check
🎤 Mic Test

In Windows: “Sound Settings → Input → Test Microphone”

Say “Hello” — if the bar moves → mic is working

🔊 Speaker Test

“Sound Settings → Output → Test Sound”

A beep sound should play → speaker is working

✅ If both work → Jarvis voice features are ready.

🧩 11. Internet Connection Check (optional online mode)
Command:

bash
ping google.com
✅ If “Reply from…” appears → internet is working.
❌ If “Request timed out” → it will only work in offline mode.

🧩 12. Final Verification
Item	Test Command / Check	Status
Python	python --version	✅
VS Code	print() test	✅
Virtual Env	(venv) prefix	✅
Libraries	pip list	✅
Ollama	ollama --version	✅
DeepSeek Model	ollama list	✅
Folder Structure	Manual check	✅
JSON Files	Open manually	✅
Mic/Speaker	System settings	✅
Internet	ping google.com	✅ / Optional
✅ If all are green ticks → your system is completely ready for coding.

🧠 JARVIS LITE — CODING PHASE PLAN (Step-by-Step)
⚙️ PHASE 1 — BASIC SETUP & STARTUP SCRIPT
🎯 Goal: Create Jarvis’s main entry point (main.py)
This file will be the project’s “brain switch” — connecting all modules.

Steps:

Create main.py file

Import basic modules (voice, AI, memory)

Add startup line: “Hello Sir, I am online.”

Add loop: continuously listen → process → respond

Test output: print messages in the console

✅ Test: Jarvis runs in the terminal and speaks the start-up message.

🎙️ PHASE 2 — VOICE INPUT & OUTPUT MODULE
🎯 Goal: Jarvis understands your voice and responds verbally.

Steps:

Open core/voice.py

Add Speech-to-Text (STT) function (using SpeechRecognition)

Add Text-to-Speech (TTS) function (using pyttsx3)

Add voice settings (speed, gender from settings.json)

Test:

Say “Hello” into the mic

Jarvis says “You said Hello”

✅ Test: Both voice input and output work correctly.

🧠 PHASE 3 — OFFLINE AI BRAIN (DeepSeek Integration)
🎯 Goal: Connect Jarvis to the local AI (Ollama + DeepSeek)

Steps:

Open core/ai_engine.py

Add function → send text to Ollama CLI

Receive DeepSeek’s reply

Return output to main.py

Test manually:

Type a prompt → AI reply should appear in the terminal

✅ Test: DeepSeek model responds offline.

💾 PHASE 4 — MEMORY SYSTEM (Tasks & Reminders)
🎯 Goal: Jarvis remembers tasks and gives reminders.

Steps:

Open core/memory.py

Add functions:

add_task(task) → save to memory.json

get_tasks() → show tasks

clear_tasks() → delete all tasks

Test:

Say: “Jarvis, remember to call Ali.”

Check memory.json → entry saved

Restart and say “show my tasks” → Jarvis remembers

✅ Test: Memory file updates and Jarvis remembers.

🌐 PHASE 5 — AUTO ONLINE SWITCH (Optional)
🎯 Goal: Use online AI if internet is available, otherwise use offline.

Steps:

Add function: check_internet()

If internet available → call DeepSeek API (online mode)

Else → use offline model (DeepSeek local)

Print which mode is active (for debug)

✅ Test:

Run with WiFi off → “Offline Mode”

Run with WiFi on → “Online Mode”

🗂️ PHASE 6 — COMMAND UNDERSTANDING (Smart Prompts)
🎯 Goal: Jarvis understands what the user is saying (simple command parsing)

Steps:

Add logic:

If “remember” in command → save to memory

If “show tasks” → show memory

If “time” → speak current time

Else → general reply from AI brain

Test:

“Jarvis, what’s the time?”

“Jarvis, add task call my friend.”

✅ Test: Jarvis takes the correct action for each simple command.

💬 PHASE 7 — MAIN LOOP LOGIC (Real Conversation)
🎯 Goal: Build a continuous conversation system.

Steps:

In main.py, add main loop:

Listen → Process → Speak → Repeat

Add stop commands (“exit”, “sleep”, “goodbye”)

Add exception handling (no mic input, slow model, etc.)

Print log messages in the terminal

✅ Test: Jarvis continuously listens and responds.

🔔 PHASE 8 — TASK REMINDER SYSTEM (Time-based)
🎯 Goal: Jarvis automatically reminds you of scheduled tasks.

Steps:

Add function to memory.py:

Add “time” field to each task

Add scheduler (simple while loop checking every minute)

When time matches → Jarvis says “Reminder: [task name]”

Test:

Add a task for 1 minute later

Wait → Jarvis reminds you

✅ Test: Jarvis auto-reminds without input.

📁 PHASE 9 — LOGGING SYSTEM (Optional)
🎯 Goal: Keep a record of every conversation and error.

Steps:

Create logs/ folder

Add daily log file (e.g., log_2025_11_06.txt)

Save:

Time

User input

Jarvis reply

Test:

Run 2–3 chats → check log file is created

✅ Test: Logs file updates continuously.

🎨 PHASE 10 — GUI (Future Optional Upgrade)
🎯 Goal: Simple desktop interface for Jarvis (later update)

Steps:

Use Tkinter or React

Add chat window + mic button

Display tasks and messages visually

✅ Future enhancement (optional).

🧩 FINAL CHECKLIST (Before Completion)
Feature	Status
Voice Input / Output	✅
Offline AI Brain (DeepSeek)	✅
Memory System	✅
Task Manager	✅
Online Switch	✅
Reminder System	✅
Logging	✅
🚀 Final Step — Full Integration Test
Run main.py

Say:

“Jarvis, remember to drink water.”

“Show my tasks.”

“What’s the time?”

“Who made you?”

Jarvis should respond verbally and save data in memory.

⚙️ JARVIS LITE – OFFLINE + ONLINE HYBRID SYSTEM OVERVIEW
🧩 1. OFFLINE MODE (DEFAULT MODE)
(when there’s no internet or you intentionally want to run offline)

🔹 How it works:

Jarvis takes your voice input from the mic

Converts Speech → Text (via SpeechRecognition)

Sends text to the DeepSeek offline model (via Ollama)

Model generates a reply

Jarvis speaks the reply aloud (via pyttsx3)

If you say “remember” → it stores the task in memory.json

🔹 What works offline:

Feature	Offline Available?
Voice input/output	✅ Yes
AI chat (DeepSeek local)	✅ Yes
Task saving/reminders	✅ Yes
JSON memory system	✅ Yes
Logs system	✅ Yes
Internet checking	⚙️ N/A (assumed false)
🧠 Meaning:

Even without internet, your Jarvis will:

Understand speech

Respond

Save your tasks

Remind you

✅ Fully usable AI assistant offline.

☁️ 2. ONLINE MODE (HYBRID UPGRADE)
(when internet is connected)

🔹 How it works:

At startup, Jarvis runs check_internet()

If connection is active → sets online flag

When you send a query:

If it’s a simple command (“remember”, “show tasks”) → handles offline

If it’s general chat (“who are you?”, “write a poem”) → sends a request to DeepSeek’s online API

API response arrives → Jarvis speaks it aloud

🔹 What works online:

Feature	Online Available?
Voice input/output	✅ Yes
AI chat (DeepSeek online)	✅ Yes
Task system	✅ Yes
Memory sync	✅ Yes
Cloud model	✅ Yes (optional)
⚙️ How it decides:

python
if internet_available():
    mode = "online"
else:
    mode = "offline"
✅ Automatic switching — you don’t need to do anything.

🔀 3. AUTO-SWITCH LOGIC
Jarvis’s smart function checks on every run:

Ping Google or DeepSeek API

If response is received → “Online Mode Activated”

If not → “Offline Mode Activated”

If internet is lost mid-conversation:

Jarvis automatically falls back to the offline model

The system won’t crash, it will only change modes quietly

✅ Fail-safe hybrid design.

⚡ 4. Practical Example
Situation	Jarvis Response
WiFi is off	“Running in offline mode, using local DeepSeek.”
WiFi is on	“Connected online, using DeepSeek API.”
Command: “Remember to send email.”	Task saved in JSON (offline)
Command: “Who is Elon Musk?”	Uses online DeepSeek (faster, more info)
Command: “Good morning.”	Uses offline DeepSeek (casual chat)
💾 5. Data Handling
Type	Storage	Works Offline?	Works Online?
Tasks	data/memory.json	✅	✅
Settings	data/settings.json	✅	✅
Logs	logs/log_*.txt	✅	✅
Jarvis never sends data over the internet (only query text is sent for the online API, but personal data is stored only in memory.json).

🧠 Meaning: Both private and functional.

🛠️ 6. Optional Upgrade (Smart Cloud Hybrid)
Later, if desired:

Jarvis can automatically backup memory.json to the cloud

You can access tasks from your phone too

This can be integrated in a future version (Jarvis Cloud).

✅ Summary
Feature	Offline Mode	Online Mode
Voice chat	✅	✅
AI brain	DeepSeek Local	DeepSeek API
Internet required	❌	✅
Task reminder	✅	✅
Speed	Medium	Fast
Storage used	2–3 GB	0 GB
Privacy	Full local	Partial (API text only)
🧠 Conclusion:
Yes — this entire system will be an offline + online hybrid.
You can run the full Jarvis even offline, and when the net is available, it will automatically switch to online mode to make answers smarter and faster ⚡