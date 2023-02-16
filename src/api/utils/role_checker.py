from typing import List
from fastapi import Depends, HTTPException, status
from src.services.users import get_current_user_info


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user_info: dict = Depends(get_current_user_info)):
        if user_info.get('role') not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Недостаточно прав',
            )
