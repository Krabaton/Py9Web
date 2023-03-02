import random

from faker import Faker
from src.db import session
from src.models import Student, ContactPerson

fake = Faker()


def create_contact_person():
    students = session.query(Student).all()

    for _ in range(len(list(students)) + 4):
        student = random.choice(students)
        cp = ContactPerson(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            phone=fake.phone_number(),
            address=fake.address(),
            student_id=student.id
        )
        session.add(cp)
    session.commit()


if __name__ == '__main__':
    create_contact_person()
