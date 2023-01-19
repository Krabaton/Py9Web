from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello group web 9!"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
