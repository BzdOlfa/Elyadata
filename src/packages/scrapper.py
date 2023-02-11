import datetime
import json

from facebook_page_scraper import Facebook_scraper

browser = "chrome"
proxy = "IP:PORT"  # if proxy requires authentication then user:password@IP:PORT
timeout = 600  # 600 seconds
headless = True


def fetch_posts(page_name, pages_number=10):
    """
    It takes a page name and number of pages to scrap as arguments, then it scraps the page and returns a list of
    dictionaries containing the scrapped data

    :param page_name: The name of the page you want to scrape
    :param pages_number: The number of pages to be scrapped, defaults to 10 (optional)
    :return: A list of dictionaries.
    """
    scrapped_posts = []
    meta_ai = Facebook_scraper(page_name, pages_number, browser, proxy=proxy, timeout=timeout, headless=headless)
    json_data = meta_ai.scrap_to_json()
    json_data = json.loads(json_data)
    added_time = datetime.datetime.now()

    for post, post_data in json_data.items():
        try:
            print(post)
            scrapped_posts.append({
                'content': post_data['content'],
                "image": post_data['image'][0] if post_data['image'][0] else '',
                "likes": int(post_data["reactions"]['likes']),
                "shares": int(post_data['shares']),
                "post_url": post_data['post_url'],
                "added_time": added_time,
                "video": post_data['video'][0] if post_data['video'][0] else '',
                "posted_on": post_data['posted_on'],
            })
        except Exception as e:
            print(f'error occured : {e}')
    return scrapped_posts
