import datetime

from aiohttp import web
from aiohttp_apispec import (
    request_schema, docs, response_schema
)
from asyncpg import UniqueViolationError
from marshmallow import ValidationError

from executors.driving_event.driving_event_client import DrivingEventClient
from executors.driving_event.driving_event_db import db_paginate, db_search
from executors.event.event_cli import EventClient
from logi_web.errors import ValidationError as VError
from logi_web.schemas import (
    driving_event_schema,
    custom_dumps,
    DrivingEventSchema,
    DrivingEventListSchema, DrivingEditEventSchema, driving_event_edit_schema
)
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class DrivingEvent:
    def __init__(self):
        self.de_client = DrivingEventClient()
        self.event_client = EventClient()


    @docs(
        tags=["driving-event"],
        summary="Create not for web app",
        description=("New driving_event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"driving_event_id": 0}')._401._422._500.build(),
    )
    @request_schema(DrivingEventSchema)
    async def create(self, request):
        org_id = 1
        data = await request.json()

        try:
            serialized_data = driving_event_schema.load(data)
            serialized_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            driving_event_id = await self.event_client.add(data=serialized_data)
        except UniqueViolationError as e:
            return VError(detail={e.constraint_name: e.args[0]})
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"driving_event_id": driving_event_id.get('id')}
        )


    @docs(
        tags=["driving-event"],
        summary="Update Driving Event item",
        description=("Update Driving Event item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(DrivingEditEventSchema)
    async def update(self, request):
        data = await request.json()
        driving_event_id = request.match_info['driving_event_id']

        data['id'] = int(driving_event_id)

        try:
            serialized_data = driving_event_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            driving_event_update = await self.event_client.modify(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=driving_event_update,
            dumps=custom_dumps
        )


    @docs(
        tags=["driving-event"],
        summary="Delete",
        description=("Delete Driving Event item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("driving_event_id").build()
    )
    async def delete(self, request):
        driving_event_id = request.match_info['driving_event_id']

        try:
            delete = await self.event_client.remove(id=int(driving_event_id))
            if not delete:
                return web.json_response(status=404)
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


    @docs(
        tags=["driving-event"],
        summary="Get one",
        description=("Get one Driving Event item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(DrivingEventSchema(), 200)
    async def get_info(self, request):
        driving_event_id = request.match_info['driving_event_id']

        try:
            driving_event = await self.event_client.get_by_id(id=driving_event_id)
            if not driving_event:
                return web.json_response(
                    status=404,
                    data={}
                )
        except Exception as ex:
            raise ex

        if driving_event is None:
            driving_event = {}

        return web.json_response(
            data=driving_event,
            dumps=custom_dumps
        )


    @docs(
        tags=["driving-event"],
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

        vehicles = {}
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
        tags=["driving-event"],
        summary="Search",
        description=("Search for Driving Event item"),
        responses=Response().list(DrivingEventListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    @response_schema(DrivingEventSchema(), 200)
    async def search(self, request):
        org_id = 1
        text = request.headers.get("search")
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")

        vehicles = {}
        try:
            if limit and offset:
                vehicles = await db_search(
                    limit=int(limit),
                    offset=int(offset),
                    organization_id=org_id,
                    text=text)
        except Exception as ex:
            raise ex

        if vehicles:
            for item in vehicles:
                item['year'] = str(item.get('year'))

        return web.json_response(
            data={"data": vehicles},
            dumps=custom_dumps,
            status=200
        )


driving_event = DrivingEvent()
