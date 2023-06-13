import json

def parse_json_and_divide(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    no_context_memories_conversations = []
    context_memories_conversations = []
    context_memories_values = []

    for conversation in data:
        contains_context_memories = False

        for message in conversation['conversations']:
            if '[CONTEXT & MEMORIES]' in message['value']:
                contains_context_memories = True
                context_memories_values.append(message['value'])

        if not contains_context_memories:
            no_context_memories_conversations.append(conversation)

        if contains_context_memories:
            context_memories_conversations.append(conversation)
    
    with open('no_context_memories_conversations.json', 'w') as f:
        json.dump(no_context_memories_conversations, f)

    with open('context_memories_conversations.json', 'w') as f:
        json.dump(context_memories_conversations, f)

    with open('context_memories_values.json', 'w') as f:
        json.dump(context_memories_values, f)

parse_json_and_divide('stage4.json')

