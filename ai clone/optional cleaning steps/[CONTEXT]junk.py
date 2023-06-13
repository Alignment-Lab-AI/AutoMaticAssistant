import json

def parse_json_and_divide(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    no_context_conversations = []
    context_conversations = []
    context_values = []

    for conversation in data:
        contains_context = False

        for message in conversation['conversations']:
            if '[CONTEXT]' in message['value']:
                contains_context = True
                context_values.append(message['value'])

        if not contains_context:
            no_context_conversations.append(conversation)

        if contains_context:
            context_conversations.append(conversation)
    
    with open('no_context_conversations.json', 'w') as f:
        json.dump(no_context_conversations, f)

    with open('context_conversations.json', 'w') as f:
        json.dump(context_conversations, f)

    with open('context_values.json', 'w') as f:
        json.dump(context_values, f)

parse_json_and_divide('stage3.json')

