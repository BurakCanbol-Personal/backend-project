from app.utils.roles import ROLES

def has_permission(user_role, action):
    return action in ROLES.get(user_role, [])