# chapters/ch13/train_lora.py
import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

BASE = "Qwen/Qwen2.5-7B-Instruct"     # any instruct model whose licence permits fine-tuning

tokenizer = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(
    BASE,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=BitsAndBytesConfig(            # QLoRA: 4-bit frozen base
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
    ),
)

data = load_dataset("json", data_files={"train": "data/cab_train.jsonl",
                                        "eval": "data/cab_eval.jsonl"})

peft_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
)

args = SFTConfig(
    output_dir="out/cab-lora",
    num_train_epochs=2,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,          # effective batch size 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=50,
    bf16=True,
    max_length=2048,
    assistant_only_loss=True,               # learn from answers, not from prompts
    report_to="none",
    seed=7,
)

trainer = SFTTrainer(model=model, args=args, train_dataset=data["train"],
                     eval_dataset=data["eval"], processing_class=tokenizer,
                     peft_config=peft_config)
trainer.train()
trainer.save_model("out/cab-lora/final")     # saves only the adapter
