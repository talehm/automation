import requests
from requests.auth import HTTPBasicAuth

site_url = "https://trueandfiction.com/wp-json/wp/v2/users/me"
username = "taleh"
password = "k2gVBjw4!"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}
response = requests.get(
    site_url, auth=HTTPBasicAuth(username, password), headers=headers
)

if response.status_code == 200:
    print("Authentication Successful!")
    print(response.json())
else:
    print("Authentication Failed!")
    print(response.status_code, response.text)
