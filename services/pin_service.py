import requests
# from utils_old import get_env_var
from utils.env_manager import EnvManager
from utils.file_handler import JsonFileHandler
from typing import Dict, List, Optional


class PinService:
    def __init__(self):
        self.base_url = "https://api.pinterest.com/v5"
        self.access_token = EnvManager.get_env_var("ACCESS_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_pin_from_db(
        self,
        link: str,
        title: str,
        description: str,
        media_url: str,
        board_id: str,
        alt_text: str,
        keywords: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> bool:
        try:
            data = {
                "board_id": str(board_id),
                "title": title,
                "alt_text": alt_text,
                "description": description,
                "media_source": {
                    "source_type": "image_url",
                    "url": media_url,
                },
                "link": link,
            }
            if section_id:
                data["board_section_id"] = section_id

            response = requests.post(
                f"{self.base_url}/pins", headers=self.headers, json=data
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error creating pin: {str(e)}")
            return False

    def create_pin(
        self,
        post: Dict,
        description: str,
        board_id: str,
        section_id: Optional[str] = None,
    ) -> bool:
        try:
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
            if section_id:
                data["board_section_id"] = section_id

            response = requests.post(
                f"{self.base_url}/pins", headers=self.headers, json=data
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error creating pin: {str(e)}")
            return False

    def get_pins(self) -> Dict:
        response = requests.get(f"{self.base_url}/pins", headers=self.headers)
        if response.ok:
            return response.json()
        return {"error": f"Error: {response.status_code} - {response.text}"}

    def fetch_pins_from_board(self, board_id: str, section_id: str = None) -> str:
        if section_id is None:
            url = f"{self.base_url}/boards/{board_id}/pins"
        else:
            url = f"{self.base_url}/boards/{board_id}/sections/{section_id}/pins"
        all_pins = []
        bookmark = None

        while True:
            params = {"bookmark": bookmark} if bookmark else {}
            response = requests.get(url, headers=self.headers, params=params)

            if response.ok:
                data = response.json()
                pins = [
                    {"title": pin.get("title", "")} for pin in data.get("items", [])
                ]
                all_pins.extend(pins)
                bookmark = data.get("bookmark")
                if not bookmark:
                    break
            else:
                print(f"Failed to fetch pins: {response.status_code} - {response.text}")
                break
        file_handler = JsonFileHandler("data/pins.json")
        file_handler.write(all_pins)
        print(f"Fetched {len(all_pins)} pins and saved to data/pins.json")
        return "Done"
