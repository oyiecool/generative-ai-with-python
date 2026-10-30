import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

NAME = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(NAME)
QUESTIONS = ["What does chmod 640 do?", "Explain inode exhaustion.", "What is a zombie process?",
             "How does logrotate work?", "What is SELinux enforcing mode?"]


def run(quant: bool):
    torch.cuda.reset_peak_memory_stats()
    cfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16) if quant else None
    model = AutoModelForCausalLM.from_pretrained(NAME, device_map="cuda", torch_dtype=torch.bfloat16,
                                                 quantization_config=cfg)
    answers, t0 = [], time.perf_counter()
    for q in QUESTIONS:
        ids = tok.apply_chat_template([{"role": "user", "content": q}], add_generation_prompt=True,
                                      return_tensors="pt").to("cuda")
        out = model.generate(ids, max_new_tokens=120, do_sample=False)
        answers.append(tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True))
    return torch.cuda.max_memory_allocated() / 1e9, time.perf_counter() - t0, answers


for quant in (False, True):
    mem, secs, ans = run(quant)
    print(f"4-bit={quant}: peak {mem:.1f} GB, {secs:.1f}s")
