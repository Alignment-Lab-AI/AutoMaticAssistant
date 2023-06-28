import json

def load_input_data(file_path: str):
    with open(file_path, 'r') as file:
        input_data = json.load(file)
    return input_data

def display_keys(input_data):
    keys = list(input_data[0].keys())
    print("Available keys:")
    for i, key in enumerate(keys):
        print(f"{i + 1}. {key}")
    return keys

def get_user_choices(keys):
    print("Enter the numbers corresponding to the keys you want to use, separated by spaces:")
    user_input = input()
    selected_keys = [keys[int(i) - 1] for i in user_input.split()]
    
    output_keys = []
    for key in selected_keys:
        print(f"Select the output name for '{key}':")
        print("1. Use the same name")
        print("2. Enter a custom name")
        choice = int(input())
        if choice == 1:
            output_keys.append(key)
        elif choice == 2:
            custom_name = input("Enter the custom name: ")
            output_keys.append(custom_name)
    return selected_keys, output_keys

def reshape_data(input_data, selected_keys, output_keys):
    reshaped_data = []
    for index, item in enumerate(input_data):
        reshaped_item = {"id": index, "conversations": []}
        for selected_key, output_key in zip(selected_keys, output_keys):
            conversation = {"from": output_key, "value": item[selected_key]}
            reshaped_item["conversations"].append(conversation)
        reshaped_data.append(reshaped_item)
    return reshaped_data

def save_reshaped_data(reshaped_data, output_file_path: str):
    with open(output_file_path, 'w') as file:
        json.dump(reshaped_data, file)

def main():
    input_file_path = "input.json"
    output_file_path = "output.json"

    input_data = load_input_data(input_file_path)
    keys = display_keys(input_data)
    selected_keys, output_keys = get_user_choices(keys)
    reshaped_data = reshape_data(input_data, selected_keys, output_keys)
    save_reshaped_data(reshaped_data, output_file_path)
    print("Reshaping process is complete. The new JSON file has been created.")

if __name__ == "__main__":
    main()
