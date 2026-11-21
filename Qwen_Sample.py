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

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
) # passes in the input token IDs (not embeddings), and outputs the resulting token IDs from the model (unembedded back to IDs for us already)

for i in range(len(messages)):
    print("prompt: ", messages[i]
    )
    output_ids = generated_ids[i][len(model_inputs.input_ids[i]):].tolist() #getting the outputs only (it appends the input/output during the transformer modelling, so we slice the output part out    )

    think_end_id = tokenizer.convert_tokens_to_ids("<|/think|>")

    try:
        index = len(output_ids) - output_ids[::-1].index(think_end_id) #finds the index of <|/think|> that ends the thinking portion
    except ValueError:
        index = 0 

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True)
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True)

    print("thinking: ", thinking_content)
    print("content: ", content)




