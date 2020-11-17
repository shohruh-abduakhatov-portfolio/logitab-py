from aiohttp import web
from aiohttp_apispec import docs
from marshmallow import ValidationError

from executors.terminal.terminal_client import TerminalClient
from logi_web.errors import ValidationError as VError
from logi_web.schemas import terminal_schema, TerminalListSchema
from logi_web.swagger.reponse_code import Response


class Terminal:
    def __init__(self):
        self.client = TerminalClient()


    async def create(self, request):
        data = await request.json()

        try:
            validated_data = terminal_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            terminal_id = await self.client.add(data=validated_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"terminal_id": terminal_id.get('id')}
        )


    async def update(self, request):
        data = await request.json()
        terminal_id = request.match_info['terminal_id']

        data['id'] = int(terminal_id)
        try:
            validated_data = terminal_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            terminal_update = await self.client.modify(data=validated_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=terminal_update
        )


    @docs(
        tags=["home-terminal"],
        summary="List",
        description=("All IssueState List"),
        responses=Response().list(TerminalListSchema)._401._422._500.build(),
    )
    async def get_list(self, request):
        try:
            terminals = await self.client.get_all()
            assert terminals
            terminals = list(terminals.values())
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"data": terminals},
        )


    async def get_info(self, request):
        terminal_id = request.match_info['terminal_id']

        try:
            terminal = await self.client.get_by_id(id=terminal_id)
        except Exception as ex:
            raise ex

        if terminal is None:
            terminal = {}

        return web.json_response(
            data=terminal
        )


    async def delete(self, request):
        terminal_id = request.match_info['terminal_id']

        try:
            delete = await self.client.remove(id=int(terminal_id))
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


terminal = Terminal()
