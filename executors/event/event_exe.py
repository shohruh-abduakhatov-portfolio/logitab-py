from executors.driver.driver_client import DriverClient
from executors.event.event_db import *
from executors.models.event import Event
from modules.core.AbstractExecutor import *


class EventExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'e'
        self.params: Event = Event()


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
        return self.params.serialize()


    async def remove(self, id):
        result = await db_remove(id)
        await self.save({self.pfx + str(id): None})
        return result


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        try:
            await self.save_changes()
        except:
            pass
        return self.params.serialize()


    async def bulk_get(self, data):
        try:
            ids = data['ids']
            organization_id = data['organization_id']
            assert ids and organization_id
            assert isinstance(ids, (dict, tuple, list))
            if isinstance(ids, dict):
                ids = ids.values()
        except:
            return {}
        try:
            result = await db_bulk_get(ids, organization_id)
        except:
            return None
        return result


    async def bulk_get_by_log_id(self, log_id):
        try:
            assert log_id
        except:
            return {}
        try:
            result = await db_bulk_get_log_id(log_id)
        except:
            return None
        return result


    async def bulk_get_by_log_ids(self, data):
        try:
            assert data
            log_ids = data.get("log_ids", ())
            assert log_ids
            result = await db_bulk_get_log_ids(log_ids=log_ids)
        except:
            return {}
        return result


    async def bulk_delete_by_log_id(self, data):
        ids = {}
        try:
            log_id = data['log_id']
            assert log_id
            ids = await db_bulk_delete_by_log_id(log_id)
            assert ids
        except:
            return None

        for id in ids:
            await self.save({self.pfx + str(id): None})

        return data['ids']


    async def copy_from_edited_event(self, data):
        try:
            log_id = data['log_id']
            assert log_id
            result = await db_copy_from_edited_event_table(int(log_id))
            assert result
            for row in result:
                await self.save({self.pfx + str(row.id): row})
        except:
            return {}

        return result


    async def get_one(self, id):
        await self.launch_instance(data={"id": id})
        await self._fill_sub_obj()
        return self.params.serialize()


    async def get_all(self):
        instances = await self._list()
        return instances


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True


    async def _fill_sub_obj(self):
        driver = await DriverClient().get_by_id(id=self.params.driver_id)
        vehicle = driver.get("vehicle", {})
        try:
            del driver['vehicle']
        except:
            pass
        self.params.driver = driver if driver else {}
        self.params.vehicle = vehicle
