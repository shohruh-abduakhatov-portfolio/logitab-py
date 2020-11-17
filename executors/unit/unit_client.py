from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .unit_executor import UnitExecutor


@executor(UnitExecutor)
class UnitClient(AbstractClient):
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


    @lpc
    async def paginate(self, limit, offset):
        pass


    @lpc
    async def search(self, text):
        pass


    @lpc
    async def restore(self, data):
        pass
