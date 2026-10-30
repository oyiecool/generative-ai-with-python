import pandas as pd

rows = [bench(m) for m in ("gemma3:1b", "qwen2.5:1.5b", "llama3.2:3b")]
print(pd.DataFrame(rows).to_markdown(index=False))
