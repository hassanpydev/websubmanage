"""
a module to communicate with the wordpress api
"""
import json

import requests
from colorama import Fore
from requests.auth import HTTPBasicAuth

# config = json.loads(open(r"/home/hassan/PycharmProjects/MyBusniess/config.json", "rb").read())
from slugify import slugify


def generate_slug(post_title):
    # Generate a slug from the post title
    slug = slugify(post_title)
    return slug


def create_post(title, content,domain):
    """
    a function to create a post in the wordpress
    @param title: the title of the article
    @param content: the body of the article
    @return:
    """
    url = f"https://{domain}/wp-json/wp/v2/posts"
    post = {
        "title": title,
        "status": "publish",
        "content": f"{content}",
        "categories": 2,
        "type": "question",
        "slug": generate_slug(title),
        "date": "2022-02-17T10:00:00",
    }
    response = requests.post(
        url, auth=HTTPBasicAuth('tusuz', 'Pa$$w0rd!'), json=post
    )

    if response.status_code == 201:
        print(
            Fore.GREEN
            + f"Post Published Successfully : {response.json()['link']}"
            + Fore.LIGHTWHITE_EX
        )
        return response.json()
    response.raise_for_status()


