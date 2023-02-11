import os
from urllib.parse import urlparse

import psycopg2
from psycopg2.extensions import AsIs


def get_cursor():
    """
    It connects to the database and returns a cursor
    :return: A connection object
    """
    db_url = os.environ["DATABASE_URL"]
    url = urlparse(db_url)
    username, password = url.username, url.password
    database, hostname, port = url.path[1:], url.hostname, url.port
    print(database, username, port, hostname, password)
    return psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )


def init_table(cursor):
    check_table_query = "SELECT to_regclass('fb_posts')"
    cursor.execute(check_table_query)
    result = cursor.fetchone()
    if not result[0]:
        create_table_query = '''CREATE TABLE fb_posts (
                        ID  serial primary key,
                        content varchar(255),
                        image varchar(255),
                        likes int,
                        shares int,
                        post_url varchar(255),
                        video varchar(255),
                        posted_on timestamp default NULL,
                        added_time timestamp default NULL);'''
        cursor.execute(create_table_query)


def persist_element(element, cursor):
    insert_query = 'insert into fb_posts (%s) values %s'
    keys = ['content', "image", "likes", "shares", "post_url", "added_time", "video", "posted_on"]
    values = [element[key] for key in keys]
    cursor.execute(insert_query, (AsIs(','.join(keys)), tuple(values)))


if __name__ == "__main__":
    with get_cursor() as conn:
        with conn.cursor() as cursor:
            init_table(cursor=cursor)
