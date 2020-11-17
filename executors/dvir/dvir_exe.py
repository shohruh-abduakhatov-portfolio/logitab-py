from executors.dvir.dvir_db import *
from executors.models.dvir import Dvir
from modules.core.AbstractExecutor import *


class DvirExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'dvir'
        self.params: Dvir = Dvir()
        self.params_dict: {Dvir} = dict()


    async def launch_instance(self, data):
        params = await self.get([self.pfx + str(data['log_id'])])
        if not params:
            params = {}
        self.params_dict = params
        return params


    async def save_changes(self):
        pass


    async def add(self, data):
        self.params.deserialize(data)
        result = await db_add(data=self.params)
        self.params.id = result['id']
        try:
            await self.save({self.pfx + str(self.params.log_id): None})
        except:
            pass
        try:
            await self.save({
                self.pfx + str(self.params.log_id): {
                    self.params.id: self.params.serialize()
                }})
        except:
            pass
        return result


    async def remove(self, data):
        self.params.deserialize(data)
        await self.launch_instance(data=data)
        try:
            self.params_dict.pop(str(self.params.id))
        except:
            return None
        result = None
        try:
            result = await db_remove(self.params.id)
            await self.save({self.pfx + str(self.params.log_id): None})
            await self.save({
                self.pfx + str(self.params.log_id): self.params_dict
            })
        except:
            pass
        return result


    async def modify(self, data):
        pass


    async def get_by_log_id(self, log_id):
        await self.launch_instance(data={"log_id": log_id})
        return self.params_dict


    async def restore(self, data):
        await self.add(data=data)
        return True
