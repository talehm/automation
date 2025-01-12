from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from domain import posts
import json
import time

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# service_account_file.json is the private key that you created for your service account.
JSON_KEY_FILE = "trueandfiction-1d70b088ba3d.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    JSON_KEY_FILE, scopes=SCOPES
)

http = credentials.authorize(httplib2.Http())
with open("data/definitions.json", "r") as file:
    data = json.load(file)

for item in data[699:799]:
    url = item["link"]
    print(url)
    # request_content = json.dumps({"url": url, "type": "URL_UPDATED"})
    # response, content = http.request(ENDPOINT, method="POST", body=request_content)
    # print(url, response, content)
    # time.sleep(20)

# Define contents here as a JSON string.
# This example shows a simple update request.
# Other types of requests are described in the next step.
