from functools import wraps
from ..services import user_service

def requires_permission(permission_name):
    """Decorator to check if a user has the required permission."""
    def decorator(func):
        @wraps(func)
        def wrapper(current_user, *args, **kwargs):
            if not current_user:
                print("You must be logged in to perform this action.")
                return

            user_permissions = user_service.get_user_permissions(current_user.id)
            if permission_name not in user_permissions:
                print(f"You do not have permission to {permission_name}.")
                return

            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator
