from executors.eld.eld_client import EldClient
from executors.fuel_type.fuel_type_cli import FuelTypeClient
from executors.issue_states.issue_state_cli import IssueStateClient
from executors.vehicle.vehicle_db import *
from modules.core.AbstractExecutor import *


class VehicleExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 've'
        self.params: Vehicle = Vehicle()


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


    async def get_by_free_vehicles(self, org_id, **kwargs):
        status = 1
        if not org_id: return None, None
        try:
            result = await db_get_by_status(int(org_id), status)
        except Exception  as e:
            return None, e
        return result


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        # await self.save({self.pfx + str(self.params.id): None})
        return await self.save_changes()


    async def modify_status(self, id, status):
        await self.launch_instance(data={"id": id})
        self.params.status = status
        # await self.save({self.pfx + str(self.params.id): None})
        return await self.save_changes()


    # noinspection PyMethodOverriding
    async def paginate(self, limit, offset, organization_id, status):
        result = await db_paginate(limit, offset, status, organization_id)
        return result


    async def search(self, limit, offset, organization_id, text):
        return await db_search(limit, offset, organization_id, text)


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True


    async def _fill_sub_obj(self):
        eld = await EldClient().get_by_id(id=self.params.eld_id)
        fuel_type = await FuelTypeClient().get_by_id(id=self.params.fuel_type_id)
        issue_state = await IssueStateClient().get_by_id(id=self.params.plate_issue_state_id)
        self.params.fuel_type = fuel_type if fuel_type else {}
        self.params.plate_issue_state = issue_state if issue_state else {}
        self.params.eld = eld if eld else {}
