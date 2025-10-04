import wikipedia
import webbrowser
import os
import sys
import subprocess
import asyncio
from shazamio import Shazam
import sounddevice as sd
from scipy.io.wavfile import write
import textwrap


# ---------- Wikipedia Search ----------
def fetch_wikipedia(query, sentences=3):
    wikipedia.set_lang("en")
    try:
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
        page = wikipedia.page(query, auto_suggest=True)
        return page.title, summary, page.url
    except Exception as e:
        return None, f"Error: {e}", ""


# ---------- Open Websites / Apps ----------
def open_website(url, name):
    print(f"🌐 Opening {name}...")
    webbrowser.open(url)

def open_app(app_name):
    print(f"🚀 Trying to open {app_name}...")
    try:
        if sys.platform.startswith("win"):
            os.startfile(app_name)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", app_name])
        else:
            subprocess.Popen([app_name])
    except Exception as e:
        print(f"❌ Could not open {app_name}: {e}")


# ---------- Song Recognition ----------
def record_audio(filename="recorded.wav", duration=7, fs=44100):
    print("🎤 Listening... play the song now.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, audio)
    print("✅ Saved recording as", filename)
    return filename

async def recognize_song(file_path):
    shazam = Shazam()
    print("🎧 Analyzing the song...")
    out = await shazam.recognize_song(file_path)

    if 'track' in out and out['track']:
        track = out['track']
        print("\n✅ Found Song:")
        print(f"🎵 Title : {track.get('title')}")
        print(f"👤 Artist: {track.get('subtitle')}")
        print(f"🔗 URL   : {track.get('url')}")
    else:
        print("❌ Could not recognize the song.")


# ---------- Main Assistant ----------
def main():
    print("🤖 JARVISH Assistant Ready!")
    print("Commands: wikipedia <query>, youtube, spotify, netflix, open <app>, listen, exit\n")

    while True:
        command = input("jarvish> ").lower().strip()

        if command in ("exit", "quit", "bye"):
            print("👋 Goodbye!")
            break

        elif command.startswith("wikipedia"):
            query = command.replace("wikipedia", "").strip()
            if not query:
                print("❓ Please type: wikipedia <search term>")
                continue
            title, summary, url = fetch_wikipedia(query)
            print("\n---")
            print(f"📖 {title}")
            print(textwrap.fill(summary, width=80))
            print(f"🔗 {url}")
            print("---\n")

        elif "youtube" in command:
            open_website("https://www.youtube.com", "YouTube")

        elif "spotify" in command:
            open_website("https://open.spotify.com", "Spotify")

        elif "netflix" in command:
            open_website("https://www.netflix.com", "Netflix")

        elif command.startswith("open"):
            app = command.replace("open", "").strip()
            if app:
                open_app(app)
            else:
                print("❓ Example: open notepad")

        elif "listen" in command:
            filename = record_audio()
            asyncio.run(recognize_song(filename))

        else:
            print("❌ Unknown command. Try: wikipedia <q>, youtube, spotify, netflix, open <app>, listen, exit")

if __name__ == "__main__":
    main()
