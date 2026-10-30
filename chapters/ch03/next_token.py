# chapters/ch03/next_token.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

name = "gpt2"   # tiny and old, but fully inspectable
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name).eval()

prompt = "Before applying the patch, always take a"
inputs = tok(prompt, return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits[0, -1]       # scores for the next token

probs = torch.softmax(logits, dim=-1)
top = torch.topk(probs, 8)
for p, i in zip(top.values, top.indices):
    print(f"{tok.decode(i)!r:>12}  {p.item():.3f}")
