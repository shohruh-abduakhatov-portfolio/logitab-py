from marshmallow import Schema


class Response:
    _stack = {}


    def __init__(self):
        self._stack = {}


    def created(self, text):
        self._stack.update({
            200: {"description": text}
        })
        return self


    def list(self, obj: [Schema]):
        self._stack.update({200: {"schema": obj}})
        return self


    @property
    def _200(self) -> 'Response':
        self._stack.update({200: {"description": "Success"}})
        return self


    @property
    def _401(self) -> 'Response':
        self._stack.update({401: {"description": "Unauthorized"}})
        return self


    @property
    def _400(self) -> 'Response':
        self._stack.update({400: {"description": "Bad Request"}})
        return self


    @property
    def _422(self) -> 'Response':
        self._stack.update({422: {"description": "Validation error"}})
        return self


    @property
    def _500(self) -> 'Response':
        self._stack.update({500: {"description": "Server error"}})
        return self


    @property
    def _404(self) -> 'Response':
        self._stack.update({404: {"description": "Object Not found"}})
        return self


    @property
    def _405(self) -> 'Response':
        self._stack.update({404: {"description": "Method Not Allowed"}})
        return self


    def build(self) -> dict:
        return self._stack
