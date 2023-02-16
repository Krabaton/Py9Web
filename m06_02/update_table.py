from random import randint

from psycopg2 import Error
from faker import Faker

from db_connection import connection

fake = Faker('uk-UA')
update_user = """
    UPDATE users SET phone_number = %s WHERE id = %s;
"""


if __name__ == '__main__':
    with connection() as conn:
        c = conn.cursor()
        for id_ in range(1,  100):
            c.execute(update_user, (fake.phone_number(), id_))
        c.close()
