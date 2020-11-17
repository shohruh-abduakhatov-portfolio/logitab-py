import datetime
import jwt
from logi_web.settings import config
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, DateTime
)


meta = MetaData()

users = Table(
    "users", meta,

    Column("id", Integer, primary_key=True),
    Column("username", String(255), nullable=False),
    Column("password", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("role", String(15), nullable=False),
    Column("date_created", DateTime, default=datetime.datetime.now()),
    Column("organization_id", Integer),
)


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config.get('token_lifetime', 30)*60),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            config.get('secret_key'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, config.get('secret_key'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token. Please log in again.')