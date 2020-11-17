from executors.terminal.terminal_db import *
from modules.core.AbstractExecutor import *


class TerminalTZExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'ttz'
        self.params = {
            "id": 0,
            "title": "",
            "alias": "",
        }


    async def launch_instance(self, data):
        params = await self.get([self.pfx + str(data["id"])])
        for p in params:
            self.params[p] = params[p]


    async def save_changes(self):
        result = await db_modify(self.params)
        for r in result:
            self.params[r] = result[r]
        await self.save({self.pfx + str(self.params['id']): self.params})
        return result


    async def add(self, data):
        for d in data:
            self.params[d] = data[d]
        result = await db_add(data=self.params)
        self.params['id'] = result['id']
        await self.save({self.pfx + str(self.params["id"]): self.params})
        return result


    async def remove(self, id):
        result = await db_remove({"id": id})
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
        for d in data:
            self.params[d] = data[d]
        await self.save({self.pfx + str(self.params["id"]): None})
        await self.save_changes()


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True
