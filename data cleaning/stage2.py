import json

def split_and_check_from_field(json_path):
    # Load the processed JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Prepare the lists to hold different types of conversations
    tool_conversations = []
    non_tool_conversations = []
    tool_outputs = []

    # Iterate through each conversation
    for conversation in data:
        # Prepare temporary lists to hold different types of messages
        tool_messages = []
        non_tool_messages = []

        # Iterate through each message in the conversation
        for message in conversation['conversations']:
            # Check the "from" field
            if message['from'] == 'tool':
                tool_messages.append(message)
                tool_outputs.append({
                    'id': conversation['id'],
                    'conversations': [message]
                })
            else:
                non_tool_messages.append(message)

        # Add the conversation to the appropriate list(s)
        if tool_messages:
            tool_conversations.append({
                'id': conversation['id'],
                'conversations': tool_messages
            })
        if non_tool_messages:
            non_tool_conversations.append({
                'id': conversation['id'],
                'conversations': non_tool_messages
            })

    # Save the lists to separate JSON files
    with open('tool_conversations.json', 'w') as file:
        json.dump(tool_conversations, file)
    with open('stage2process.json', 'w') as file:
        json.dump(non_tool_conversations, file)
    with open('tool_outputs.json', 'w') as file:
        json.dump(tool_outputs, file)

# Split the conversations based on the "from" field in the processed JSON file
split_and_check_from_field('stage1process.json')

