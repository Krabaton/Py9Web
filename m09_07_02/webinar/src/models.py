from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    start_work = Column(Date, nullable=False)
    students = relationship('Student', secondary='teachers_to_students', back_populates='teachers')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    teachers = relationship('Teacher', secondary='teachers_to_students', back_populates='students')
    contacts = relationship('ContactPerson', back_populates='student')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class ContactPerson(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship('Student', back_populates='contacts')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

class TeacherStudent(Base):
    __tablename__ = 'teachers_to_students'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))

