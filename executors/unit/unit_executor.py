from executors.driver.driver_client import DriverClient
from executors.groups.groups_client import GroupsClient
from executors.models.unit import Units
from executors.unit.unit_db import *
from modules.core.AbstractExecutor import *


class UnitExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'unit'
        self.params: Units = Units()


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
        await self.launch_instance(data={"id": id})
        await self._fill_sub_obj()
        return self.params.serialize()


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        # await self.save({self.pfx + str(self.params.id): None})
        return await self.save_changes()


    async def paginate(self, limit, offset, organization_id):
        """
        :type offset: int
        :type limit: int
        :type organization_id: int
        """
        result = await db_paginate(limit, offset, organization_id)
        return result


    async def search(self, limit, offset, organization_id, text):
        return await db_search(limit, offset, organization_id, text)

    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True

    async def _fill_sub_obj(self):
        driver = await DriverClient().get_by_id(id=self.params.driver_id)
        groups = {}
        for group_id in self.params.groups.keys():
            groups[group_id] = await GroupsClient().get_by_id(id=group_id)
        self.params.driver = driver if driver else {}
        self.params.groups = groups if groups else {}
        self.params.vehicle = driver.get("vehicle", {})
        try:
            del self.params.driver.vehicle
        except:
            pass

