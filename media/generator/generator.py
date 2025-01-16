from .config import WebDriverConfig
from .html_renderer import HtmlRenderer
from .screenshot_manager import ScreenshotManager
from .content_processor import ContentProcessor
from .style_loader import StyleLoader
import os


class ImageGenerator:
    def __init__(self):
        self.driver = WebDriverConfig.create_chrome_driver()
        self.renderer = HtmlRenderer(self.driver)
        self.screenshot_manager = ScreenshotManager(self.driver)

    def generate(
        self, template_folder, post, style=None, content_type="post", word=None
    ):
        try:
            # Load template
            template_path = os.path.join(template_folder, "template.html")
            self.renderer.load_template(template_path)
            # Apply CSS
            css = StyleLoader.load_style(template_folder, style)
            self.renderer.update_css(css)
            # Process content based on type
            if content_type == "post":
                content = ContentProcessor.process_post_content(post)
            elif content_type == "riddle":
                content = ContentProcessor.process_riddle_content(post)
            elif content_type == "definition":
                content = ContentProcessor.process_definition_content(post, word)
            # Update content
            for key, value in content.items():
                self.renderer.update_element(key, value)
            # Update background if available
            background_url = ContentProcessor.get_background_image(post)
            if background_url:
                self.renderer.update_background(background_url)
            # Capture and save image
            element = self.renderer.get_element("#main")
            output_path = "element_image.png"
            return self.screenshot_manager.save_element_image(element, output_path)
        finally:
            self.driver.quit()


def run(template_folder, post, style=None, type="post", word=None):
    generator = ImageGenerator()
    return generator.generate(template_folder, post, style, type, word)
