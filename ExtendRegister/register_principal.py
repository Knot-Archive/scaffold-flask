from functools import partial

from flask_login import current_user
from flask_principal import Need
from flask_principal import Permission
from flask_principal import Principal
from flask_principal import RoleNeed
from flask_principal import UserNeed
from flask_principal import identity_loaded

principals = Principal()

# Role
admin_permission = Permission(RoleNeed('admin'))
common_permission = Permission(RoleNeed('common'))
# Careerline
CareerlineNeed = partial(Need, 'careerline')
game_permission = Permission(CareerlineNeed('game'))
ad_permission = Permission(CareerlineNeed('ad'))


@identity_loaded.connect
def on_identity_loaded(sender, **kwargs):
    identity = kwargs['identity']
    # Set the identity user object
    user = current_user
    identity.user = user

    # Add the UserNeed to the identity
    if hasattr(identity.user, 'id'):
        identity.provides.add(UserNeed(identity.user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(identity.user, 'roles'):
        for role in identity.user.roles:
            identity.provides.add(RoleNeed(role.name))
