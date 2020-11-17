from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .driver_executor import DriverExecutor


@executor(DriverExecutor)
class DriverClient(AbstractClient):
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
    async def get_one(self, id):
        pass


    @lpc
    async def get_by_status(self, data):
        pass


    @lpc
    async def remove(self, id):
        pass


    @lpc
    async def get_all(self):
        pass


    @lpc
    async def modify_status(self, id, status):
        pass


    @lpc
    async def paginate(self, limit, offset, status):
        pass


    @lpc
    async def search(self, text):
        pass


    @lpc
    async def restore(self, data):
        pass
