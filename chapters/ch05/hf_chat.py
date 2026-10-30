# chapters/ch05/hf_chat.py
import torch
from transformers import pipeline

MODEL = "Qwen/Qwen2.5-1.5B-Instruct"   # small, permissively licensed; swap freely

generator = pipeline(
    "text-generation",
    model=MODEL,
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",          # GPU if available, otherwise CPU
)

messages = [
    {"role": "system", "content": "You are a concise Linux tutor."},
    {"role": "user", "content": "What does `chmod 640 file` do?"},
]
out = generator(messages, max_new_tokens=150, do_sample=True, temperature=0.3)
print(out[0]["generated_text"][-1]["content"])
