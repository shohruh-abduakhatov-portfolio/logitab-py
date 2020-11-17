import datetime

from aiohttp import web
from aiohttp_apispec import (
    request_schema, docs, response_schema
)
from asyncpg import UniqueViolationError
from marshmallow import ValidationError

from executors.event.event_cli import EventClient
from logi_web.errors import ValidationError as VError
from logi_web.schemas import (
    event_schema,
    custom_dumps,
    EventSchema,
    DrivingEventListSchema, EventEditSchema, event_edit_schema, EventListSchema
)
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class Event:
    def __init__(self):
        self.client = EventClient()


    @docs(
        tags=["event"],
        summary="Create not for web app",
        description=("New event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"event_id": 0}')._401._422._500.build(),
    )
    @request_schema(EventSchema)
    async def create(self, request):
        org_id = 1
        data = await request.json()

        try:
            serialized_data = event_schema.load(data)
            serialized_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            event_id = await self.client.add(data=serialized_data)
        except UniqueViolationError as e:
            return VError(detail={e.constraint_name: e.args[0]})
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"event_id": event_id.get('id')}
        )


    @docs(
        tags=["event"],
        summary="Update Driving Event item",
        description=("Update Driving Event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(EventEditSchema)
    async def update(self, request):
        data = await request.json()
        event_id = request.match_info['event_id']

        data['id'] = int(event_id)

        try:
            serialized_data = event_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            event_update = await self.client.modify(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=event_update,
            dumps=custom_dumps
        )


    @docs(
        tags=["event"],
        summary="Delete",
        description=("Delete Driving Event item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("event_id").build()
    )
    async def delete(self, request):
        event_id = request.match_info['event_id']

        try:
            delete = await self.client.remove(id=int(event_id))
            if not delete:
                return web.json_response(
                    status=404
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


    @docs(
        tags=["event"],
        summary="Get one",
        description=("Get one Driving Event item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(EventSchema(), 200)
    async def get_info(self, request):
        event_id = request.match_info['event_id']

        try:
            event = await self.client.get_by_id(id=event_id)
            if not event:
                return web.json_response(
                    status=404,
                    data={}
                )
        except Exception as ex:
            raise ex

        if event is None:
            event = {}

        return web.json_response(
            data=event,
            dumps=custom_dumps
        )


    @docs(
        tags=["event"],
        summary="Driving Event list",
        description=("All Driving Event List"),
        responses=Response().list(DrivingEventListSchema)._401._422._500.build(),
        parameters=Param().paginate()
            .query('startDate', "date")
            .query('endDate')
            .query('driver_id')
            .query('vehicle_id')
            .build()
    )
    async def get_list(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        start_date = request.rel_url.query.get("startDate")
        end_date = request.rel_url.query.get("endDate")
        driver_id = request.rel_url.query.get("driver_id")
        vehicle_id = request.rel_url.query.get("vehicle_id")

        try:
            if isinstance(start_date, datetime.date):
                start_date = str(start_date)
            if isinstance(end_date, datetime.date):
                end_date = str(end_date)
            if isinstance(start_date, datetime.datetime):
                start_date = str(start_date.date())
            if isinstance(end_date, datetime.datetime):
                end_date = str(end_date.date())
        except:
            return VError(detail="date, datetime or str-date expected: '2020-01-30'")

        try:
            if limit and offset:
                vehicles = await db_paginate(
                    limit=int(limit), offset=int(offset),
                    organization_id=org_id,
                    start_date=start_date, end_date=end_date,
                    driver_id=driver_id, vehicle_id=vehicle_id,
                )
            else:
                pass
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": vehicles},
            dumps=custom_dumps
        )


    @docs(
        tags=["event"],
        summary="Bulk Get",
        description=("Get list of Events by ids"),
        responses=Response().list(EventListSchema)._401._422._500.build(),
        parameters=Param().build()
    )
    async def bulk_get(self, data):
        pass


    @docs(
        tags=["event"],
        summary="Bulk Delete",
        description=("Delete Events by ids"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("event_id").build()
    )
    async def bulk_delete(self, data):
        pass


    @docs(
        tags=["event"],
        summary="Bulk Insert",
        description=("Insert Events by ids"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("event_id").build()
    )
    async def bulk_insert(self, data):
        pass


event = Event()
