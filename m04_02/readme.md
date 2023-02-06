# Обзор застосунку app.py

```python
import json
import logging
import pathlib
import socket
import urllib.parse
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import pathlib

from jinja2 import Environment, FileSystemLoader

BASE_DIR = pathlib.Path()
env = Environment(loader=FileSystemLoader('templates'))
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
BUFFER = 1024


def send_data_to_socket(body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (SERVER_IP, SERVER_PORT))
    client_socket.close()


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # self.send_html('contact.html')
        body = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_socket(body)
        self.send_response(302)
        self.send_header('Location', '/blog')
        self.end_headers()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html('index.html')
            case "/contact":
                self.send_html('contact.html')
            case "/blog":
                self.render_template('blog.html')
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('404.html', 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def render_template(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open('blog.json', 'r', encoding='utf-8') as fd:
            r = json.load(fd)
        template = env.get_template(filename)
        print(template)
        html = template.render(blogs=r)
        self.wfile.write(html.encode())

    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())


def run(server=HTTPServer, handler=HTTPHandler):
    address = ('0.0.0.0', 3000)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


def save_data(data):
    body = urllib.parse.unquote_plus(data.decode())
    try:
        payload = {key: value for key, value in [el.split('=') for el in body.split('&')]}
        with open(BASE_DIR.joinpath('data/data.json'), 'w', encoding='utf-8') as fd:
            json.dump(payload, fd, ensure_ascii=False)
    except ValueError as err:
        logging.error(f"Field parse data {body} with error {err}")
    except OSError as err:
        logging.error(f"Field write data {body} with error {err}")


def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(BUFFER)
            save_data(data)
    except KeyboardInterrupt:
        logging.info('Socket server stopped')
    finally:
        server_socket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    STORAGE_DIR = pathlib.Path().joinpath('data')
    FILE_STORAGE = STORAGE_DIR / 'data.json'
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False)

    thread_server = Thread(target=run)
    thread_server.start()
    thread_socket = Thread(target=run_socket_server(SERVER_IP, SERVER_PORT))
    thread_socket.start()
```

Ми реалізували прості `HTTP` та `UDP` сервери. `HTTP`-сервер використовує клас `BaseHTTPRequestHandler`
із модуля `http.server`. `HTTP`-сервер може обробляти запити `GET` і `POST`
і використовує бібліотеку `Jinja2` для створення шаблону HTML-сторінки блогу, яку він надсилає браузеру.

Для обробки вхідних запитів `POST` за маршрутом `/contact` `HTTP` сервер надсилає тіло запиту на вказану `IP`
-адресу `SERVER_IP` та порт `SERVER_PORT` через `UDP` протокол. Застосунок також запускає сервер `UDP`, в окремому
потоці, він прослуховує вхідні дані з цієї `IP`-адреси на порту `SERVER_PORT` та зберігає отримані дані у файлі `JSON`.

Код класу `HTTPHandler` містить кілька методів обробки вхідних запитів `HTTP`:

- `do_GET`: обробляє запити `GET` і надсилає відповідний вміст `HTML` клієнту на основі запитуваного `URL`-шляху.
- `send_html`: надсилає вказаний файл HTML клієнту з указаним кодом статусу `HTTP`.
- `render_template`: рендерить файл HTML за допомогою `Jinja2` і надсилає його клієнту з указаним кодом статусу HTTP.
- `send_static`: надсилає вказаний статичний файл (в нашому випадку, зображення, `CSS`, `JavaScript`) клієнту.

Крім того, код застосунку також містить такі допоміжні функції:

- `run`: запускає `HTTP`-сервер і прослуховує вхідні запити.
- `save_data`: аналізує вхідні дані з `UDP`-сокета та зберігає їх у файлі JSON.
- `run_socket_server`: запускає сервер `UDP` і прослуховує вхідні дані.
-

Код запускає сервери `HTTP` та `UDP` в окремих потоках.

Тепер окремо по деяких методах, та функціях

```python
def send_static(self, filename):
    self.send_response(200)
    mime_type, *rest = mimetypes.guess_type(filename)
    if mime_type:
        self.send_header('Content-Type', mime_type)
    else:
        self.send_header('Content-Type', 'text/plain')
    self.end_headers()
    with open(filename, 'rb') as f:
        self.wfile.write(f.read())
```

Цей код є частиною обробника запитів HTTP класу `HTTPHandler`, який обслуговує відправку статичних файлів для браузеру.

1. Надсилає код статусу відповіді HTTP 200, щоб вказати, що запит виконано успішно `self.send_response(200)`.
2. Визначає тип MIME файлу за допомогою модуля `mimetypes` і додає заголовок `Content-Type` до відповіді з відповідним
   типом `MIME`. Якщо тип `MIME` не вдається визначити, за замовчуванням він має значення `"text/plain"`.
   ```python
       mime_type, *rest = mimetypes.guess_type(filename)
       if mime_type:
           self.send_header('Content-Type', mime_type)
       else:
           self.send_header('Content-Type', 'text/plain')
   ```
3. Завершує заголовки відповідей `self.end_headers()`.
4. Відкриває файл із вказаним іменем у бінарному режимі `with open(filename, 'rb') as f:`.
5. Записує вміст файлу в тіло відповіді `self.wfile.write(f.read())`.

```python
def render_template(self, filename, status_code=200):
    self.send_response(status_code)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    with open('blog.json', 'r', encoding='utf-8') as fd:
        r = json.load(fd)
    template = env.get_template(filename)
    print(template)
    html = template.render(blogs=r)
    self.wfile.write(html.encode())
```

Метод `render_template` використовує механізм шаблонів `Jinja2` для рендерингу HTML-шаблону з
файлу `templates/blog.html`. Він починається з
надсилання заголовка відповіді з указаним кодом статусу та типом вмісту, встановленим як `"text/html"`. Потім він
відкриває файл під назвою `"blog.json"` і завантажує вміст за допомогою бібліотеки `json`. Потім метод використовує
об’єкт `env = Environment(loader=FileSystemLoader('templates'))` `Jinja2`, щоб отримати шаблон із вказаною назвою файлу
та показати його з даними з `"blog.json"`. Потім відтворений HTML кодується у вигляді байтів і надсилається клієнту як
тіло відповіді.

```python
def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(BUFFER)
            save_data(data)
    except KeyboardInterrupt:
        logging.info('Socket server stopped')
    finally:
        server_socket.close()
```

Функція `run_socket_server` це дуже проста реалізація сокет-сервера, який використовує протокол `UDP`. Сервер
прослуховує вхідні повідомлення на заданій `IP`-адресі та порту `(ip, port)`, отримує вхідні дані, а потім викликає
функцію `save_data` з отриманими даними як аргументом. Сервер продовжуватиме прослуховувати вхідні дані, доки не буде
викликано переривання клавіатури (наприклад, користувач натискає `CTRL + C`), у цьому випадку він зареєструє
повідомлення 'Socket server stopped' та закриє сокет. Константа `BUFFER` це розмір буфера, що визначає максимальний
обсяг даних, який можна отримати за один виклик метод `recvfrom`.