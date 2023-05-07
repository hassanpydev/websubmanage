import http.client
import json
from mysql.connector import connect
from .chate_gpt_util import create_article
from ..worpress_poster import create_post


def insert_search_results(data):
    conn = connect(
        host="localhost",
        user="hassan",  # Replace with your MySQL username
        password="hassan1998",  # Replace with your MySQL password
        dbname="kok"
    )

    # Create a new database
    cursor = conn.cursor()
    cursor.execute("""
    
    """)


def scarp_google_results(query_string, page=1, number_of_results=10):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query_string.strip()})
    headers = {
        "X-API-KEY": "fef0ad2c1f25533eb3f2e112de0d0aa3d722e6b6",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


# dict_keys(['searchParameters', 'organic', 'peopleAlsoAsk', 'relatedSearches'])
def get_organic_search_results(data: dict) -> list:
    return data.get("organic")


def get_people_also_ask_search_results(data: dict) -> list:
    return data.get("peopleAlsoAsk")


def get_related_search_results(data: dict) -> list:
    return data.get("relatedSearches")


def get_search_results(query_string: str, domain: str):
    ppl_asks = get_people_also_ask_search_results(scarp_google_results(query_string))
    if ppl_asks:
        for question in ppl_asks:
            article = create_article(question.get("question"))

            create_post(title=question.get("question"), content=article)
            print("Post created successfully")
