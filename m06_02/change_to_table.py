from random import randint
import pprint

from faker import Faker

from db_connection import connection

fake = Faker('uk-UA')
change_table_users = """
    ALTER TABLE users ADD COLUMN phone_number varchar(25);
"""


if __name__ == '__main__':
    with connection() as conn:
        c = conn.cursor()
        c.execute(change_table_users)
        c.close()
