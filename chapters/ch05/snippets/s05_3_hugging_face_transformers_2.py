from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16,
                         bnb_4bit_quant_type="nf4")
model = AutoModelForCausalLM.from_pretrained("<an-8B-instruct-model>",
                                             quantization_config=bnb, device_map="auto")
