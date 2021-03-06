from contextlib import contextmanager
from urllib.parse import urlparse

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor

from looklike.configs import config


_connection_pool = None


def get_db_connection_pool():
    global _connection_pool

    if _connection_pool:
        return _connection_pool

    url = urlparse(config.POSTGRESQL_URL)
    _connection_pool = ThreadedConnectionPool(
        minconn=1,
        maxconn=20,
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return _connection_pool


@contextmanager
def get_db_connection():
    connection_pool = get_db_connection_pool()
    try:
        connection = connection_pool.getconn()
        yield connection
    finally:
        connection_pool.putconn(connection)


@contextmanager
def get_db_cursor(commit: bool = False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()
