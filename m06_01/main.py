from psycopg2 import connect, DatabaseError
from contextlib import contextmanager


@contextmanager
def connection():
    conn = None
    try:
        conn = connect(host='localhost', user='postgres', database='postgres', password='567234')
        yield conn
    except DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_table_users = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  email VARCHAR(30),
  password VARCHAR(30),
  age NUMERIC CHECK (age > 1 AND age < 150)
);
"""


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        c.close()
        conn.commit()
    except DatabaseError as error:
        print(error)


if __name__ == '__main__':
    with connection() as conn:
        if conn is not None:
            # create_table(conn, create_table_users)
            c = conn.cursor()
            instr = "INSERT INTO users (name, email, password, age) VALUES(%s, %s, %s, %s)"
            c.execute(instr, ('Mykola', 'mika@api.com', 'qwerty', 111))
            c.close()
            conn.commit()
