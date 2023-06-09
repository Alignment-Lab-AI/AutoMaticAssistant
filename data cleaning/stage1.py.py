import ijson
import json
from decimal import Decimal
import subprocess

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def handle_content(content):
    if isinstance(content, dict):
        if 'text' in content:
            return content['text']
        elif 'parts' in content:
            return ' '.join(handle_content(part) for part in content['parts'])
        else:
            return json.dumps(content, indent=2, cls=DecimalEncoder)
    elif isinstance(content, list):
        return ' '.join(handle_content(item) for item in content)
    else:
        return str(content)

def extract_conversations(json_path):
    conversations = []

    with open(json_path, 'r') as file:
        objects = ijson.items(file, 'item')
        for obj in objects:
            conversation = []
            for message_id, message in obj['mapping'].items():
                try:
                    if message is None or message['message'] is None:
                        continue

                    if isinstance(message, dict) and 'message' in message:
                        if 'author' in message['message'] and 'role' in message['message']['author']:
                            author_role = message['message']['author']['role']
                        else:
                            print("Unexpected structure for 'author' in message")
                            print(json.dumps(message, indent=2, cls=DecimalEncoder))
                            continue

                        if 'content' in message['message']:
                            content = handle_content(message['message']['content'])
                            conversation.append({
                                'from': author_role,
                                'value': content
                            })
                        else:
                            print("Unexpected structure for message")
                            print(json.dumps(message, indent=2, cls=DecimalEncoder))
                            continue
                    else:
                        print("Unexpected structure for message")
                        print(json.dumps(message, indent=2, cls=DecimalEncoder))

                except Exception as e:
                    print(f"Unexpected error for message: {message}")
                    print(f"Error: {str(e)}")
                    continue

            conversations.append({
                'id': obj['id'],
                'conversations': conversation
            })

    return conversations

# Extract conversations from the JSON file
conversations = extract_conversations('conversations.json')

# Open a new JSON file and write the data to it
with open('stage1process.json', 'w') as f:
    json.dump(conversations, f, cls=DecimalEncoder)

# After all the main processing is done, start the other scripts
subprocess.run(["python", "stage2.py"])
subprocess.run(["python", "tokenresort.py"])

