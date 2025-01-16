from flask import Blueprint, request, session
from utils.file_handler import JsonFileHandler
from indexing.bing import IndexNowClient

indexing_db = Blueprint("indexing", __name__)


@indexing_db.route("/bing", methods=["GET"])
def index_on_bing():
    url_count = request.args.get("url_count")
    return submit_urls(url_count)


def submit_urls(url_count=None):
    client = IndexNowClient()
    if url_count is None:
        url_count = client.get_daily_quota()
    try:
        records_handler = JsonFileHandler("indexing/records.json")
        URL_LIST, last_index = get_url_list(url_count, records_handler)
        response = client.submit_urls(url_list=URL_LIST)
        if response.status_code == 200:
            records_handler.write({"bing": last_index})
            print(f"Response from IndexNow API: {len(URL_LIST)} is indexed")
        else:
            print(f"Response from IndexNow API: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
    return "True"


def get_url_list(count, records_handler):
    urls_handler = JsonFileHandler("data/definitions.json")
    data = urls_handler.read()
    links = [item["link"] for item in data]

    records = records_handler.read()
    start_index = records["bing"]
    last_index = start_index + int(count)
    URL_LIST = links[start_index:last_index]
    return URL_LIST, last_index
