import requests
from utils.env_manager import EnvManager
import xml.etree.ElementTree as ET


class IndexNowClient:
    """
    A client for submitting URLs to the IndexNow API.
    """

    def __init__(
        self,
        base_url: str = "https://ssl.bing.com/webmaster/api.svc",
    ):
        self.api_key = EnvManager.get_env_var("BING_API_KEY")
        self.base_url = base_url

    def get_daily_quota(self) -> int:
        route = "pox/GetUrlSubmissionQuota"
        site_url = EnvManager.get_env_var("SITE_URL")
        endpoint = f"{self.base_url}/{route}?apiKey={self.api_key}&siteUrl={site_url}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            xml_content = response.text  # Get XML content as a string
            namespace = {
                "ns": "http://schemas.datacontract.org/2004/07/Microsoft.Bing.Webmaster.Api"
            }

            root = ET.fromstring(
                xml_content
            )  # Parse the XML string into an ElementTree.Element
            daily_quota = root.find("ns:DailyQuota", namespace).text
            return daily_quota
            # return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to submit URLs: {e}") from e

    def submit_urls(self, url_list: list[str]) -> dict:
        """
        Submit a batch of URLs to the IndexNow API.

        :param site_url: The root URL of the site.
        :param url_list: A list of URLs to submit.
        :return: The response from the API as a dictionary.
        """
        if not url_list:
            raise ValueError("url_list cannot be empty.")

        site_url = EnvManager.get_env_var("SITE_URL")
        payload = {"siteUrl": site_url, "urlList": url_list}
        headers = {"Content-Type": "application/json"}
        endpoint = f"{self.base_url}/json/SubmitUrlBatch?apiKey={self.api_key}"

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to submit URLs: {e}") from e
