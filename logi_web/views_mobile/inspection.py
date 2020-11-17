from aiohttp import web
from aiohttp_apispec import docs
from dateutil.parser import parse

from logi_web.errors import ValidationError as VError, HTTPServiceError
from logi_web.schemas import custom_dumps
from logi_web.swagger.params import Param
from logi_web.utils.pdf import to_pdf


class Inspection:
    def __init__(self) -> None:
        super().__init__()
        pass


    @staticmethod
    # @auth_required(UserRole.DRIVER)
    @docs(
        tags=["mobile-inspection"],
        summary="Get last Logs by date range",
        description=("Get list of Logs by given date range as query"),
        parameters=Param().query('startDate', "date").query('endDate', "date").build()
    )
    async def hand_review(request):
        # https://docs.aiohttp.org/en/2.0.7/web.html#file-uploads
        # https://stackoverflow.com/questions/34121814/aiohttp-serve-single-static-file
        org_id = request.user['org_id']
        start_date = request.rel_url.query.get("startDate")
        end_date = request.rel_url.query.get("endDate")
        try:
            assert start_date and end_date
            start_date = parse(start_date)
            end_date = parse(end_date)
        except:
            return VError(detail="Invalid query, startDate and endDate expected")

        result, driver = {}, {}
        try:
            # Get Events and Log
            from executors.log.log_cli import LogClient
            log_cli = LogClient()
            result: dict = await log_cli.get_by_date(
                org_id=org_id,
                start_date=start_date, end_date=end_date
            )
            if not len(result) or not result:
                return web.json_response(
                    data={"data": {}},
                    dumps=custom_dumps
                )
            # todo get: driver, org, terminal, log, eld, timezone, vehicle
            # Get Driver
            # driver_id = result.values()[0]
            # from executors.driver.driver_client import DriverClient
            # driver_cli = DriverClient()
            # driver = await driver_cli.get_one()
            # assert driver_cli
            data = {}
            location = await to_pdf('inspection.html', 'inspection.pdf', data)

        except Exception as ex:
            return HTTPServiceError(ex.__cause__)

        return web.FileResponse('./index.html')


inspection_mobile = Inspection()
