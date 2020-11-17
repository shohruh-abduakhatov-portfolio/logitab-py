from aiohttp import web
from aiohttp_apispec import docs

from executors.fuel_type.fuel_type_cli import FuelTypeClient
from logi_web.schemas import FuelTypeListSchema
from logi_web.swagger.reponse_code import Response


class FuelType:
    def __init__(self):
        self.client = FuelTypeClient()


    @docs(
        tags=["fuel_type"],
        summary="List",
        description=("All FueltType List"),
        responses=Response().list(FuelTypeListSchema)._401._422._500.build(),
    )
    async def get_list(self, request):
        try:
            obj_list = await self.client.get_all()
            assert obj_list
            obj_list = list(obj_list.values())
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data={"data": obj_list},
        )


fuel_type = FuelType()
