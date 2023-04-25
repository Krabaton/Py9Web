from typing import List

from fastapi import Depends, HTTPException, status, Request

from src.database.models import User, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        print(request.method, request.url)
        print(f'User role {current_user.roles}')
        print(f'Allowed roles: {self.allowed_roles}')
        if current_user.roles not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Operation forbidden')

