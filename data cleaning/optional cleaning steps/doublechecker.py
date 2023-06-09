import json
import os

filename = 'stage7.json'

def analyze_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    num_conversations = len(data)
    print(f'Number of conversations: {num_conversations}')

    if num_conversations > 0:
        print('First conversation:')
        print(json.dumps(data[0], indent=4))

    return data

# Get current working directory
cwd = os.getcwd()

# Full path to the file
path_to_file = os.path.join(cwd, filename)

# Analyze the file
analyze_json(path_to_file)

