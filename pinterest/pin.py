import requests
from utils import get_env_var
import csv
import os
import utils

columns = [
    "Title",
    "Media URL",
    "Pinterest board",
    "Description",
    "Link",
    "Publish date",
    "Keywords",
]
# Define the folder to save CSV files
folder_path = "csv_files"
os.makedirs(folder_path, exist_ok=True)


def get_next_csv_filename():
    """Generate a new CSV filename based on the existing files in the folder."""
    existing_files = [
        f
        for f in os.listdir(folder_path)
        if f.startswith("data") and f.endswith(".csv")
    ]
    next_index = len(existing_files) + 1
    return os.path.join(folder_path, f"data_{next_index}.csv")


def add_row_to_csv(row_data):
    """
    Add a new row to the latest CSV file. If the file exceeds 200 rows, create a new CSV file.
    """
    # Get the list of existing files
    existing_files = sorted(
        [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith(".csv")
        ]
    )
    current_file = existing_files[-1] if existing_files else get_next_csv_filename()

    # Check the number of rows in the current file
    try:
        with open(current_file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            row_count = sum(1 for row in reader) - 1  # Exclude the header row
    except FileNotFoundError:
        row_count = 0

    # If the current file has 200 rows, create a new file
    if row_count >= 100:
        current_file = get_next_csv_filename()

    # Write the new row to the file
    write_header = not os.path.exists(current_file)
    with open(current_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        if write_header:
            writer.writerow(columns)  # Write the header only if it's a new file
        writer.writerow(row_data)


def get_boards(id):
    boards = [
        {
            "name": "stories",
            "id": "882283451939745557",
            "sections": [
                {"id": "5398508827117151890", "name": "true", "cat_id": 5},
                {
                    "id": "5398508804082025745",
                    "name": "bedtime",
                    "cat_id": 1,
                },
                {"id": "5398508424346526516", "name": "horror", "cat_id": 23},
                {"id": "5398509851036923141", "name": "mystery", "cat_id": 7},
            ],
        },
        {
            "name": "definitions",
            "id": "882283451939745680",
            "sections": [{"name": "English", "id": "5399322510743366593"}],
        },
        {"name": "house", "id": "882283451939747875", "cat_id": 64},
        {"name": "puzzle", "id": "882283451939805214"},
    ]
    board = next((board for board in boards if board["name"] == id), None)
    return board


def fetch_pins_from_board(board_id, section_id):
    """
    Fetch all pins from a Pinterest board, handling pagination using the bookmark value.
    """
    access_token = get_env_var("ACCESS_TOKEN")
    url = f"https://api.pinterest.com/v5/boards/{board_id}/sections/{section_id}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}

    all_pins = []  # To store all pin titles
    bookmark = None  # Bookmark for pagination

    while True:
        params = {"bookmark": bookmark} if bookmark else {}  # Add bookmark if available
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            pins = [{"title": pin.get("title", "")} for pin in data.get("items", [])]
            all_pins.extend(pins)  # Add the pins to the list

            bookmark = data.get("bookmark")  # Get the next bookmark
            if not bookmark:  # Exit loop if no more pages
                break
        else:
            print(f"Failed to fetch pins: {response.status_code} - {response.text}")
            break

    # Save the collected pins to a JSON file
    utils.save_to_json("data/pins.json", all_pins)
    print(f"Fetched {len(all_pins)} pins and saved to data/pins.json")
    return "Done"


def get_pins():
    # Get the access token from the environment variables
    access_token = get_env_var("ACCESS_TOKEN")

    # Define the URL for the GET request
    url = "https://api.pinterest.com/v5/pins"

    # Define the headers, including the authorization header
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 201 or response.status_code == 200:
        return f"Pin listed successfully: {response.json()}"
    else:
        return f"Error creating pin: {response.status_code} - {response.text}"


def create_csv(
    post, description, board_name, section_name=None, publish_date="", keywords=""
):
    # Example usage

    title = post["title"]["rendered"]
    media_url = post["pinterest_media"]
    if section_name is not None:
        board = f"{board_name}/{section_name}"
    else:
        board = f"{board_name}"

    example_row = [
        title,
        media_url,
        board,
        description,
        post["link"],
        publish_date,
        keywords,
    ]
    # Add the example row to the CSV file
    add_row_to_csv(example_row)
    return True
    # access_token = get_env_var("ACCESS_TOKEN")
    # if not access_token:
    #     return "Error: Access token not available."

    # url = "https://api.pinterest.com/v5/pins"
    # headers = {
    #     "Authorization": "Bearer " + access_token,
    #     "Content-Type": "application/json",
    #     "Accept": "application/json",
    # }

    # data = {
    #     "board_id": board_id,
    #     "title": post["title"]["rendered"],
    #     "alt_text": post["title"]["rendered"],
    #     "description": description,
    #     "media_source": {
    #         "source_type": "image_url",
    #         "url": post["pinterest_media"],
    #     },
    #     "link": post["link"],
    # }
    # if section_id is not None:
    #     data["board_section_id"] = section_id
    # response = requests.post(url, headers=headers, json=data)
    # if response.status_code == 201:
    #     # print(f"Pin created successfully: {response.json()}")
    #     return True
    # else:
    #     print(f"Error creating pin: {response.status_code} - {response.text}")
    #     return False


def create_pin(post, description, board_id, section_id=None):
    try:
        access_token = get_env_var("ACCESS_TOKEN")
        if not access_token:
            return "Error: Access token not available."

        url = "https://api.pinterest.com/v5/pins"
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = {
            "board_id": board_id,
            "title": post["title"]["rendered"],
            "alt_text": post["title"]["rendered"],
            "description": description,
            "media_source": {
                "source_type": "image_url",
                "url": post["pinterest_media"],
            },
            "link": post["link"],
        }
        if section_id is not None:
            data["board_section_id"] = section_id
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            # print(f"Pin created successfully: {response.json()}")
            return True
        else:
            print(f"Error creating pin: {response.status_code} - {response.text}")
            return False
    except:
        print("Error occurec in create_pin")
