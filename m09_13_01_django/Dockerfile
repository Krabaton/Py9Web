# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію усередині контейнера
WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

# Встановимо залежності усередині контейнера
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Скопіюємо інші файли до робочої директорії контейнера
COPY . .

# Позначимо порт де працює програма всередині контейнера
EXPOSE 8000

# Запустимо нашу програму всередині контейнера
CMD ["python", "killer_instagram/manage.py", "runserver", "0.0.0.0:8000"]
