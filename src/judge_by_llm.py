import json
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

def polarity_classifier_by_llm(post) -> str:
    messages = [
        {"role": "system", "content": "受け取った短文に対してポジティブかネガティブかの判定を行ってください。ポジティブなら'pos'、ネガティブなら'neg'をラベルとして返してください"},
        {"role": "user", "content": post}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=10,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response.strip()


if __name__ == "__main__":    
    result = {}

    with open("data/posts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        posts = list(data.keys())

    for post in posts:
        label = polarity_classifier_by_llm(post)
        result[post] = label

    with open("output/result_by_llm2.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)