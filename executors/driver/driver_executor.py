from executors.driver.driver_db import *
from executors.eld.eld_client import EldClient
from executors.user import user_db
from executors.user.user_client import UserClient
from executors.vehicle.vehicle_client import VehicleClient
from modules.core.AbstractExecutor import *


class DriverExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'driver'
        self.params: Driver = Driver()


    async def launch_instance(self, data):
        params = await self.get([self.pfx + str(data['id'])])
        assert params
        self.params.deserialize(params)


    async def save_changes(self):
        result = await db_modify(self.params)
        self.params.deserialize(result)
        await self.save({self.pfx + str(self.params.id): self.params.serialize()})
        return result


    async def add(self, data):
        self.params.deserialize(data)

        user_cli = UserClient()
        try:
            data['role'] = 'driver'
            user_result = await user_cli.add(data=data)
            if not user_result['id']:
                return
            self.params.user_id = user_result['id']
        except Exception as e:
            return

        result = await db_add(data=self.params)
        self.params.id = result['id']
        self.params.date_created = datetime.now()
        try:
            await self.save({self.pfx + str(self.params.id): self.params.serialize()})
        except Exception as e:
            await self.remove(self.params.id)
            await user_cli.remove(id=self.params.user_id)

        # if not self.params.id:
        #     from executors.scheduler.log_scheduler_cli import LogSchedulerClient
        #     await LogSchedulerClient().run_driver_log_scheduler(data=self.params.serialize())
        return result


    async def remove(self, id):
        await self.launch_instance(data={"id": id})
        if self.params.user_id != 0:
            await user_db.db_remove(self.params.user_id)
        else:
            await db_remove(self.params)
        await self.save({self.pfx + str(id): None})
        return self.params.serialize()


    async def get_all(self):
        instances = await self._list()
        return instances


    async def get_by_status(self, data):
        self.params.deserialize(data)
        organization_id = self.params.organization_id
        status = self.params.status
        instances = await db_get_by_status(organization_id=organization_id,
                                           status=status)
        return instances


    async def get_by_id(self, id):
        await self.launch_instance(data={"id": id})
        await self._fill_sub_obj()
        return self.params.serialize()


    async def get_one(self, id):
        await self.launch_instance(data={"id": id})
        return self.params.serialize()


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        if self.params.user_id:
            data['id'] = self.params.user_id
            data['role'] = 'driver'
            user_res = await UserClient().modify(data=data)
            user_res['user_id'] = self.params.user_id
            self.params.deserialize(user_res)
        await self.save_changes()
        return self.params.serialize()


    async def modify_status(self, id, status):
        await self.launch_instance(data={"id": id})
        self.params.status = status
        if self.params.user_id != 0:
            user_res = await UserClient().set_status(data={
                "id": self.params.user_id,
                "status": self.params.status
            })
            self.params.status = user_res.status
        await self.save_changes()
        return self.params.serialize()


    # noinspection PyMethodOverriding
    async def paginate(self, limit, offset, organization_id, status):
        result = await db_paginate(limit, offset, status, organization_id)
        return result


    async def search(self, limit, offset, organization_id, text):
        return await db_search(limit, offset, organization_id, text)


    async def _fill_sub_obj(self):
        eld = await EldClient().get_by_id(id=self.params.device_version_id)
        user = await UserClient().get_by_id(id=self.params.user_id)
        vehicle = await VehicleClient().get_by_id(id=self.params.vehicle_id)
        self.params.eld = eld if eld else {}
        self.params.user = user if user else {}
        self.params.vehicle = vehicle if vehicle else {}


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True
