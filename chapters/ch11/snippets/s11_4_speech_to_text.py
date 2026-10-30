# uv add faster-whisper
from faster_whisper import WhisperModel

model = WhisperModel("small", device="auto", compute_type="int8")
segments, info = model.transcribe("data/bridge_call.m4a", vad_filter=True)
print("language:", info.language)
for seg in segments:
    print(f"[{seg.start:7.1f}s] {seg.text}")
