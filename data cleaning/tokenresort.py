import json
import nltk

def load_conversations(json_path):
    with open(json_path, 'r') as file:
        conversations = json.load(file)
    return conversations

def save_conversations(conversations, json_path):
    with open(json_path, 'w') as file:
        json.dump(conversations, file)

def get_token_count(conversation):
    token_count = 0
    for message in conversation['conversations']:
        tokens = nltk.word_tokenize(message['value'])
        token_count += len(tokens)
    return token_count

def sort_conversations_by_token_count(conversations):
    return sorted(conversations, key=get_token_count)

# Load conversations
conversations = load_conversations('stage6.json')

# Sort conversations by token count
sorted_conversations = sort_conversations_by_token_count(conversations)

# Save sorted conversations
save_conversations(sorted_conversations, 'stage7.json')

