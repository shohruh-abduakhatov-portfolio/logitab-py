from aiohttp import web
from aiohttp_apispec import docs, request_schema
from marshmallow import ValidationError
from sqlalchemy import and_

from logi_web.errors import ValidationError as VError
from logi_web.middlewares import auth_required
from logi_web.views_mobile.schemas import ChangePassWordSchema, LoginSchema, SendPasswordSchema, change_password_schema, \
    login_schema, send_password_schema
from logi_web.models import users, encode_auth_token
from logi_web.swagger.reponse_code import Response
from logi_web.utils.enum import UserRole


class Auth:

    # @staticmethod
    @docs(
        tags=["mobile_auth"],
        summary="Login",
        description="Get jwt auth token.",
        responses=Response()._200._401._405._500.build(),
    )
    @request_schema(LoginSchema)
    async def login_driver(self, request):
        # todo request: keep me logedin
        print(">> auth")
        try:
            data = login_schema.load(await request.json())
        except ValidationError as err:
            return VError(detail=err.messages)

        async with request.app['db'].acquire() as conn:
            result = await conn.execute(
                users.select().where(and_(
                    users.c.username == data['username'],
                    users.c.password == data['password']
                )))
            user = await result.first()
            status = 200
            if user:
                if user.role != UserRole.DRIVER:
                    response = {"error": "Wrong role"}
                    status = 405
                else:
                    try:
                        auth_token = encode_auth_token(user.id)
                        if auth_token:
                            response = {
                                'status': 'success',
                                'message': 'Successfully logged in.',
                                'auth_token': auth_token.decode()
                            }
                    except:
                        response = {"error": "Wrong role"}
                        status = 405
            else:
                response = {"error": "Wrong credentials"}
                status = 401
            return web.json_response(
                data=response,
                status=status
            )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_auth"],
        summary="Change Password",
        description="Set new password.",
        responses=Response()._200._401.build(),
    )
    @request_schema(ChangePassWordSchema)
    async def change_password(request):
        try:
            data = change_password_schema.load(await request.json())
        except ValidationError as err:
            return VError(detail=err.messages)

        async with request.app['db'].acquire() as conn:
            result = await conn.execute(
                users.update().where(and_(
                    users.c.username == request.user['username'],
                    users.c.password == data['old_password']
                )).values(password=data['new_password']).returning(users.c.id)
            )
            response, status = {}, 200
            id = await result.first()
            if not id:
                response = {"error": "Wrong Credentials"}
                status = 401
            return web.json_response(
                data=response,
                status=status
            )


    @staticmethod
    @docs(
        tags=["mobile_auth"],
        summary="Forgot Password",
        description="Send password to email.",
        responses=Response()._200._404._500.build(),
    )
    @request_schema(SendPasswordSchema)
    async def send_password(request):
        try:
            data = send_password_schema.load(await request.json())
        except ValidationError as err:
            return VError(detail=err.messages)

        async with request.app['db'].acquire() as conn:
            result = await conn.execute(
                users.select().where(
                    users.c.email == data['email'].lower()
                ))
            user = await result.first()
            response, status = {}, 200
            if not user:
                response = {"error": "Email does not exist"}
                status = 404
            else:
                try:
                    from executors.email.email_cli import EmailClient
                    email_cli = EmailClient()
                    sent, err = await email_cli.send_forgotten_password(
                        to_email=user.email, password=user.password)
                    assert sent and not err
                    response = "Sent"
                except:
                    response = {"error": "Could not send passord"}
                    status = 500
            return web.json_response(
                data=response,
                status=status
            )


    
    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_auth"],
        summary="validate token",
        description="Validate token to check if user is logged in.",
        responses=Response()._200._401.build(),
    )
    async def is_valid_token(request):
        return web.json_response(
            data={
                'status': 'success',
                'message': 'User already logged in.',
                'is_logged_in': True 
            },
            status=200
        )

auth = Auth()
