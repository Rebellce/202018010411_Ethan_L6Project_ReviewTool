from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Suppressing the logging output of transformers
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize the model and tokenizer
model_name = "Hello-SimpleAI/chatgpt-detector-roberta"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def Start():
    text_to_check = input("Your text to be checked: ")
    # Tokenize the input text and convert to Tensor
    inputs = tokenizer(text_to_check, return_tensors="pt")
    # Get model outputs (logits)
    outputs = model(**inputs)
    # Logits from your model's output
    logits = outputs.logits
    # Calculate probabilities using softmax
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    # Extract probabilities for human and GPT
    prob_human = probabilities[0][0].item()
    prob_gpt = probabilities[0][1].item()
    # Format the output
    formatted_output = f"Human: {prob_human * 100:.2f}%, GPT: {prob_gpt * 100:.2f}%"
    return formatted_output


if __name__ == '__main__':
    while True:
        print(Start())
        print("\n")
