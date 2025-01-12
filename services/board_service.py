from typing import Dict, List, Optional


class BoardService:
    @staticmethod
    def get_boards(id: str) -> Optional[Dict]:
        boards = [
            {
                "name": "stories",
                "id": "882283451939745557",
                "sections": [
                    {"id": "5398508827117151890", "name": "true", "cat_id": 5},
                    {"id": "5398508804082025745", "name": "bedtime", "cat_id": 1},
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
        return next((board for board in boards if board["name"] == id), None)
