import click
from click import Command
from flask.cli import AppGroup

from ExtendRegister.register_sqlalchemy import db
from applications.auth import UserModel
from applications.auth.models import RoleModel

demo_cli = AppGroup('demo')


@demo_cli.command('hello')
@click.argument('name')
def hello_name(name):
    print("hi {}".format(name))


@demo_cli.command('dropall')
def dropall():
    db.drop_all()
    print('db drop_all')


@demo_cli.command('createall')
def createall():
    db.create_all()
    print('db create_all')


@demo_cli.command('startproject')
def startproject():
    role = RoleModel(name='admin').add()
    role2 = RoleModel(name='common').add()
    user = UserModel(username='adminUser', password=UserModel.generate_hash('adminPass')).add()
    user2 = UserModel(username='commonUser', password=UserModel.generate_hash('commonPass')).add()
    user.roles.append(role)
    user2.roles.append(role2)
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    print('create user admin with role admin')
    print('admin user {}'.format(user.username))
    print('common user {}'.format(user2.username))
