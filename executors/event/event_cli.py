from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .event_exe import EventExecutor


@executor(EventExecutor)
class EventClient(AbstractClient):
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
    async def bulk_get_by_log_id(self, log_id):
        pass


    @lpc
    async def bulk_get_by_log_ids(self, data):
        pass


    @lpc
    async def bulk_delete_by_log_id(self, data):
        pass


    @lpc
    async def copy_from_edited_event(self, data):
        pass


    @lpc
    async def get_one(self, id):
        pass


    @lpc
    async def get_all(self):
        pass


    @lpc
    async def restore(self, data):
        pass
