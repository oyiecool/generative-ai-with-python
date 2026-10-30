# chapters/ch19/pibench.py
import statistics
import subprocess
import time

import ollama
import psutil

PROMPT = "List five checks to perform before rebooting a production Linux server."


def soc_temp() -> float:
    out = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True).stdout
    return float(out.split("=")[1].split("'")[0])          # "temp=54.3'C"


def throttled() -> str:
    return subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True).stdout.strip()


def bench(model: str, runs: int = 3) -> dict:
    ollama.generate(model=model, prompt="hi", options={"num_predict": 1})   # warm-up / load
    tps, ttft = [], []
    for _ in range(runs):
        r = ollama.generate(model=model, prompt=PROMPT, options={"num_predict": 200, "temperature": 0})
        tps.append(r["eval_count"] / (r["eval_duration"] / 1e9))
        ttft.append((r["load_duration"] + r["prompt_eval_duration"]) / 1e9)
    return {
        "model": model,
        "tokens_per_s": round(statistics.median(tps), 2),
        "ttft_s": round(statistics.median(ttft), 2),
        "ram_used_gb": round(psutil.virtual_memory().used / 1e9, 2),
        "temp_c": soc_temp(),
        "throttled": throttled(),
    }


if __name__ == "__main__":
    for m in ["gemma3:1b", "qwen2.5:1.5b", "llama3.2:3b"]:
        print(bench(m))
        time.sleep(30)                                     # let the board cool between models
