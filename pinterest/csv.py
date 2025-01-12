import csv
import os

# Define the column names
columns = [
    "Title",
    "Video URL",
    "Pinterest board",
    "Thumbnail",
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
    if row_count >= 200:
        current_file = get_next_csv_filename()

    # Write the new row to the file
    write_header = not os.path.exists(current_file)
    with open(current_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(columns)  # Write the header only if it's a new file
        writer.writerow(row_data)


# Example usage
example_row = [
    "Sample Title",
    "https://example.com/video",
    "Sample Board",
    "https://example.com/thumbnail.jpg",
    "Sample description",
    "https://example.com",
    "2024-11-24",
    "keyword1, keyword2",
]

# Add the example row to the CSV file
add_row_to_csv(example_row)
