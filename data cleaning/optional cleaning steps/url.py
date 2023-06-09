import json
import re

def parse_json_and_divide(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    no_url_conversations = []
    url_conversations = []
    url_values = []

    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )

    for conversation in data:
        contains_url = False

        for message in conversation['conversations']:
            if re.search(url_pattern, message['value']):
                contains_url = True
                url_values.append(message['value'])

        if not contains_url:
            no_url_conversations.append(conversation)

        if contains_url:
            url_conversations.append(conversation)
    
    with open('no_url_conversations.json', 'w') as f:
        json.dump(no_url_conversations, f)

    with open('url_conversations.json', 'w') as f:
        json.dump(url_conversations, f)

    with open('url_values.json', 'w') as f:
        json.dump(url_values, f)

parse_json_and_divide('stage5.json')

