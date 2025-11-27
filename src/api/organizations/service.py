from fastapi import Depends

from ..base.depend import get_current_user


async def get_organizations(user = Depends(get_current_user)):
    return user.organizations
