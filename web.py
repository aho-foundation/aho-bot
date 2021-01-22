from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '404'


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
    print('web app started')
