from aiohttp import web
from aiohttp_apispec import docs, response_schema, request_schema
from marshmallow import ValidationError

from executors.eld.eld_client import EldClient
from executors.eld.eld_db import db_paginate, db_get_by_org_id, db_search
from logi_web.errors import ValidationError as VError
from logi_web.schemas import eld_schema, EldSchema, EldListSchema, EldEditSchema, eld_edit_schema
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class Eld:
    def __init__(self):
        self.client = EldClient()


    @docs(
        tags=["eld"],
        summary="Create",
        description=("Create Eld item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"eld_id": 0}')._401._422._500.build(),
    )
    @request_schema(EldSchema)
    async def create_eld(self, request):
        org_id = 1
        data = await request.json()

        try:
            validated_data = eld_schema.load(data)
            validated_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            eld_id = await self.client.add(data=validated_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"eld_id": eld_id.get('id')}
        )


    @docs(
        tags=["eld"],
        summary="Update ELD item",
        description=("Update ELD item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(EldEditSchema)
    @response_schema(EldSchema(), 200)
    async def update_eld(self, request):
        data = await request.json()
        eld_id = request.match_info['eld_id']

        try:
            validated_data = eld_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        validated_data['id'] = int(eld_id)
        try:
            eld_update = await self.client.modify(data=validated_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=eld_update
        )


    @docs(
        tags=["eld"],
        summary="ELDs list",
        description=("All ELDs List"),
        responses=Response().list(EldListSchema)._401._422._500.build(),
        parameters=Param().paginate().build()
    )
    async def get_eld_list(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        try:
            if limit and offset:
                eld_list = await self.client.paginate(limit=int(limit), offset=int(offset), organization_id=org_id)
            else:
                eld_list = await db_get_by_org_id(org_id)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": eld_list}
        )


    @docs(
        tags=["eld"],
        summary="Get one",
        description=("Get one ELD item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(EldSchema(), 200)
    async def get_eld_info(self, request):
        eld_id = request.match_info['eld_id']

        try:
            response = await self.client.get_by_id(id=eld_id)
            if not response:
                return web.json_response(
                    status=404,
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data=response
        )


    @docs(
        tags=["eld"],
        summary="Delete",
        description=("Delete ELD item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("eld_id").build()
    )
    async def delete_eld(self, request):
        eld_id = request.match_info['eld_id']

        try:
            delete = await self.client.remove(id=int(eld_id))
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
        tags=["eld"],
        summary="Search",
        description=("Search for ELD item"),
        responses=Response().list(EldListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    async def search(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        text = request.headers.get("search")

        obj_list = []
        try:
            if limit and offset:
                obj_list = await db_search(
                    limit=int(limit),
                    offset=int(offset),
                    organization_id=org_id,
                    text=text)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": obj_list},
            status=200
        )


eld = Eld()
