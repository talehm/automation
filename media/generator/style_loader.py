import os
import random


class StyleLoader:
    @staticmethod
    def load_style(template_folder, style=None):
        if style is None:
            css_folder = os.path.join(template_folder, "styles")
            styles = [f for f in os.listdir(css_folder) if f.endswith(".css")]
            if not styles:
                raise ValueError("No CSS files found in the folder.")
            chosen_style = random.choice(styles)
            css_path = os.path.join(css_folder, chosen_style)
        else:
            css_path = os.path.join(template_folder, "styles/style1.css")

        with open(css_path, "r") as css_file:
            return css_file.read()
