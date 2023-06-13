import json

def parse_json_and_divide(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    no_hrp_conversations = []
    only_hrp_conversations = []
    hrp_conversations = []

    for conversation in data:
        contains_hrp = False
        only_hrp = True

        for message in conversation['conversations']:
            if '[hrp]' in message['value']:
                contains_hrp = True
            else:
                only_hrp = False

        if not contains_hrp:
            no_hrp_conversations.append(conversation)
        elif only_hrp:
            only_hrp_conversations.append(conversation)
        
        if contains_hrp:
            hrp_conversations.append(conversation)
    
    with open('no_hrp_conversations.json', 'w') as f:
        json.dump(no_hrp_conversations, f)

    with open('only_hrp_conversations.json', 'w') as f:
        json.dump(only_hrp_conversations, f)

    with open('hrp_conversations.json', 'w') as f:
        json.dump(hrp_conversations, f)

parse_json_and_divide('non_tool_conversations.json')

