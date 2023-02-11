import json

import uvicorn
from src.packages.db_utils import get_cursor, persist_element, init_table
from src.packages.scrapper import fetch_posts
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def scrap_posts(page: str, limit: int = 1, persist: bool = True, max_trials=1000):
    """
    It scrapes the posts of a given page, and persists them in a database

    :param page: the page to scrap
    :type page: str
    :param limit: the number of pages to scrap, defaults to 1
    :type limit: int (optional)
    :param persist: if True, the data will be persisted in the database, defaults to True
    :type persist: bool (optional)
    :param max_trials: the number of times the scraper will try to fetch posts from the page, defaults to 1000 (optional)
    :return: A dictionary with a key of records and a value of added.
    """
    res = []  # init output object
    cursor = get_cursor().cursor()
    init_table(cursor)  # init table if not created
    try:
        while not len(res) and max_trials > 0:
            res = fetch_posts(page, pages_number=limit)
            max_trials -= 1
    except Exception as e:
        print(f'failed, {e}')
    if res and persist:
        persist_element(res, cursor)
        return {"records": "added"}
    return {"operation": "failed"}


@app.get("/get_all/")
async def get_all_records():
    """
    It creates a connection to the database, creates a cursor, executes a query, fetches the results, and returns the
    results as a JSON string
    :return: A JSON object containing all the records in the database.
    """
    conn = get_cursor()
    cursor = conn.cursor()
    cursor.execute('select * from fb_posts;')
    results = cursor.fetchall()
    json_output = json.dumps(results)
    return json_output


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
