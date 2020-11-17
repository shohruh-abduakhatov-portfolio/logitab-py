from executors.driver.driver_client import DriverClient
from executors.edited_event.edited_event_db import *
from modules.core.AbstractExecutor import *


class EditedEventExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'oe'
        self.params: EditedEvent = EditedEvent()


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


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        return await self.save_changes()


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
            await db_bulk_get(ids, organization_id)
        except:
            return None
        return data['ids']


    async def bulk_get_by_log_id(self, data):
        try:
            log_id = data['log_id']
            assert log_id
        except:
            return {}
        try:
            await db_bulk_get_by_log_id(log_id)
        except:
            return None
        return data['ids']


    async def bulk_delete(self, data):
        try:
            ids = data['ids']
            assert ids
            assert isinstance(ids, (dict, tuple, list))
            if isinstance(ids, dict):
                ids = ids.values()
        except:
            return {}
        try:
            await db_bulk_delete(ids)
        except:
            return None
        return data['ids']


    async def bulk_insert(self, data):
        _data = [{}]
        try:
            assert isinstance(data, dict)
            _data = data.values()
            assert len(_data) != 0
            assert isinstance(_data, dict)
        except:
            return {}
        try:
            res = await db_bulk_insert(_data)
            assert res
            return res
        except:
            return {}


    async def get_one(self, id):
        await self.launch_instance(data={"id": id})
        await self._fill_sub_obj()
        return self.params.serialize()


    async def get_by_status(self, data):
        status_code = data['edited_status_code']
        org_id = data['organization_id']
        driver_id = data['driver_id']
        result = None
        try:
            assert status_code and org_id and driver_id
            result = await db_get_by_status(
                int(status_code),
                int(org_id),
                int(driver_id)
            )
            assert result
        except Exception as e:
            return None, e
        return result, None


    async def get_first_by_status(self, data):
        status_code = data['edited_status_code']
        org_id = data['organization_id']
        driver_id = data['driver_id']
        result = None
        try:
            assert status_code and org_id and driver_id
            result = await db_get_first_by_status(
                int(status_code),
                int(org_id),
                int(driver_id)
            )
            assert result
        except Exception as e:
            return None, e
        return result, None


    async def get_all(self):
        instances = await self._list()
        return instances


    async def request_make_action(self, log_id, accept=True):
        try:
            from executors.log.log_cli import LogClient
            log_cli = LogClient()
            log = await log_cli.modify(data={
                "id": int(log_id),
                "edited_event_ids": {}
            })
            assert log
            if not accept:
                result = await db_bulk_delete_by_log_id(log_id=int(log_id))
                assert result
            else:
                from executors.event.event_cli import EventClient
                event_cli = EventClient()
                data = {"log_id": int(log_id)}
                ids = await event_cli.bulk_delete_by_log_id(data=data)
                assert ids
                result = await event_cli.copy_from_edited_event(data=data)
                assert result
        except Exception as ex:
            raise ex
        return result


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
