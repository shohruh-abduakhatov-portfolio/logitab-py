from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .edit_request_history_exe import EditRequestHistoryExecutor


@executor(EditRequestHistoryExecutor)
class EditRequestHistoryClient(AbstractClient):
    @lpc
    async def add(self, data):
        pass


    @lpc
    async def remove(self, data):
        pass


    @lpc
    async def modify(self, data):
        pass


    @lpc
    async def get_by_log_id(self, log_id):
        pass


    @lpc
    async def restore(self, data):
        pass
