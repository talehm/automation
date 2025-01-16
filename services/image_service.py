from dropbox import (
    DropboxConfig,
    DropboxUploader,
    DropboxLinkGenerator,
    DropboxUrlFormatter,
)
from typing import Optional, Dict


class ImageService:
    """Handles image generation and upload operations."""

    def __init__(self):
        config = DropboxConfig()
        url_formatter = DropboxUrlFormatter()
        link_generator = DropboxLinkGenerator(config, url_formatter)
        self.uploader = DropboxUploader(config, link_generator)

    def generate_and_upload(
        self, template_folder: str, item: Dict, result: Dict = None
    ) -> Optional[str]:
        """Generate and upload an image."""
        from image import generator  # Local import to avoid circular dependency

        img_local_url = generator.run(
            template_folder, item, None, "definition" if result else None, result
        )

        if not img_local_url:
            return None

        return self.uploader.upload(img_local_url)
