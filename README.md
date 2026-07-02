# 🤖 NEXA AI — Personal Voice Assistant

<p align="center">

<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge&logo=google">
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">

</p>

A powerful AI-powered desktop voice assistant built with Python and Google Gemini.

NEXA listens for your voice, understands your commands, performs useful desktop actions, and intelligently answers questions using Google's Gemini AI.

Designed with clean architecture, secure API handling, and real-world development practices.

---

# ✨ Features

* 🎙️ Wake word detection ("Nexa")
* 🧠 AI-powered conversations using Google Gemini
* 🔊 Natural text-to-speech responses
* 🎤 Speech recognition with microphone input
* 🌐 Open websites using voice commands
* 🕒 Tell current time and date
* 💬 Friendly conversational responses
* 🔐 Secure API key management using `.env`
* 🧹 Automatic temporary audio cleanup
* ⚡ Lightweight and beginner-friendly architecture

---

# 🛠️ Tech Stack

* Python 3.12
* Google Gemini API
* SpeechRecognition
* gTTS
* pygame
* python-dotenv
* PyAudio

---

# 📂 Project Structure

```
NEXA-AI/
│
├── main.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/NEXA-AI.git

cd NEXA-AI
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install gTTS pygame SpeechRecognition pyaudio google-genai python-dotenv
```

---

# 🔑 Setup Environment Variables

Create a file named

```
.env
```

Inside it add

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Never upload your API key to GitHub.

---

# ▶️ Run

```bash
python main.py
```

NEXA will start listening.

Simply say

> "Nexa"

Then speak your command.

---

# 🎤 Example Commands

```
Open Google

Open YouTube

Open GitHub

What is the time?

What is today's date?

Who created you?

How are you?

Tell me about Artificial Intelligence

Exit
```

---

# 🔒 Security

This project never stores API keys inside the source code.

All sensitive credentials are loaded securely using:

* python-dotenv
* .env file
* environment variables

---

# 🎯 Future Improvements

* Weather information
* Spotify controls
* WhatsApp messaging
* Email support
* Face recognition
* Home automation
* Desktop application (GUI)
* Offline speech recognition
* Multi-language support
* Custom plugins

---

# 📸 Preview

```
Initializing Nexa...

Say "Nexa"

You:
Open Google

Nexa:
Opening Google for you boss.
```

---

# 🤝 Contributing

Contributions, ideas, and improvements are always welcome.

Fork the repository, create a new branch, and submit a Pull Request.

---

# ⭐ Support

If you found this project helpful,

please consider giving it a ⭐ on GitHub.

It motivates me to build more open-source projects.

---

# 👨‍💻 Developer

**Mayank Bisht**

BCA (Data Science) Student

Python Developer | AI Enthusiast | Open Source Learner

Building projects to learn, improve, and solve real-world problems.

---


