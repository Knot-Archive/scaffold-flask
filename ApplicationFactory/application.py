import os
from flask import Flask as _Flask
from flask import jsonify

from ExtendRegister.register_cors import cors
from ExtendRegister.register_login import login_manager
from ExtendRegister.register_mail import mail
from ExtendRegister.register_principal import principals
from ExtendRegister.register_sqlalchemy import db
from applications.auth import bp_auth
from clis import demo_cli
from config.config import ConfigInstanceFactory


class Flask(_Flask):
    # json_encoder = JSONEncoder # replace JsonEncoder Here
    template_folder = os.getcwd() + '/templates'
    static_folder = os.getcwd() + '/static'


def create_app():
    config_factory = ConfigInstanceFactory()
    config_obj = config_factory.get_config_instance()

    app = Flask(__name__)

    """
    add converters 
    like this 
    
        app.url_map.converters['objectid'] = ObjectIdConverter
    
    """

    # config  Debug = True
    app.config.from_object(config_obj)

    """
    register blueprint here not in ExtendRegister
    like ths 
    
        from modules import blue_index
        from modules import blue_user
        from modules import blue_admin
        app.register_blueprint(blue_index)
        app.register_blueprint(blue_user)
        app.register_blueprint(blue_admin)
        
    """
    app.register_blueprint(bp_auth)

    # init flask-cors
    cors.init_app(app)
    # init mongo
    # pymongo.init_app(app)
    # init sqlalchemy
    db.init_app(app)
    # init flask-mail
    mail.init_app(app)
    # init flask-login
    login_manager.init_app(app)
    # init flask-principal
    principals.init_app(app)

    # hock_function_wrapper before_first_request
    @app.before_first_request
    def before_first():
        # print("app.before_first")
        pass

    # hock_function_wrapper before_request
    @app.before_request
    def before():
        # print("app.before")
        pass

    # hock_function_wrapper after_request
    @app.after_request
    def after(response):
        # print("app.after")
        return response

    # hock_function_wrapper teardown_request
    @app.teardown_request
    def teardown(e):
        # print("app.teardown")
        pass

    @app.errorhandler(400)
    def resource_not_found(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(401)
    def resource_not_found(e):
        return jsonify(error=str(e)), 401

    @app.errorhandler(403)
    def resource_not_found(e):
        return jsonify(error=str(e)), 403

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def resource_not_found(e):
        return jsonify(error=str(e)), 500

    app.cli.add_command(demo_cli)

    return app
