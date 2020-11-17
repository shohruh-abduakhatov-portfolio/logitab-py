from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .groups_executor import GroupsExecutor


@executor(GroupsExecutor)
class GroupsClient(AbstractClient):
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
    async def paginate(self, limit, offset, organization_id):
        pass

    @lpc
    async def search(self, limit, offset, organization_id, text):
        pass

    @lpc
    async def restore(self, data):
        pass
