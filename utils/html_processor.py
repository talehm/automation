from bs4 import BeautifulSoup
import re


class HtmlProcessor:
    @staticmethod
    def from_html(html_description: str) -> str:
        soup = BeautifulSoup(html_description, "html.parser")
        description = re.sub(r"[" "]", '"', soup.get_text())
        description = re.sub(r"[″]", '"', description)
        return description
