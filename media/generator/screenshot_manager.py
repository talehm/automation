from PIL import Image
import io


class ScreenshotManager:
    def __init__(self, driver):
        self.driver = driver

    def capture_element(self, element):
        original_size = self.driver.get_window_size()
        location = element.location
        size = element.size
        # Set window size to element dimensions
        self.driver.set_window_size(size["width"] + 200, size["height"] + 200)

        # Take screenshot
        png = self.driver.get_screenshot_as_png()

        # Restore window size
        self.driver.set_window_size(original_size["width"], original_size["height"])

        return Image.open(io.BytesIO(png)), location, size

    def save_element_image(self, element, output_path):
        full_image, location, size = self.capture_element(element)

        # Crop image to element dimensions
        box = (
            location["x"],
            location["y"],
            location["x"] + size["width"],
            location["y"] + size["height"],
        )
        element_image = full_image.crop(box)

        # Save image
        full_path = os.path.abspath(output_path)
        element_image.save(full_path)
        return full_path
