from aiohttp import web
from aiohttp_apispec import docs, response_schema
from dateutil.parser import parse

from logi_web.errors import ValidationError as VError
from logi_web.middlewares import auth_required
from logi_web.schemas import custom_dumps, LogSchema
from logi_web.swagger.params import Param
from logi_web.swagger.reponse_code import Response
from logi_web.utils.enum import UserRole


class Log:
    def __init__(self) -> None:
        super().__init__()
        pass


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile-log"],
        summary="Get last Logs by date range",
        description=("Get list of Logs by given date range as query"),
        parameters=Param().query('startDate', "date").query('endDate', "date").build()
    )
    async def get_by_date(request):
        org_id = request.user['org_id']
        start_date = request.rel_url.query.get("startDate")
        end_date = request.rel_url.query.get("endDate")
        try:
            assert start_date and end_date
            start_date = parse(start_date)
            end_date = parse(end_date)
        except:
            return VError(detail="Invalid query, startDate and endDate expected")

        result = {}
        try:
            from executors.log.log_cli import LogClient
            log_cli = LogClient()
            vehicles = await log_cli.get_by_date(
                org_id=org_id,
                start_date=start_date, end_date=end_date
            )
        except Exception as ex:
            raise ex

        return web.json_response(
            data={"data": vehicles},
            dumps=custom_dumps
        )


    @staticmethod
    @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile-log"],
        summary="Get one",
        description=("Get one Groups item"),
        responses=Response()._401._404._422._500.build(),
    )
    @response_schema(LogSchema(), 200)
    async def get_info(self, request):
        log_id = request.match_info['log_id']

        try:
            from executors.log.log_cli import LogClient
            cli = LogClient()
            response = await cli.get_by_id(id=log_id)
            if not response:
                return web.json_response(
                    status=404,
                )
        except Exception as ex:
            raise ex

        return web.json_response(
            status=200,
            data=response,
            dumps=custom_dumps,
        )


log_mobile = Log()
