short = "Summarise: " + "The backup completed. " * 20          # ~200 tokens
long = "Summarise: " + "The backup completed. " * 200          # ~2,000 tokens
for label, p in (("short", short), ("long", long)):
    r = ollama.generate(model="qwen2.5:1.5b", prompt=p, options={"num_predict": 50})
    print(label, "prompt tokens:", r["prompt_eval_count"],
          "TTFT:", round(r["prompt_eval_duration"] / 1e9, 2), "s",
          "prompt tok/s:", round(r["prompt_eval_count"] / (r["prompt_eval_duration"] / 1e9), 1))
