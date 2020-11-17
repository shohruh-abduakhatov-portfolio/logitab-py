from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from asyncpg import UniqueViolationError
from marshmallow import ValidationError

from executors.vehicle.vehicle_client import VehicleClient
from executors.vehicle.vehicle_db import db_get_by_status, db_paginate, db_search
from logi_web.schemas import vehicle_schema, VehicleSchema, VehicleListSchema, custom_dumps, VehicleEditSchema, \
    vehicle_edit_schema
from logi_web.errors import ValidationError as VError, HTTPServiceError
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response


class Vehicle:
    def __init__(self):
        self.client = VehicleClient()


    @docs(
        tags=["vehicle"],
        summary="Create",
        description=("New Vehicle item. 'unit' field request should be: "
                     "```{'1': 1} # {str(vehicle_id): int(vehicle_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response().created('{"vehicle_id": 0}')._401._422._500.build(),
    )
    @request_schema(VehicleSchema)
    async def create_vehicle(self, request):
        org_id = 1
        data = await request.json()

        try:
            validated_data = vehicle_schema.load(data)
            validated_data['organization_id'] = org_id
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            vehicle_id = await self.client.add(data=validated_data)
        except UniqueViolationError as e:
            return VError(detail={e.constraint_name: e.args[0]})
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"vehicle_id": vehicle_id.get('id')}
        )


    @docs(
        tags=["vehicle"],
        summary="Update Vehicle item",
        description=("Update Vehicle item. 'unit' field request should be: "
                     "```{'1': 1} # {str(vehicle_id): int(vehicle_id)}```.\n"
                     "**NOTE: If something uncomfortable with request structure, ask for edit**"),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(VehicleEditSchema)
    @response_schema(VehicleSchema(), 200)
    async def update_vehicle(self, request):
        vehicle_id = request.match_info['vehicle_id']
        data = await request.json()

        data['id'] = int(vehicle_id)
        try:
            validated_data = vehicle_edit_schema.load(data)
        except ValidationError as err:
            return VError(detail=err.messages)

        try:
            vehicle_update = await self.client.modify(data=validated_data)
        except Exception as ex:
            raise ex
        return web.json_response(
            data={"vehicle_id": vehicle_update}
        )


    @docs(
        tags=["vehicle"],
        summary="Delete",
        description=("Delete Vehicle item"),
        responses=Response()._200._401._404._422._500.build(),
        parameters=Param().url_path("vehicle_id").build()
    )
    async def delete_vehicle(self, request):
        vehicle_id = request.match_info['vehicle_id']
        try:
            delete = await self.client.remove(id=int(vehicle_id))
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
        tags=["vehicle"],
        summary="Get one",
        description=("Get one Vehicle item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(VehicleSchema(), 200)
    async def get_vehicle_info(self, request):
        vehicle_id = request.match_info['vehicle_id']
        try:
            result = await self.client.get_by_id(id=vehicle_id)
            if not result:
                return web.json_response(
                    status=404,
                    data={}
                )
        except Exception as ex:
            raise HTTPServiceError()

        result['year'] = str(result.get('year'))

        return web.json_response(
            data=result,
            dumps=custom_dumps,
        )


    @docs(
        tags=["vehicle"],
        summary="Vehicles list",
        description=("All Vehicles List\n"
                     "Status: 1(activated), 0(deactivated)"),
        responses=Response().list(VehicleListSchema)._401._422._500.build(),
        parameters=Param().paginate().query('status', 'int').build()
    )
    async def get_vehicle_list(self, request):
        org_id = 1
        limit = request.rel_url.query.get("limit")
        offset = request.rel_url.query.get("offset")
        status = request.rel_url.query.get("status", 1)

        try:
            if limit and offset:
                vehicles = await db_paginate(
                    limit=int(limit), offset=int(offset), status=int(status),
                    organization_id=org_id)
            else:
                vehicles = await db_get_by_status(org_id, int(status))
        except Exception as ex:
            raise ex

        if vehicles:
            for item in vehicles:
                item['year'] = str(item.get('year'))

        return web.json_response(
            data={"data": vehicles},
            dumps=custom_dumps,
        )

    @docs(
        tags=["vehicle"],
        summary="Search",
        description=("Search for Vehicle item"),
        responses=Response().list(VehicleListSchema)._401._422._500.build(),
        parameters=Param().header("search").paginate().build()
    )
    @response_schema(VehicleSchema(), 200)
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


    @docs(
        tags=["vehicle"],
        summary="Deactivate/Activate Vehicle",
        description=("(De)Activate Vehicle item"),
        responses=Response()._200._400._401._422._500.build(),
        parameters=Param().url_path("vehicle_id").query_req("status", type='int').build()
    )
    async def change_status(self, request):
        vehicle_id = request.match_info['vehicle_id']
        status = request.rel_url.query.get("status")
        if not status:
            return web.json_response(
                status=400
            )
        try:
            response = await self.client.modify_status(
                id=int(vehicle_id), status=int(status))
            if not response:
                return web.json_response(
                    status=500
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200
        )


vehicle = Vehicle()