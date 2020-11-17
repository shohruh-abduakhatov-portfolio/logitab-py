from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .eld_executor import EldExecutor


@executor(EldExecutor)
class EldClient(AbstractClient):
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

