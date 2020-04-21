from sqlalchemy import Table
from sqlalchemy.orm import relationship

from ExtendRegister.register_sqlalchemy import db, ModelMixin
from passlib.hash import pbkdf2_sha256 as sha256

association_table = Table('association', db.Model.metadata,
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class RoleModel(db.Model, ModelMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='')
    users = relationship("UserModel", secondary=association_table, back_populates="roles")


class UserModel(db.Model, ModelMixin):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String)
    nickname = db.Column(db.String(120))
    authenticated = db.Column(db.Boolean, default=False)
    roles = relationship("RoleModel", secondary=association_table, back_populates="users")

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
