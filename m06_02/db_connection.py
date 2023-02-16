from psycopg2 import connect, Error
from contextlib import contextmanager


@contextmanager
def connection():
    conn = None
    try:
        conn = connect(host='balarama.db.elephantsql.com', user='hvlvohkr', database='hvlvohkr',
                       password='')
        yield conn
        conn.commit()
    except Error as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
