import csv
import os
from typing import List, Optional


class CSVService:
    def __init__(self):
        self.columns = [
            "Title",
            "Media URL",
            "Pinterest board",
            "Description",
            "Link",
            "Publish date",
            "Keywords",
        ]
        self.folder_path = "csv_files"
        os.makedirs(self.folder_path, exist_ok=True)

    def get_next_csv_filename(self) -> str:
        existing_files = [
            f
            for f in os.listdir(self.folder_path)
            if f.startswith("data") and f.endswith(".csv")
        ]
        next_index = len(existing_files) + 1
        return os.path.join(self.folder_path, f"data_{next_index}.csv")

    def add_row_to_csv(self, row_data: List) -> None:
        existing_files = sorted(
            [
                os.path.join(self.folder_path, f)
                for f in os.listdir(self.folder_path)
                if f.endswith(".csv")
            ]
        )
        current_file = (
            existing_files[-1] if existing_files else self.get_next_csv_filename()
        )

        try:
            with open(current_file, "r", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                row_count = sum(1 for row in reader) - 1
        except FileNotFoundError:
            row_count = 0

        if row_count >= 100:
            current_file = self.get_next_csv_filename()

        write_header = not os.path.exists(current_file)
        with open(current_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            if write_header:
                writer.writerow(self.columns)
            writer.writerow(row_data)

    def create_csv(
        self,
        post: dict,
        description: str,
        board_name: str,
        section_name: Optional[str] = None,
        publish_date: str = "",
        keywords: str = "",
    ) -> bool:
        title = post["title"]["rendered"]
        media_url = post["pinterest_media"]
        board = f"{board_name}/{section_name}" if section_name else board_name

        row_data = [
            title,
            media_url,
            board,
            description,
            post["link"],
            publish_date,
            keywords,
        ]
        self.add_row_to_csv(row_data)
        return True
