import os
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup
import re


def load_env_vars():
    # Load environment variables from .env file
    load_dotenv()


def save_tokens_to_env(tokens):
    # Load the existing environment variables from .env file
    load_dotenv()

    # Create a dictionary to store the environment variables
    env_vars = {
        "ACCESS_TOKEN": tokens["access_token"],
        "REFRESH_TOKEN": tokens["refresh_token"],
        "EXPIRES_IN": str(tokens["expires_in"]),
    }

    # Read the current .env file content
    try:
        with open(".env", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    # Update or append the tokens in the .env file content
    updated_lines = []
    for line in lines:
        key = line.split("=")[0].strip()
        if key in env_vars:
            # Update the existing token value
            updated_lines.append(f"{key}={env_vars[key]}\n")
            env_vars.pop(key)
        else:
            # Keep the current line
            updated_lines.append(line)

    # Append any remaining new tokens (if they didn't exist in the .env file)
    for key, value in env_vars.items():
        updated_lines.append(f"{key}={value}\n")

    # Write the updated content back to the .env file
    with open(".env", "w") as f:
        f.writelines(updated_lines)


def get_env_var(var_name):
    # Get environment variable value
    return os.getenv(var_name)


def read_existing_ids(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            data = json.load(f)
            return {entry["id"] for entry in data}
    return set()


def write_article_id(file_path, article_id):
    if os.path.exists(file_path):
        with open(file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append({"id": article_id})
            f.seek(0)
            json.dump(data, f, indent=4)
    else:
        with open(file_path, "w") as f:
            json.dump([{"id": article_id}], f, indent=4)


def fromHtml(html_description):
    soup = BeautifulSoup(html_description, "html.parser")
    description = re.sub(r"[“”]", '"', soup.get_text())
    description = re.sub(r"[″]", '"', description)
    return description


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
