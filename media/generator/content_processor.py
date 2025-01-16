import json
import re
from utils.html_processor import HtmlProcessor


class ContentProcessor:
    @staticmethod
    def process_post_content(post):
        return {
            "title": post["title"]["rendered"],
            "paragraph": post["excerpt"]["rendered"],
        }

    @staticmethod
    def process_riddle_content(post):
        return {"paragraph": post["riddle"]}

    @staticmethod
    def process_definition_content(post, word):
        content = HtmlProcessor.fromHtml(post["content"]["rendered"])
        content = json.loads(content)
        return {
            "title": content["word"],
            "paragraph": word["definition"],
            "type": word["partOfSpeech"],
        }

    @staticmethod
    def get_background_image(post):
        return post.get("media", {}).get("source_url")
