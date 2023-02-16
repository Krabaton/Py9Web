from random import randint
import pprint

from faker import Faker

from db_connection import connection

fake = Faker('uk-UA')
simple_select = """
    SELECT * FROM users WHERE id=%s;
"""
select = """
    SELECT id, name, email, age 
    FROM users 
    WHERE age > 45
    ORDER BY name
    LIMIT 10;
"""

select_regex = """
    SELECT id, name, email, age 
    FROM users 
    WHERE name SIMILAR TO '%(рій|ко)%'
    ORDER BY name
    LIMIT 10;
"""

if __name__ == '__main__':
    with connection() as conn:
        c = conn.cursor()
        # c.execute(simple_select, (10,))
        # print(c.fetchone())
        c.execute(select_regex)
        pprint.pprint(c.fetchall())
        c.close()
