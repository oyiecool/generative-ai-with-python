# pi_projects/voice/assistant.py
import datetime as dt
import subprocess
import wave
from pathlib import Path

import numpy as np
import ollama
import sounddevice as sd
from faster_whisper import WhisperModel
from gpiozero import LED, Button
from piper import PiperVoice

RATE = 16_000
MODEL = "qwen2.5:1.5b"
VOICE = Path.home() / "voices/en_US-lessac-medium.onnx"
OUT_WAV = Path("/dev/shm/reply.wav")                 # RAM disk: no SD-card wear

button, led = Button(17), LED(27)
stt = WhisperModel("base.en", device="cpu", compute_type="int8")
tts = PiperVoice.load(str(VOICE))

SYSTEM = ("You are a concise offline home assistant on a Raspberry Pi. Answer in at most two "
          "short sentences suitable for speech. Use tools for the time or system status. "
          "If you do not know, say so.")


# ---- read-only tools (Chapter 7 rules: narrow, validated, no side effects) ----
def get_time() -> str:
    """Return the current local date and time."""
    return dt.datetime.now().strftime("%A %d %B, %H:%M")


def get_system_status() -> str:
    """Return the Raspberry Pi temperature, load and free disk space."""
    temp = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True).stdout.strip()
    load = Path("/proc/loadavg").read_text().split()[:3]
    df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.splitlines()[1].split()
    return f"{temp}; load {' '.join(load)}; root disk {df[4]} used, {df[3]} free"


TOOLS = {"get_time": get_time, "get_system_status": get_system_status}


def record_while_pressed() -> np.ndarray:
    frames = []
    with sd.InputStream(samplerate=RATE, channels=1, dtype="float32") as stream:
        while button.is_pressed:
            chunk, _ = stream.read(1024)
            frames.append(chunk)
    return np.concatenate(frames).flatten() if frames else np.zeros(0, dtype=np.float32)


def transcribe(audio: np.ndarray) -> str:
    if audio.size < RATE * 0.3:                        # ignore taps shorter than 0.3 s
        return ""
    segments, _ = stt.transcribe(audio, language="en", vad_filter=True, beam_size=1)
    return " ".join(s.text.strip() for s in segments)


def think(question: str) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for _ in range(3):                                 # bounded tool loop (Chapter 10)
        r = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                        options={"temperature": 0.2, "num_predict": 120})
        msg = r.message
        if not msg.tool_calls:
            return msg.content.strip()
        messages.append(msg)
        for call in msg.tool_calls:
            fn = TOOLS.get(call.function.name)
            result = fn() if fn else "unknown tool"
            messages.append({"role": "tool", "content": result, "tool_name": call.function.name})
    return "Sorry, I could not finish that."


def speak(text: str) -> None:
    with wave.open(str(OUT_WAV), "wb") as wf:
        tts.synthesize_wav(text, wf)
    subprocess.run(["aplay", "-q", str(OUT_WAV)], check=False)


def main() -> None:
    speak("Ready.")
    while True:
        button.wait_for_press()
        led.on()                                       # solid: listening
        audio = record_while_pressed()
        led.blink(on_time=0.1, off_time=0.1)           # blinking: thinking
        text = transcribe(audio)
        reply = think(text) if text else "I didn't catch that."
        led.off()
        speak(reply)


if __name__ == "__main__":
    main()
