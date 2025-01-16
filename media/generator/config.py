from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebDriverConfig:
    @staticmethod
    def create_chrome_driver(driver_path="./chromedriver.exe"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)
