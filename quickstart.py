from transformers import AutoModelForCausalLM, AutoTokenizer


model_name = "Qwen/Qwen3-0.6B"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

prompt = "Explain to me in two sentences how the transformer model works"

messages = [
    [{
        "role": "user",
        "content": prompt
    }],
    [{
        "role": "user",
        "content": "second prompt test"
    }]
]

text = [tokenizer.apply_chat_template(
    m,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True
) for m in messages]

tokenizer.padding_side = "left" # ARMs are left to right, so padding on the right would mean a prediction could be incorrect

model_inputs = tokenizer(
    text, 
    padding=True,
    add_special_tokens=False,
    return_tensors="pt"
).to(model.device)

outputs = model(**model_inputs)

print(model_inputs)
