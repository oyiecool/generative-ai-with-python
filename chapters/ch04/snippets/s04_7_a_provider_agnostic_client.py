from aikit.llm import LLM

llm = LLM()
r = llm.chat("Summarise the purpose of a CAB in two sentences.", system="Be precise.")
print(r.text, r.input_tokens, r.output_tokens, f"{r.latency_s:.2f}s")

for piece in LLM(provider="ollama", model="llama3.2").stream("Name three log rotation tools."):
    print(piece, end="")
