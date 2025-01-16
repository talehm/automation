from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class HtmlRenderer:
    def __init__(self, driver):
        self.driver = driver

    def load_template(self, html_file_path):
        file_url = f"file:///{os.path.abspath(html_file_path)}"
        self.driver.get(file_url)
        self.driver.implicitly_wait(5)

    def update_css(self, css):
        self.driver.execute_script(
            "var style = document.createElement('style'); style.innerHTML = arguments[0]; document.head.appendChild(style);",
            css,
        )

    def update_element(self, element_id, content):
        self.driver.execute_script(
            "document.getElementById(arguments[0]).innerHTML = arguments[1];",
            element_id,
            content,
        )

    def update_background(self, background_image_url):
        script = f"""
        document.querySelector('.background').style.backgroundImage = "url('{background_image_url}')";
        """
        self.driver.execute_script(script)

    def get_element(self, selector):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("window.scrollBy(0, -window.innerHeight / 2);")
