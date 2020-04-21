from flask import Flask

from common.modules.flask_storage import FileSystemStorage


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.config['UPLOADS_FOLDER'] = 'uploads'
        storage = FileSystemStorage()
        storage.save('file.md', 'hello')
    return app


if __name__ == '__main__':
    create_app()
