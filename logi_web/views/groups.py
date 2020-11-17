from aiohttp import web
from aiohttp_apispec import docs, response_schema, request_schema
from marshmallow import ValidationError

from executors.groups.groups_client import GroupsClient
from executors.groups.groups_db import db_get_by_org_id, db_paginate, db_search
from logi_web.errors import ValidationError as VError
from logi_web.schemas import (
    group_schema, GroupSchema, GroupListSchema, GroupEditSchema, group_edit_schema
)
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class Groups:
    def __init__(self):
        self.client = GroupsClient()


    @docs(
        tags=["group"],
        summary="Create",
        description=("Update Groups item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"groups_id": 0}')._401._422._500.build(),
    )
    @request_schema(GroupSchema)
    async def create(self, request):
        org_id = 1
        data = await request.json()

        try:
            serialized_data = group_schema.load(data)
            serialized_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            groups_id = await self.client.add(data=serialized_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"groups_id": groups_id.get('id')}
        )


    @docs(
        tags=["group"],
        summary="Update Groups item",
        description=("Update Groups item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(GroupEditSchema)
    @response_schema(GroupSchema(), 200)
    async def update(self, request):
        data = await request.json()
        groups_id = request.match_info['group_id']

        try:
            validated_data = group_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        validated_data['id'] = int(groups_id)
        try:
            groups_update = await self.client.modify(data=validated_data)
        except Exception as ex:
            raise ex

        return web.json_response(
            data=groups_update
        )


    @docs(
        tags=["group"],
        summary="Groups list",
        description=("All Groups List"),
        responses=Response().list(GroupListSchema)._401._422._500.build(),
        parameters=Param().paginate().build()
    )
    async def get_list(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        try:
            if limit and offset:
                groupss = await db_paginate(
                    limit=int(limit), offset=int(offset), organization_id=org_id)
            else:
                groupss = await db_get_by_org_id(org_id)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": groupss}
        )


    @docs(
        tags=["group"],
        summary="Get one",
        description=("Get one Groups item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(GroupSchema(), 200)
    async def get_info(self, request):
        groups_id = request.match_info['group_id']

        try:
            response = await self.client.get_by_id(id=groups_id)
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
        tags=["group"],
        summary="Delete",
        description=("Delete Groups item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("group_id").build()
    )
    async def delete(self, request):
        groups_id = request.match_info['group_id']

        try:
            delete = await self.client.remove(id=int(groups_id))
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
        tags=["group"],
        summary="Search",
        description=("Search for Groups item"),
        responses=Response().list(GroupListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    async def search(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        text = request.headers.get("search")

        groupss = []
        try:
            if limit and offset:
                groupss = await db_search(
                    limit=int(limit),
                    offset=int(offset),
                    organization_id=org_id,
                    text=text)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": groupss},
            status=200
        )


groups = Groups()
