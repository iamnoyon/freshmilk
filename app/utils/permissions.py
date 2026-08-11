from enum import Enum

from fastapi import Depends, HTTPException, status

from app.utils.token import get_current_user


class Permission(str, Enum):
    CREATE_USER = "create_user"
    EDIT_USER = "edit_user"
    DELETE_USER = "delete_user"
    VIEW_USERS = "view_users"


def require_permission(*permissions: str):
    def checker(current_user: dict = Depends(get_current_user)):
        user_perms = set(current_user.get("permissions", []))
        if not set(permissions).issubset(user_perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )
        return current_user

    return checker
