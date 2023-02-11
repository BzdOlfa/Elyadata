import sys

sys.path.append("/app/src/packages")
from db_utils import get_cursor, init_table, persist_element


def test_get_cursor():
    assert get_cursor()


def test_init_table():
    cursor = get_cursor().cursor()
    init_table(cursor)
    cursor.execute("SELECT to_regclass('fb_posts')")
    result = cursor.fetchone()
    assert result[0]


def test_persist_element():
    cursor = get_cursor().cursor()
    init_table(cursor)
    element = {
        'content': 'elyatest',
        'image': 'test.jpg',
        'likes': 10,
        'shares': 5,
        'post_url': 'www.elyatest.com',
        'added_time': '2022-01-01',
        'video': 'elyatest.mp4',
        'posted_on': '2022-01-01'
    }
    persist_element(element, cursor)
    cursor.execute("SELECT * FROM fb_posts WHERE content='elyatest'")
    result = cursor.fetchone()
    assert result
