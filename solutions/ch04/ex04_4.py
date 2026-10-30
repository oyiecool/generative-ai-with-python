import time

prompt = "Write about 400 words explaining RAID levels 0, 1, 5, 6 and 10."

t0 = time.perf_counter()
llm.chat(prompt, max_tokens=600)
full = time.perf_counter() - t0

t0, first = time.perf_counter(), None
for piece in llm.stream(prompt):
    if first is None:
        first = time.perf_counter() - t0
streamed_total = time.perf_counter() - t0
print(f"non-streaming: {full:.2f}s | streaming TTFT: {first:.2f}s, total {streamed_total:.2f}s")
