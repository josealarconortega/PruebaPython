from os import getenv

from application import create_app

app = create_app(getenv('APP_SETTINGS'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8099)
