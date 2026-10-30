# chapters/ch03/tokens.py
# uv add tiktoken transformers
import tiktoken
from transformers import AutoTokenizer

text = "Patch CVE-2024-3094 on all xz-utils hosts before Friday's change window."

enc = tiktoken.get_encoding("o200k_base")
ids = enc.encode(text)
print(len(ids), "tokens (o200k_base)")
print([enc.decode([i]) for i in ids])

hf_tok = AutoTokenizer.from_pretrained("gpt2")
print(len(hf_tok.encode(text)), "tokens (gpt2)")
print(hf_tok.tokenize(text))
