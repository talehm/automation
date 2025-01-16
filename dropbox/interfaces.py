from abc import ABC, abstractmethod
from typing import Optional


class FileUploader(ABC):
    """Abstract base class for file upload operations."""

    @abstractmethod
    def upload(self, file_path: str, destination_path: str) -> Optional[str]:
        """Upload a file and return its shared link."""
        pass


class LinkGenerator(ABC):
    """Abstract base class for generating shared links."""

    @abstractmethod
    def create_link(self, file_path: str) -> Optional[str]:
        """Create a shared link for a file."""
        pass


class UrlFormatter(ABC):
    """Abstract base class for URL formatting operations."""

    @abstractmethod
    def format_url(self, url: str) -> str:
        """Format a URL according to specific requirements."""
        pass
