import json
import os


def save_to_json(file_path, data):
    try:
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        else:
            # Create a new file and write the first ID
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
    except FileNotFoundError:
        return []


def load_from_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

    except FileNotFoundError:
        return []


def filter_by_title(filter_file, main_file, output_file):
    pins = load_from_json(filter_file)
    definitions = load_from_json(main_file)

    pin_titles = {pin["title"] for pin in pins}
    filtered_definitions = [
        definition
        for definition in definitions
        if definition["title"] not in pin_titles
    ]

    save_to_json(output_file, filtered_definitions)
