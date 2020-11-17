from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import ValidationError

from executors.edited_event.edited_event_db import (
    db_bulk_get_by_log_id as edited_event_get_by_log_id,
    db_get_first_by_status
)
from executors.event.event_db import db_bulk_get_log_id as event_get_by_log_id
from executors.utils.enum import EventEditedCodeEnum
from logi_web.errors import HTTPServiceError, ValidationError as VError
from logi_web.middlewares import auth_required
from logi_web.schemas import custom_dumps, EditedEventListSchema, EditedAndCurrentEvent
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response
from logi_web.utils.enum import UserRole
from logi_web.views_mobile.schemas import LogEditReqestSchema, log_edit_request_schema


class LogEditRequest:
    def __init__(self):
        pass
        # self.client = VehicleClient()


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_log_edit_request"],
        summary="Log Edit Request list",
        description=("All Log Edit Request List"),
        responses=Response().list(EditedEventListSchema)._401._422._500.build(),
    )
    @request_schema(LogEditReqestSchema)
    async def get_list(request):
        try:
            data = log_edit_request_schema.load(await request.json())
        except ValidationError as err:
            return VError(detail=err.messages)

        org_id = request.user['org_id']
        try:
            vehicles = await db_get_first_by_status(
                EventEditedCodeEnum.WAITING, org_id, int(data['driver_id']))
        except Exception as ex:
            return HTTPServiceError()

        return web.json_response(
            data={"data": vehicles},
            dumps=custom_dumps,
        )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_log_edit_request"],
        summary="Log Edit Request Details",
        description=("Log Edit Request Details with current and edited log"),
        parameters=Param().url_path("log_id").build()
    )
    @response_schema(EditedAndCurrentEvent(), 200)
    async def details(request):
        log_id = request.match_info['log_id']
        try:
            edited_events = await edited_event_get_by_log_id(log_id=int(log_id))
            events = await event_get_by_log_id(log_id=int(log_id))
            assert edited_events and events
        except Exception as ex:
            return HTTPServiceError()

        return web.json_response(
            data={"current_log": events,
                  "edited_log": edited_events},
            dumps=custom_dumps,
        )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_log_edit_request"],
        summary="Accept Log Edit Request",
        description=("Accept Log Edit Request Details by given log_id"),
        parameters=Param().url_path("log_id").build(),
        responses=Response().list(EditedEventListSchema)._401._422._500.build(),
    )
    async def accept(request):
        log_id = request.match_info['log_id']
        try:
            from executors.edited_event.edited_event_cli import EditEventClient
            edite_event_cli = EditEventClient()
            result = await edite_event_cli.request_make_action(
                log_id=int(log_id), accept=True
            )
            assert result
        except Exception as ex:
            return HTTPServiceError()

        return web.json_response(
            data={True},
            dumps=custom_dumps,
        )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_log_edit_request"],
        summary="Reject Log Edit Request",
        description=("Reject Log Edit Request Details by given log_id"),
        parameters=Param().url_path("log_id").build(),
        responses=Response().list(EditedEventListSchema)._401._422._500.build(),
    )
    async def reject(request):
        log_id = request.match_info['log_id']
        try:
            from executors.edited_event.edited_event_cli import EditEventClient
            edite_event_cli = EditEventClient()
            result = await edite_event_cli.request_make_action(
                log_id=int(log_id), accept=False
            )
            assert result
        except Exception as ex:
            return HTTPServiceError()

        return web.json_response(
            data={True},
            dumps=custom_dumps,
        )


    async def multipart_test(self, request: web.Request) -> web.Response:
        f1 = "/home/sa/Desktop/startup/us_project/logi-back-py/font-colors.pdf"
        # post_id = request.match_info["post"]
        # db = request.config_dict["DB"]
        # async with db.execute("SELECT image FROM posts WHERE id = ?", [post_id]) as cursor:
        #     row = await cursor.fetchone()
        #     if row is None or row["image"] is None:
        #         img = PIL.Image.new("RGB", (64, 64), color=0)
        #         import io
        #         fp = io.BytesIO()
        #         img.save(fp, format="JPEG")
        #         content = fp.getvalue()
        #     else:
        #         content = row["image"]
        # return web.Response(body=content, content_type="image/jpeg")


log_edit_request = LogEditRequest()
