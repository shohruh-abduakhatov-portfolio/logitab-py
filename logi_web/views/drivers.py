from aiohttp import web
from aiohttp_apispec import (
    request_schema, docs, response_schema
)
from asyncpg import UniqueViolationError
from marshmallow import ValidationError

from executors.driver.driver_client import DriverClient
from executors.driver.driver_db import db_paginate, db_get_by_status, db_search
from executors.user.user_client import UserClient
from logi_web.errors import HTTPServiceError
from logi_web.errors import ValidationError as VError
from logi_web.errors import ValidationError as ValidError
from logi_web.schemas import custom_dumps, driver_edit_schema, DriverEditSchema
from logi_web.schemas import driver_schema, DriverSchema, DriverListSchema
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response
from logi_web.views.user import user_view


class Drivers:

    @staticmethod
    # @auth_required
    @docs(
        tags=["driver"],
        summary="Create",
        description=("Create Driver item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"driver_id": 0}')._401._422._500.build(),
    )
    @request_schema(DriverSchema)
    async def create_driver(request):
        org_id = 1
        # await user_view.check_permission(request, 'admin')
        driver_client = DriverClient()
        user_client = UserClient()
        data = await request.json()

        try:
            serialized_data = driver_schema.load(data)
            serialized_data['organization_id'] = org_id
        except ValidationError as err:
            raise HTTPServiceError()

        await user_view.is_unique(request)

        try:
            result = await driver_client.add(data=serialized_data)
        except UniqueViolationError as e:
            return VError(detail={e.constraint_name: e.args[0]})
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={
                "driver_id": result.get('id'),
            }
        )


    @staticmethod
    # @auth_required
    @docs(
        tags=["driver"],
        summary="Update Driver item",
        description=("Update Driver item. 'unit' field request should be: "
                     "```{'1': 1} # {str(unit_id): int(unit_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
        parameters=Param().url_path("driver_id").build()
    )
    @request_schema(DriverEditSchema)
    @response_schema(DriverSchema(), 200)
    async def update_driver(request):
        driver_client = DriverClient()
        driver_id = request.match_info['driver_id']
        data = await request.json()

        try:
            serialized_data = driver_edit_schema.load(data)
            serialized_data['id'] = int(driver_id)
        except ValidationError as err:
            return ValidError(detail=err.messages)

        try:
            update = await driver_client.modify(data=serialized_data)
        except Exception as ex:
            raise HTTPServiceError()

        return web.json_response(
            status=200,
            data={"driver_id": update},
            dumps=custom_dumps,
        )


    @staticmethod
    # @auth_required
    # @docs(
    #     tags=["driver"],
    #     summary="Delete",
    #     description=("Delete Driver item"),
    #     responses=Response()._200._401._404._422._500.build(),
    #     parameters=Param().url_path("driver_id").build()
    # )
    async def delete_driver(request):
        driver_client = DriverClient()
        driver_id = request.match_info['driver_id']

        try:
            delete = await driver_client.remove(id=int(driver_id))
            if not delete:
                return web.json_response(
                    status=404
                )
        except Exception as ex:
            raise HTTPServiceError()

        return web.json_response(
            status=200
        )


    @staticmethod
    # @auth_required
    @docs(
        tags=["driver"],
        summary="Get one",
        description=("Get one Driver item"),
        responses=Response()._401._404._422._500.build(),
        # parameters=Param().header("Authorization").build()
    )
    @response_schema(DriverSchema(), 200)
    async def get_driver_info(request):
        driver_client = DriverClient()

        driver_id = request.match_info['driver_id']
        try:
            driver = await driver_client.get_by_id(id=driver_id)
            if not driver:
                return web.json_response(
                    status=404,
                    data={}
                )
        except Exception as ex:
            raise HTTPServiceError()

        if driver is None:
            driver = []

        return web.json_response(
            status=200,
            data=driver,
            dumps=custom_dumps
        )


    @staticmethod
    # @auth_required
    @docs(
        tags=["driver"],
        summary="Drivers list",
        description=("All Drivers List\n"
                     "Status: 1(activated), 0(deactivated)"),
        responses=Response().list(DriverListSchema)._401._422._500.build(),
        parameters=Param().paginate().query('status', 'int').build()
    )
    async def get_driver_list(request):
        driver_client = DriverClient()

        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        status = request.rel_url.query.get("status", 1)

        try:
            if limit and offset:
                drivers = await db_paginate(
                    limit=int(limit), offset=int(offset), status=int(status),
                    organization_id=org_id)
            else:
                drivers = await db_get_by_status(org_id, int(status))
        except Exception as ex:
            raise HTTPServiceError()

        return web.json_response(
            status=200,
            data={"data": drivers},
            dumps=custom_dumps
        )


    @docs(
        tags=["driver"],
        summary="Search",
        description=("Search for Vehicle item"),
        responses=Response().list(DriverListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    @response_schema(DriverSchema(), 200)
    async def search(self, request):
        org_id = 1
        text = request.headers.get("search")
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")

        drivers = {}
        try:
            if limit and offset:
                drivers = await db_search(
                    limit=int(limit),
                    offset=int(offset),
                    organization_id=org_id,
                    text=text)
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": drivers},
            dumps=custom_dumps,
            status=200
        )


    @docs(
        tags=["driver"],
        summary="Deactivate/Activate Driver",
        description=("(De)Activate Driver item"),
        responses=Response()._200._400._401._422._500.build(),
        parameters=Param().url_path("driver_id").query_req("status", type='int').build()
    )
    async def change_status(self, request):
        driver_id = request.match_info['driver_id']
        status = request.rel_url.query.get("status")
        if not status:
            return web.json_response(
                status=400
            )

        try:
            response = await self.client.modify_status(
                id=int(driver_id), status=int(status))
            if not response:
                return web.json_response(
                    status=500
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


driver = Drivers()
