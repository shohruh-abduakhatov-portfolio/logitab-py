import datetime as _dt

from executors.driver.driver_client import DriverClient
from executors.dvir.dvir_cli import DvirClient
from executors.edited_event.edited_event_cli import EditEventClient
from executors.event.event_cli import EventClient
from executors.log.log_db import *
from executors.models.log import Log
from executors.organization.organization_cli import OrganizationClient
from executors.terminal.terminal_client import TerminalClient
from executors.user.user_client import UserClient
from executors.vehicle.vehicle_client import VehicleClient
from executors.violation.violation_cli import ViolationClient
from modules.core.AbstractExecutor import *


class LogExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'log'
        self.params: Log = Log()


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


    async def get_by_date(self, org_id, start_date, end_date, **kwargs):
        try:
            result = await db_get_by_date(org_id, start_date, end_date, **kwargs)
            assert result
            new_result = {}
            for i in result:
                try:
                    new_result[str(i['date'])].append(i)
                except:
                    new_result[str(i['date'])] = [i]
        except:
            return {}
        return new_result


    async def get_by_id(self, id):
        await self.launch_instance(data={"id": id})
        try:
            await self._fill_sub_obj()
        except Exception as e:
            print(traceback.print_exception())
            print(traceback.print_exc())
            return {}

        return self.params.serialize()


    async def modify(self, data):
        await self.launch_instance(data=data)
        self.params.deserialize(data)
        await self.save({self.pfx + str(self.params.id): None})
        return await self.save_changes()


    async def exists(self, date):
        if isinstance(date, _dt.datetime):
            date = str(date.date())
        elif isinstance(date, _dt.date):
            date = str(date)
        params = await db_exist_date(date=date)
        return params


    # noinspection PyMethodOverriding
    async def paginate(self, limit, offset, organization_id, **kwargs):
        result = await db_paginate(limit, offset, organization_id,
                                   kwargs.get("startDate", ""),
                                   kwargs.get("endDate", ""))
        return result


    async def insert_duty_status(self, data):
        """
        Insert duty status for log events (edited)
        :param data:
        :return:
        """
        pass


    async def edit_event(self, data):
        """
        Edit event for log events (edited)
        :param data:
        :return:
        """
        pass


    async def _fill_sub_obj(self):
        driver = await DriverClient().get_by_id(id=self.params.driver_id)
        assert not driver
        user = await UserClient().get_by_id(id=driver.user_id)
        vehicle = await VehicleClient().get_by_id(id=self.params.vehicle_id)
        terminal = await TerminalClient().get_by_id(id=self.params.terminal_id)
        events = await EventClient().bulk_get_by_log_id(log_id=self.params.id)
        violation = await ViolationClient().get_by_log_id(log_id=self.params.id)
        dvir = await DvirClient().get_by_log_id(log_id=self.params.id)
        organization = await OrganizationClient().get_by_id(log_id=self.params.organization_id)
        edited_events = not self.params.edited_event_ids or \
                        await EditEventClient().bulk_get_by_log_id(log_id=self.params.id)
        self.params.driver = driver or {}
        self.params.user = user or {}
        self.params.vehicle = vehicle or {}
        self.params.terminal = terminal or {}
        self.params.events = events or {}
        self.params.violation = violation or {}
        self.params.dvir = dvir or {}
        self.params.organization = organization or {}
        self.params.edited_events = edited_events or {}


    async def restore(self, data):
        await self.save({self.pfx + str(data['id']): data})
        return True
