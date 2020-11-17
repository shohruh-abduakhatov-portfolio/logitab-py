from functools import wraps

from logi_web.errors import HTTPUnauthorized
from logi_web.utils.enum import UserRole
from logi_web.views.user import user_view


def auth_required(role: UserRole = UserRole.OPERATOR):
    def auth_required_decorator(handler):
        @wraps(handler)
        async def wrapper(request):
            logged_in, message = await user_view.is_authorized(request)
            if not logged_in:
                return HTTPUnauthorized(detail=message)
            await user_view.check_permission(request, role)
            return await handler(request)


        return wrapper


    return auth_required_decorator
