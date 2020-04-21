from flask import Blueprint
from flask_restful import Api

from . import resources
from .models import UserModel

bp_auth = Blueprint('bp_auth', __name__, url_prefix='/auth')
api = Api(bp_auth)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.CommonPermissionResource, '/need_common')
