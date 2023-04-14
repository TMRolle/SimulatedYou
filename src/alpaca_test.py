from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("chainyo/alpaca-lora-7b")

model = AutoModelForCausalLM.from_pretrained("chainyo/alpaca-lora-7b")
