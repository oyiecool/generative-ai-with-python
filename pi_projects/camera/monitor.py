# pi_projects/camera/monitor.py
import io
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import ollama
from picamera2 import Picamera2
from PIL import Image

VLM = "moondream"
LOG = Path("/var/lib/camwatch/events.jsonl")
CHANGE_THRESHOLD = 12.0       # mean absolute pixel difference that counts as a change
COOLDOWN_S = 60

cam = Picamera2()
cam.configure(cam.create_still_configuration(main={"size": (1280, 720)},
                                             lores={"size": (320, 180), "format": "YUV420"}))
cam.start()
time.sleep(2)


def small_gray() -> np.ndarray:
    yuv = cam.capture_array("lores")
    return yuv[:180, :320].astype(np.int16)            # Y plane = grayscale


def describe(jpeg: bytes) -> str:
    r = ollama.generate(
        model=VLM,
        prompt=("Describe what changed in this server cupboard image in one sentence. "
                "Mention people, open doors, cables on the floor, smoke or warning lights. "
                "Do not guess identities."),
        images=[jpeg],
        options={"temperature": 0, "num_predict": 60},
    )
    return r["response"].strip()


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    prev, last_event = small_gray(), 0.0
    while True:
        cur = small_gray()
        diff = float(np.abs(cur - prev).mean())
        prev = cur
        if diff > CHANGE_THRESHOLD and time.time() - last_event > COOLDOWN_S:
            last_event = time.time()
            buf = io.BytesIO()
            Image.fromarray(cam.capture_array("main")).convert("RGB").save(buf, "JPEG", quality=80)
            event = {"ts": datetime.now().isoformat(timespec="seconds"),
                     "change": round(diff, 1), "description": describe(buf.getvalue())}
            with LOG.open("a") as f:
                f.write(json.dumps(event) + "\n")
            print(event)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
