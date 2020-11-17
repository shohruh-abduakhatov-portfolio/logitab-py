from executors.terminal.terminal_db import *
from executors.terminal_tz.terminal_tz_cli import TerminalTZClient
from modules.core.AbstractExecutor import *


class TerminalExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'te'
        self.params = {
            "id": 0,
            "name": "",
            "state_id": 0,
            "home_terminal_address": "",
            "home_terminal_timezone_id": ""
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


    async def get_all(self):
        instances = await self._list()
        return instances


    async def get_by_id(self, id):
        terminal = await self.get([self.pfx + str(id)])
        if not terminal:
            terminal_tz_cli = TerminalTZClient()
            terminal_tz = await terminal_tz_cli.get_by_id(id=terminal['home_terminal_timezone_id'])
            terminal['home_terminal_timezone'] = terminal_tz
        return terminal


    async def modify(self, data):
        await self.launch_instance(data=data)
        for d in data:
            self.params[d] = data[d]
        await self.save({self.pfx + str(self.params["id"]): None})
        await self.save_changes()


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True
