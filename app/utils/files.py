import json
from pathlib import Path

def json_to_dict(file_name: Path) -> dict:
    try:
        with open(file_name, 'r') as file:
            dic = json.load(file)
            return dic
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file {file_name}.")
