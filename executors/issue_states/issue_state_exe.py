from executors.issue_states.issue_state_db import *
from executors.models.issue_state import IssueState
from modules.core.AbstractExecutor import *


class IssueStateExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'is'
        self.params: IssueState = IssueState()


    async def launch_instance(self, data):
        params = await self.get([self.pfx + str(data['id'])])
        self.params.deserialize(params)


    async def save_changes(self):
        result = await db_modify(self.params)
        self.params.deserialize(result)
        await self.save({self.pfx + str(self.params.id): self.params.serialize()})
        return result


    async def add(self, data):
        self.params.deserialize(data)
        result = await db_add(data=self.params)
        self.params.id = result['id']
        await self.save({self.pfx + str(self.params.id): self.params.serialize()})
        return result


    async def remove(self, id):
        result = await db_remove(id)
        await self.save({self.pfx + str(id): None})
        return result


    async def get_all(self):
        instances = await self._list()
        return instances


    async def get_by_id(self, id):
        driver = await self.get([self.pfx + str(id)])
        return driver


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        await self.save({self.pfx + str(self.params.id): None})
        return await self.save_changes()

    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True