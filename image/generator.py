from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import random
from bs4 import BeautifulSoup
import json
from utils import fromHtml
import re
import os
import io
import codecs


class HTMLScreenshotter:
    def __init__(self, driver_path="./chromedriver.exe"):
        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Start the Chrome WebDriver
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def load_html_template(self, html_file_path):
        """Load the HTML file."""
        file_url = f"file:///{os.path.abspath(html_file_path)}"
        self.driver.get(file_url)
        self.driver.implicitly_wait(5)

    def update_css(self, css):
        """Update the CSS of the loaded HTML."""
        self.driver.execute_script(
            "var style = document.createElement('style'); style.innerHTML = arguments[0]; document.head.appendChild(style);",
            css,
        )

    def update_element_content(self, element_id, new_content):
        """Update the content of a specific element by ID."""
        self.driver.execute_script(
            "document.getElementById(arguments[0]).innerHTML = arguments[1];",
            element_id,
            new_content,
        )

    def update_title(self, new_title):
        """Update the title content."""
        self.update_element_content("title", new_title)

    def update_pro(self, pro):
        """Update the title content."""
        self.update_element_content("pro", pro)

    def update_definition_type(self, type):
        """Update the title content."""
        self.update_element_content("type", type)

    def update_paragraph(self, new_paragraph):
        """Update the paragraph content."""
        self.update_element_content("paragraph", new_paragraph)

    def update_background(self, background_image_url=None):
        # print(background_image_url, "background_image_url")
        """Injects dynamic background image for .background and color for #main."""
        script = f"""
        document.querySelector('.background').style.backgroundImage = "url('{background_image_url}')";
        """
        self.driver.execute_script(script)

    def scroll_to_element(self, element):
        """Scrolls to the element to ensure it's fully visible."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script(
            "window.scrollBy(0, -window.innerHeight / 2);"
        )  # Adjust as needed

    def full_element_screenshot(self, element):
        """Captures a screenshot of the entire element regardless of viewport size."""
        original_size = self.driver.get_window_size()

        # Get the element's location and size
        location = element.location
        size = element.size

        # Scroll to the element
        self.scroll_to_element(element)

        # Set the window size to the full dimensions of the element
        self.driver.set_window_size(size["width"] + 200, size["height"] + 200)

        # Take the screenshot
        png = self.driver.get_screenshot_as_png()

        # Restore the original window size
        self.driver.set_window_size(original_size["width"], original_size["height"])

        return Image.open(io.BytesIO(png)), location, size

    def element_to_image(self, output_image_path, element_selector):
        """Capture the element as an image."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )
        except Exception as e:
            print(f"Error locating element: {e}")
            return

        # Get the full element screenshot
        full_image, location, size = self.full_element_screenshot(element)

        # Define the cropping box (left, upper, right, lower)
        left = location["x"]
        upper = location["y"]
        right = left + size["width"]
        lower = upper + size["height"]
        box = (left, upper, right, lower)

        # Crop the image to the element
        element_image = full_image.crop(box)

        # Save the image using the full path
        full_path = os.path.abspath(output_image_path)
        element_image.save(full_path)
        print(f"Image saved to {full_path}")

        return full_path

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()

    def load_css_from_file(self, css_file_path):
        """Load CSS from an external file."""
        with open(css_file_path, "r") as css_file:
            return css_file.read()


def replace_unicode_matches(match):
    # Get the hexadecimal number (e.g., '026a')
    hex_code = match.group(1)

    # Convert it to an integer (base 16) and get the corresponding Unicode character
    return chr(int(hex_code, 16))


def run(template_folder, post, style=None, type="post", word=None):
    screenshotter = HTMLScreenshotter()

    # Path to your HTML file
    template = os.path.join(
        template_folder, "template.html"
    )  # Build the path using the template_folder variable
    output_image_path = "element_image.png"  # Specify the desired output image path
    # Load HTML template
    screenshotter.load_html_template(template)

    # Load custom CSS from an external file
    if style is None:
        css_folder = os.path.join(
            template_folder, "styles"
        )  # Build the path for the CSS file
        styles = [file for file in os.listdir(css_folder) if file.endswith(".css")]
        if not styles:
            print("No CSS files found in the folder.")
            return
        chosen_style = random.choice(styles)  # Choose a random CSS file
        css_file_path = os.path.join(css_folder, chosen_style)
    else:
        css_file_path = os.path.join(template_folder, "styles/style1.css")

    custom_css = screenshotter.load_css_from_file(css_file_path)

    # Apply the custom CSS
    screenshotter.update_css(custom_css)
    # Update title and paragraph content
    if type == "post":
        screenshotter.update_title(post["title"]["rendered"])
        screenshotter.update_paragraph(post["excerpt"]["rendered"])
    elif type == "riddle":
        # screenshotter.update_title(post["title"]["rendered"])
        screenshotter.update_paragraph(post["riddle"])
    elif type == "definition":
        content = fromHtml(post["content"]["rendered"])
        content = json.loads(content)
        screenshotter.update_title(content["word"])
        screenshotter.update_paragraph(word["definition"])
        # pronunciation = (
        #     "["
        #     + re.sub(
        #         r"([0-9a-fA-F]{4})",
        #         replace_unicode_matches,
        #         content["pronunciation"]["all"],
        #     )
        #     + "]"
        # )
        # screenshotter.update_pro(pronunciation)
        screenshotter.update_definition_type(word["partOfSpeech"])
    if "media" in post:
        print(post["media"]["source_url"])
        screenshotter.update_background(
            background_image_url=post["media"][
                "source_url"
            ]  # Dynamic background image URL
        )
    else:
        print("no media found")
    # Capture the element as an image
    image_url = screenshotter.element_to_image(output_image_path, "#main")

    # Clean up
    screenshotter.close()
    return image_url
