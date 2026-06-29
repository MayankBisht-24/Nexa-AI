"""
NEXA Voice Assistant v4.1
==========================
CHANGES in v4.1:
  - API key now loaded securely from .env file via python-dotenv
  - No hardcoded credentials — production safe

INSTALL inside .venv (run this FIRST):
  pip install gTTS pygame SpeechRecognition pyaudio google-genai python-dotenv

SETUP:
  Create a file named .env in the same folder as this script.
  Add this line inside it:
      GEMINI_API_KEY=your_actual_api_key_here
"""

import os
import re
import time
import threading
import tempfile
import webbrowser

import speech_recognition as sr
from google import genai
from gtts import gTTS
from dotenv import load_dotenv
import pygame


# =======================
# ENVIRONMENT & API SETUP
# =======================
# Load environment variables from the .env file in the project root.
# This keeps the API key out of source code — safe to push to GitHub.

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Create a .env file and add: GEMINI_API_KEY=your_key_here"
    )

client = genai.Client(api_key=API_KEY)


# =======================
# PYGAME AUDIO INIT
# =======================
# Initialize the pygame mixer once at startup.
# All audio playback is routed through this mixer.

pygame.mixer.init()


# =======================
# SPEECH SYNTHESIS
# =======================

_speak_lock = threading.Lock()


def speak(text):
    """
    Convert text to speech using Google TTS and play it via pygame.
    Thread-safe via a lock — only one utterance plays at a time.
    Automatically cleans up the temporary MP3 file after playback.
    """
    print(f"Nexa: {text}")

    with _speak_lock:
        tmp_path = None
        try:
            # Strip markdown symbols that would sound wrong when spoken
            clean = re.sub(r'[*#_`]', '', text).strip()
            if not clean:
                return

            # Generate speech audio using Indian English accent
            tts = gTTS(text=clean, lang="en", tld="co.in", slow=False)

            # Save to a temporary file — deleted after playback
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = tmp.name

            tts.save(tmp_path)

            # Load and play audio; block until playback finishes
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.05)

            pygame.mixer.music.unload()

        except Exception as e:
            print(f"[Speak Error]: {e}")

        finally:
            # Always remove the temp file, even if an error occurred
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass


def speak_long(text, chunk_size=220):
    """
    Speak long responses by splitting them into sentence-level chunks.
    Ensures no part of the response is skipped or cut off.
    """
    text = re.sub(r'[*#_`]', '', text).strip()

    if len(text) <= chunk_size:
        speak(text)
        return

    # Split on sentence boundaries — period, exclamation, question mark
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) + 1 <= chunk_size:
            chunk += (" " if chunk else "") + sentence
        else:
            if chunk.strip():
                speak(chunk.strip())
            chunk = sentence

    if chunk.strip():
        speak(chunk.strip())


# =======================
# AI RESPONSE — GEMINI
# =======================

def ask_gemini(question):
    """
    Send the user's question to Gemini 2.5 Flash and return a
    voice-friendly plain-text response — short, clear, no markdown.
    """
    try:
        prompt = (
            "You are Nexa, a smart and friendly voice assistant. "
            "Give a SHORT, clear, conversational answer — max 3 sentences. "
            "Plain text only. No bullet points, no markdown, no special characters.\n\n"
            f"User said: {question}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

        return "Sorry boss, I could not get an answer for that."

    except Exception as e:
        return f"Gemini Error: {e}"


# =======================
# MICROPHONE INPUT
# =======================

def listen(recognizer, timeout=6, phrase_limit=10, label=""):
    """
    Record audio from the microphone and transcribe it using Google
    Speech Recognition with Indian English language support.
    Returns lowercase transcribed text, or None if nothing was heard.
    """
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise before each recording session
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 300

            if label:
                print(f"\n{label}...")

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )

        text = recognizer.recognize_google(audio, language="en-IN")
        return text.lower().strip()

    except sr.WaitTimeoutError:
        # No speech detected within the timeout window
        return None
    except sr.UnknownValueError:
        # Speech was detected but could not be transcribed
        return None
    except sr.RequestError as e:
        print(f"[Mic/Network Error]: {e}")
        return None
    except Exception as e:
        print(f"[Listen Error]: {e}")
        return None


# =======================
# COMMAND ROUTING
# =======================

# Accepted wake word variants — covers common misrecognitions by Google STT
WAKE_WORDS = ["nexa", "lexa", "hexa", "nexus", "next sir", "next", "nxa"]


def process_command(command):
    """
    Route the transcribed command to the appropriate action.
    Simple commands are handled locally for speed.
    All unrecognised queries fall back to Gemini AI.
    Returns 'EXIT' to signal the main loop to terminate.
    """

    # --- Browser navigation ---
    if "open google" in command:
        speak("Opening Google for you boss.")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube boss.")
        webbrowser.open("https://youtube.com")

    elif "open chatgpt" in command:
        speak("Opening Chat G P T boss.")
        webbrowser.open("https://chatgpt.com")

    elif "open github" in command:
        speak("Opening GitHub boss.")
        webbrowser.open("https://github.com")

    elif "open instagram" in command:
        speak("Opening Instagram boss.")
        webbrowser.open("https://instagram.com")

    elif "open spotify" in command:
        speak("Opening Spotify boss.")
        webbrowser.open("https://spotify.com")

    # --- Identity responses ---
    elif "who created you" in command or "who made you" in command:
        speak(
            "I was created by Mayank — a future data scientist and developer. "
            "He built me to be his personal assistant. Pretty cool, right boss?"
        )

    elif "your name" in command or "what are you" in command:
        speak("I am Nexa, your personal voice assistant. Always ready boss.")

    # --- Greetings ---
    elif any(x in command for x in ["how are you", "how r you", "how are", "how r"]):
        speak("I am doing great boss! Fully charged and ready to help you.")

    elif any(x in command for x in ["hello", "hi nexa", "hey nexa", "hi"]):
        speak("Hello boss! How can I help you today?")

    # --- Time and date ---
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"Boss, the current time is {current_time}.")

    elif "date" in command or "today" in command:
        current_date = time.strftime("%A, %d %B %Y")
        speak(f"Today is {current_date} boss.")

    # --- Shutdown command ---
    elif any(x in command for x in ["stop", "goodbye", "bye", "exit", "shutdown"]):
        speak("Goodbye boss! Nexa signing off. Have a great day!")
        return "EXIT"

    # --- Fallback: send to Gemini AI ---
    else:
        speak("Let me think about that boss.")
        response = ask_gemini(command)
        print(f"\n[Gemini Response]:\n{response}\n")
        speak_long(response)

    return None


# =======================
# MAIN LOOP
# =======================

def main():
    """
    Primary execution loop.
    Phase 1: Listen continuously for the wake word.
    Phase 2: On wake word detection, listen for the command.
    Phase 3: Route the command and repeat.
    Auto-resets the recognizer after 5 consecutive errors.
    """
    recognizer = sr.Recognizer()

    speak("Initializing Nexa. Say Nexa to wake me up boss.")

    consecutive_errors = 0

    while True:
        try:

            # Phase 1 — Listen for wake word (short window, 3 seconds max)
            wake = listen(
                recognizer,
                timeout=5,
                phrase_limit=3,
                label="Listening for wake word"
            )

            if wake is None:
                consecutive_errors = 0
                continue

            print(f"Heard: {wake}")

            # Ignore audio that does not contain a valid wake word
            if not any(w in wake for w in WAKE_WORDS):
                continue

            consecutive_errors = 0

            # Phase 2 — Acknowledge and listen for the command
            speak("Yes Boss")
            time.sleep(0.3)

            command = listen(
                recognizer,
                timeout=7,
                phrase_limit=12,
                label="Listening for command"
            )

            if command is None:
                speak("Boss, I didn't catch that. Try again please.")
                continue

            print(f"Command: {command}")

            # Phase 3 — Process and respond
            result = process_command(command)
            if result == "EXIT":
                break

        except KeyboardInterrupt:
            print("\n[Nexa stopped by user]")
            speak("Goodbye boss!")
            break

        except Exception as e:
            consecutive_errors += 1
            print(f"[Unexpected Error #{consecutive_errors}]: {e}")

            # Reset the recognizer after repeated failures
            if consecutive_errors >= 5:
                print("Too many errors. Restarting mic listener...")
                recognizer = sr.Recognizer()
                consecutive_errors = 0
                time.sleep(2)

    pygame.mixer.quit()


# =======================
# ENTRY POINT
# =======================

if __name__ == "__main__":
    main()