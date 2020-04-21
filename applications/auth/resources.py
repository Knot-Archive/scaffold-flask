from flask import current_app
from flask import make_response
from flask import session
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_principal import AnonymousIdentity
from flask_principal import Identity
from flask_principal import identity_changed
from flask_restful import Resource
from flask_restful import reqparse

from ExtendRegister.register_login import login_manager
from ExtendRegister.register_principal import common_permission
from .models import UserModel


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(user_id)


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

parser_change_password = reqparse.RequestParser()
parser_change_password.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.add()
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if not user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        if UserModel.verify_hash(data['password'], user.password):
            # Keep the user info in the session using Flask-Login
            login_user(user)
            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
            payload = {
                "user": user.username,
            }
            response = make_response(payload)
            return response
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    def post(self):
        # Remove the user information from the session
        logout_user()
        # Remove session keys set by Flask-Principal
        for key in ('identity.name', 'identity.auth_type'):
            session.pop(key, None)
        identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
        return {'message': 'Access token has been revoked'}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @login_required
    def get(self):
        user = current_user
        return {"user": user.username}


class ChangePasswordResource(Resource):
    def post(self):
        return {"message": 'password change successful.'}


class ChangePasswordAdminResource(Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        user.password = UserModel.generate_hash(data['password'])
        user.add()
        return {"message": 'password chagne successful.'}


class CommonPermissionResource(Resource):
    @common_permission.require()
    def get(self):
        return {"message": 'user with role common'}
