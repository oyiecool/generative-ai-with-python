# chapters/ch13/compare.py
from peft import PeftModel
from transformers import AutoModelForCausalLM, pipeline

base = AutoModelForCausalLM.from_pretrained(BASE, device_map="auto", torch_dtype=torch.bfloat16)
tuned = PeftModel.from_pretrained(base, "out/cab-lora/final")
gen = pipeline("text-generation", model=tuned, tokenizer=tokenizer)

for ex in eval_rows[:20]:
    prompt = ex["messages"][:-1]
    out = gen(prompt, max_new_tokens=400, do_sample=False)[0]["generated_text"][-1]["content"]
    score = grade(out, reference=ex["messages"][-1]["content"])   # Chapter 14 grader
    print(score)
