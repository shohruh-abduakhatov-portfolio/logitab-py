from aiohttp import web
from aiohttp_apispec import request_schema, docs, response_schema
from asyncpg import UniqueViolationError
from marshmallow import ValidationError

from logi_web.errors import ValidationError as VError
from logi_web.schemas import custom_dumps, EventSchema, event_schema
from logi_web.swagger.reponse_code import Response
from logi_web.swagger.params import Param


class Event:
    def __init__(self) -> None:
        super().__init__()
        pass


    @docs(
        tags=["event"],
        summary="Create not for web app",
        description=("New event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        parameters=Param().url_path("log_id").build(),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(EventSchema)
    @response_schema(EventSchema(), 200)
    async def insert(self, request):
        org_id = 1  # request.user['org_id']
        try:
            data = event_schema.load(await request.json())
            data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            from executors.event.event_cli import EventClient
            event_cli = EventClient()
            event = await event_cli.add(data=data)
        except UniqueViolationError as e:
            return VError(detail={e.constraint_name: e.args[0]})
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data=event
        )


    @docs(
        tags=["event"],
        summary="Update Driving Event item",
        description=("Update Driving Event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        parameters=Param().url_path("event_id").build(),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(EventSchema)
    @response_schema(EventSchema(), 200)
    async def update(self, request):
        event_id = request.match_info['event_id']

        try:
            serialized_data = event_schema.load(await request.json())
            serialized_data['id'] = int(event_id)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            from executors.event.event_cli import EventClient
            event_cli = EventClient()
            event_update = await event_cli.modify(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=event_update,
            dumps=custom_dumps
        )


event_mobile = Event()
