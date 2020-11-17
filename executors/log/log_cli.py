from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .log_exe import LogExecutor


@executor(LogExecutor)
class LogClient(AbstractClient):
    @lpc
    async def add(self, data):
        pass


    @lpc
    async def modify(self, data):
        pass


    @lpc
    async def get_by_id(self, id):
        pass


    @lpc
    async def remove(self, id):
        pass


    @lpc
    async def exists(self, date):
        pass


    @lpc
    async def get_all(self):
        pass


    @rpc
    async def paginate(self, limit, offset, organization_id):
        pass


    @lpc
    async def search(self, limit, offset, organization_id, text):
        pass


    @lpc
    async def restore(self, data):
        pass


    @lpc
    async def get_by_date(self, org_id, start_date, end_date, **kwargs):
        pass
