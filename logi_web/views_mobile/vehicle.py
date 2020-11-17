from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from executors.driver.driver_client import DriverClient
from executors.driver.driver_db import db_get_by_user_id
from executors.vehicle.vehicle_client import VehicleClient
from logi_web.errors import HTTPServiceError
from logi_web.middlewares import auth_required
from logi_web.schemas import VehicleSchema, custom_dumps, VehicleEditSchema
from logi_web.swagger.reponse_code import Response
from logi_web.utils.enum import UserRole
from logi_web.views_mobile.schemas import VehicleConfirmationSchema


class Vehicle:
    def __init__(self):
        self.client = VehicleClient()


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_vehicle"],
        summary="Vehicles list",
        description=("All Vehicles List\n"
                     "Status: 1(activated), 0(deactivated)"),
        responses=Response().list(VehicleConfirmationSchema)._401._422._500.build(),
    )
    async def get_vehicle_list(request):
        org_id = request.user['org_id']
        try:
            client = VehicleClient()
            vehicles = await client.get_by_free_vehicles(org_id=org_id)
            assert vehicle
            driver = await db_get_by_user_id(user_id=request.user['id'])
            assert driver
        except Exception as ex:
            return HTTPServiceError()

        return web.json_response(
            data={
                "vehicles": vehicles,
                "driver": driver,
            },
            dumps=custom_dumps,
        )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile_vehicle"],
        summary="Update Vehicle item",
        description=(""),
        responses=Response()._401._422._500.build(),
    )
    @request_schema(VehicleEditSchema)
    @response_schema(VehicleSchema(), 200)
    async def set_vehicle_to_driver(request):
        vehicle_id = request.match_info['vehicle_id']
        driver_id = request.match_info['driver_id']
        try:
            driver_cli = DriverClient()
            vehicle_update = await driver_cli.modify(data={
                'id': int(driver_id),
                'vehicle_id': int(vehicle_id)
            })
        except Exception as ex:
            raise ex
        return web.json_response(
            data={"vehicle_id": vehicle_update}
        )


vehicle = Vehicle()
