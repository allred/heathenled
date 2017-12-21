import json

def load_file_json(path="data/user_actions"):
    with open(path, "r") as infile:
        return json.load(infile)
