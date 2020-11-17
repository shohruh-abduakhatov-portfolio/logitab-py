from executors.driving_event.driving_event_db import *
from modules.core.AbstractExecutor import *


class DrivingEventExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.pfx = 'e'
        self.params: DrivingEvent = DrivingEvent()


    async def get_all(self):
        instances = await self._list()
        return instances


    # noinspection PyMethodOverriding
    async def paginate(self, limit, offset, organization_id, status, **kwargs):
        result = await db_paginate(limit, offset, organization_id,
                                   kwargs.get("startDate", ""),
                                   kwargs.get("endDate", ""))
        return result


    async def search(self, limit, offset, organization_id, text):
        return await db_search(limit, offset, organization_id, text)
