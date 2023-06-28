from transformers import AutoTokenizer
from datasets import load_dataset
import logging

logging.basicConfig(level=logging.INFO)

# Load dataset and tokenizer
dataset = load_dataset('csebuetnlp/squad_bn')
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")

# Log the dataset structure
logging.info(f"Dataset Structure: {dataset}")

# Encoding function
def encode(examples):
    inputs = []
    answers = []
    for question, context, answer in zip(examples['question'], examples['context'], examples['answers']):
        input_str = f"question: {question}  context: {context}"
        inputs.append(input_str)
        # As 'answers' is a list of dicts, we need to handle cases where it might be empty.
        if answer['text']:
            answers.append(answer['text'][0])
        else:
            answers.append('')
    # Log the first input and answer after processing
    if inputs:
        logging.info(f"First processed input: {inputs[0]}")
    if answers:
        logging.info(f"First processed answer: {answers[0]}")

    # Tokenize inputs and answers
    tokenized_inputs = tokenizer(inputs, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
    tokenized_answers = tokenizer(answers, truncation=True, padding='max_length', max_length=512, return_tensors='pt')

    # The model expects the 'labels' field to be the ids of the tokenized answers
    tokenized_inputs["labels"] = tokenized_answers.input_ids

    return tokenized_inputs

# Map the encoding function to the dataset
dataset = dataset.map(encode, batched=True)