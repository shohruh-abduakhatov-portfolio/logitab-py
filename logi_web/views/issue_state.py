from aiohttp import web
from aiohttp_apispec import docs

from executors.issue_states.issue_state_cli import IssueStateClient
from logi_web.schemas import IssueStateListSchema
from logi_web.swagger.reponse_code import Response


class IssueState:
    def __init__(self):
        self.client = IssueStateClient()


    @docs(
        tags=["issue_state"],
        summary="List",
        description=("All IssueState List"),
        responses=Response().list(IssueStateListSchema)._401._422._500.build(),
    )
    async def get_list(self, request):
        try:
            obj_list = await self.client.get_all()
            assert obj_list
            obj_list = list(obj_list.values())
        except Exception as ex:
            raise {}

        return web.json_response(
            status=200,
            data={"data": obj_list},
        )


issue_state = IssueState()
