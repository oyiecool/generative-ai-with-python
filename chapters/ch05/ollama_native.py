# chapters/ch05/ollama_native.py
import ollama

resp = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Give three causes of high iowait."}],
    options={"temperature": 0.2, "num_ctx": 8192},
)
print(resp["message"]["content"])
