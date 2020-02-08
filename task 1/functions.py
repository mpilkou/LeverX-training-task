import json

def print_json_file(path):
    with open(path, "r") as file: 
        data = json.load(file)
        print(data)
