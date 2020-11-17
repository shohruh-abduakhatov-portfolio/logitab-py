from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .edited_event_exe import EditedEventExecutor


@executor(EditedEventExecutor)
class EditEventClient(AbstractClient):
    @lpc
    async def add(self, data):
        pass


    @lpc
    async def remove(self, id):
        pass


    @lpc
    async def modify(self, data):
        pass


    @lpc
    async def bulk_get(self, data):
        pass


    @lpc
    async def bulk_get_by_log_id(self, data):
        pass


    @lpc
    async def bulk_delete(self, data):
        pass


    @lpc
    async def bulk_insert(self, data):
        pass


    @lpc
    async def get_one(self, id):
        pass


    @lpc
    async def get_by_status(self, data):
        pass


    @lpc
    async def get_first_by_status(self, data):
        pass


    @lpc
    async def get_all(self):
        pass


    @lpc
    async def request_make_action(self, log_id, accept):
        pass


    @lpc
    async def restore(self, data):
        pass
