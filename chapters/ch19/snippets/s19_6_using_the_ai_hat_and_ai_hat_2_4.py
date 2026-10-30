from ollama import Client

hailo = Client(host="http://localhost:8000")
r = hailo.chat(model="qwen2:1.5b", messages=[{"role": "user", "content": "Summarise RAID 1 in one line."}])
print(r["message"]["content"])
