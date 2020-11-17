from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .driving_event_executor import DrivingEventExecutor


@executor(DrivingEventExecutor)
class DrivingEventClient(AbstractClient):

    @lpc
    async def get_all(self):
        pass


    @lpc
    async def paginate(self, limit, offset, organization_id, status, **kwargs):
        pass


    @lpc
    async def search(self, limit, offset, organization_id, text):
        pass
