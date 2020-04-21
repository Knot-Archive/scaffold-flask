from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModelMixin(object):
    def __init__(self, *args, **kwargs):
        pass

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
