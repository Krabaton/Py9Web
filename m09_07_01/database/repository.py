from sqlalchemy import and_

from database.db import session
from database.models import User, Todo


def get_user(login):
    user = session.query(User).filter(User.login == login).first()
    return user


def get_all_todos(user):
    todos = session.query(Todo).join(User).filter(Todo.user == user).all()  # filter == where
    return todos


def create_todo(title, description, user):
    todo = Todo(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()


def update_todo(_id, title, description, user):
    todo = session.query(Todo).filter(and_(Todo.user == user, Todo.id == _id))
    if todo:
        todo.update({"title": title, "description": description})
        session.commit()
    session.close()
    return todo.first()


def remove_todo(_id, user):
    r = session.query(Todo).filter(and_(Todo.user_id == user.id, Todo.id == _id)).delete()
    session.commit()
    session.close()
    return r
