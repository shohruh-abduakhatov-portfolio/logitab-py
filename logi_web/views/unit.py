from aiohttp import web
from aiohttp_apispec import (
    request_schema, docs, response_schema
)
from marshmallow import ValidationError

from executors.unit.unit_client import UnitClient
from executors.unit.unit_db import db_paginate, db_search
from logi_web.errors import ValidationError as VError, HTTPServiceError
from logi_web.schemas import custom_dumps, UnitEditSchema, unit_edit_schema
from logi_web.schemas import unit_schema, UnitSchema, UnitListSchema
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class Unit:
    def __init__(self):
        self.client = UnitClient()


    @docs(
        tags=["unit"],
        summary="Create",
        description=("Create unit item. 'groups' field request should be: "
                     "```{'1': 1} # {str(group_id): int(group_id)}```.\n"
                     "or as a list ```['1', 1]``` "
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"unit_id": 0}')._401._422._500.build(),
    )
    @request_schema(UnitSchema)
    async def create(self, request):
        org_id = 1
        data = await request.json()

        try:
            if isinstance(data['groups'], list):
                data['groups'] = dict(zip(map(lambda x:
                                              str(x), data['groups']), data['groups']))
            serialized_data = unit_schema.load(data)
            serialized_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            unit_id = await self.client.add(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"unit_id": unit_id.get('id')}
        )


    @docs(
        tags=["unit"],
        summary="Update Unit item",
        description=("Update Unit item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(UnitEditSchema)
    async def update(self, request):
        data = await request.json()
        unit_id = request.match_info['unit_id']

        data['id'] = int(unit_id)

        try:
            if isinstance(data['groups'], list):
                data['groups'] = dict(zip(map(lambda x:
                                              str(x), data['groups']), data['groups']))
            serialized_data = unit_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            unit_update = await self.client.modify(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"unit_id": unit_update},
            dumps=custom_dumps
        )


    @docs(
        tags=["unit"],
        summary="Delete",
        description=("Delete Unit item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("unit_id").build()
    )
    async def delete(self, request):
        unit_id = request.match_info['unit_id']

        try:
            delete = await self.client.remove(id=int(unit_id))
            if not delete:
                return web.json_response(
                    status=404
                )
        except Exception as ex:
            raise HTTPServiceError()

        return web.json_response(
            status=200
        )


    @docs(
        tags=["unit"],
        summary="Get one",
        description=("Get one Unit item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(UnitSchema(), 200)
    async def get_info(self, request):
        unit_id = request.match_info['unit_id']

        try:
            unit = await self.client.get_by_id(id=unit_id)
            if not unit:
                return web.json_response(
                    status=404,
                    data={}
                )
        except Exception as ex:
            raise HTTPServiceError()

        if unit is None:
            unit = {}

        return web.json_response(
            data=unit,
            dumps=custom_dumps
        )


    @docs(
        tags=["unit"],
        summary="Unit list",
        description=("All Unit List"),
        responses=Response().list(UnitListSchema)._401._422._500.build(),
        parameters=Param().paginate().build()
    )
    async def get_list(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")

        units_list = {}
        try:
            if limit and offset:
                units_list = await db_paginate(
                    limit=int(limit), offset=int(offset),
                    organization_id=org_id)
            units = await self.client.get_all()
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": units_list},
            dumps=custom_dumps,
        )


    @docs(
        tags=["unit"],
        summary="Search",
        description=("Search for Unit item"),
        responses=Response().list(UnitListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    async def search(self, request):
        org_id = 1
        text = request.headers.get("search")
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")

        units_list = {}
        try:
            if limit and offset:
                units_list = await db_search(
                    limit=int(limit),
                    offset=int(offset),
                    organization_id=org_id,
                    text=text)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": units_list},
            status=200,
            dumps=custom_dumps,
        )


unit = Unit()
