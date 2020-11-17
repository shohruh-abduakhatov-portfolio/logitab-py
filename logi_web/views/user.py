from aiohttp import web
from aiohttp_apispec import docs
from sqlalchemy import and_

from executors.user.user_client import UserClient
from logi_web.errors import HTTPForbidden
from logi_web.errors import ValidationError as VError
from logi_web.models import users, encode_auth_token, decode_auth_token
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class User:
    async def login(self, request):
        # todo request: keep me logedin
        data = await request.json()
        async with request.app['db'].acquire() as conn:
            result = await conn.execute(
                users.select().where(and_(
                    users.c.username == data['username'],
                    users.c.password == data['password']
                )))
            user = await result.first()
            if user:
                auth_token = encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return web.json_response(
                        data=response_object
                    )
            else:
                return web.json_response(
                    data={"error": "Wrong credentials"}
                )


    async def register(self, request):
        # todo request:
        #
        data = await request.json()
        pass


    async def logoff(self, request):
        pass


    async def check_permission(self, request, role):
        try:
            user = request.user
        except Exception as ex:
            raise HTTPForbidden(detail="Wrong permissions")

        user_role = user.get('role', None)
        if role == 'admin' or (role is not None and role == user_role):
            return
        raise HTTPForbidden(detail="Wrong permissions")


    async def is_authorized(self, request):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return False, 'Token required'
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                request.user = "anonymous_user"
                return False, "invalid token"
        else:
            auth_token = ''
        if auth_token:
            try:
                resp = decode_auth_token(auth_token)
            except Exception as err:
                request.user = "anonymous_user"
                return False, "invalid_token"

            if not isinstance(resp, str):
                async with request.app['db'].acquire() as conn:
                    result = await conn.execute(users.select().where(users.c.id == resp))
                    user = await result.first()
            if user:
                request.user = {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "date_created": str(user.date_created),
                    "org_id": user.organization_id,
                }
                return True, user.username
        else:
            return False, "Unauthorized"


    async def is_unique(self, request, **kwargs):
        data = await request.json()
        async with request.app['db'].acquire() as conn:
            result = await conn.execute(
                users.select().where(and_(users.c.username == data['username'])))
            user = await result.first()
            if user:
                VError("Username exists. Please, choose another one")


    @docs(
        tags=["user"],
        summary="Activate User",
        description=("Activate User"),
        responses=Response()._200._400._401._422._500.build(),
        parameters=Param().url_path("user_id").build()
    )
    async def activate(self, request):
        user_id = request.match_info['user_id']
        if not user_id:
            VError("user_id missing")
        try:
            user_cli = UserClient()
            response = await user_cli.set_status(data={
                "id": int(user_id),
                "status": 1,
            })
            if not response:
                return web.json_response(
                    status=500
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


    @docs(
        tags=["user"],
        summary="Deactivate User",
        description="Deactivate User",
        responses=Response()._200._400._401._422._500.build(),
        # parameters=Param().url_path("user_id").build()
    )
    async def deactivate(self, request):
        user_id = request.match_info['user_id']
        if not user_id:
            VError("user_id missing")
        try:
            user_cli = UserClient()
            response = await user_cli.set_status(data={
                "id": int(user_id),
                "status": 0,
            })
            if not response:
                return web.json_response(
                    status=500
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


user_view = User()
