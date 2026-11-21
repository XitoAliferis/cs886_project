from transformers import AutoModelForCausalLM, AutoTokenizer

class Runner:
    def __init__(self, model):
        self.model = AutoModelForCausalLM.from_pretrained(model, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.tokenizer.padding_side = "left"

    def run(self, inputs, thinking=True, max_new_tokens=512):

        messages = [
            [{
                "role": "user",
                "content": i
            }] for i in inputs
        ]

        text = [self.tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True, enable_thinking=thinking) for m in messages]
        model_inputs = self.tokenizer(text, padding=True, add_special_tokens=False, return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens
        )
        
        for i in range(len(inputs)):
            output_ids = generated_ids[i][len(model_inputs.input_ids[i]):].tolist()

            thinking_token = self.tokenizer.convert_tokens_to_ids("</think>")

            try:
                index = len(output_ids) - output_ids[::-1].index(thinking_token)
            except ValueError:
                index = 0

            thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True)
            content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True)

            print("thinking content:", thinking_content)
            print("content:", content)
