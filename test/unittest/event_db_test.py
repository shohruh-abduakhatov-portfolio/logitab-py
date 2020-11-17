import asyncio
from datetime import datetime

import aiounittest

from executors.event.event_db import *
from executors.models.event import Event
from executors.utils.enum import EventStatus


class TestEventDB(aiounittest.AsyncTestCase):
    data = Event({
        "log_id": 1,
        "start_datetime": datetime.now(),
        "start_odometer": 0.,
        "start_engine_hours": 0.,
        "duration": 0,
        "from_address": "",
        "to_address": "",
        "distance": 0,
        "notes": "",
        "driver_id": 1,
        "unit_id": 2,
        "vehicle_id": 1,
        "organization_id": 1,
        "current_address": "",
        "current_lon": 0.,
        "current_lat": 0.,
        "time_minute": 0,
        "event_status": 'off'
    })
    data_list = [data]


    def get_event_loop(self):
        self.my_loop = asyncio.get_event_loop()
        return self.my_loop


    # async def test_add(self):
    #     result = await db_add(data=self.data)
    #     print("added: ", result)
    #     self.assertNotEqual(result, None)
    #     if result:
    #         self.data.id = result['id']
    #
    #
    # async def test_b_details(self):
    #     result = await db_bulk_get_log_id(log_id=self.data.log_id)
    #     print("details: ", result)
    #     _res = list(filter(lambda d: d['id'] == self.data.id, result))
    #     self.assertEqual(len(_res), 1)
    #     self.assertEqual(self.data.id, _res[0]['id'])



    async def test_b_details(self):
        result = await db_bulk_get_log_ids(log_id=self.data.log_id)
        print("details: ", result)
        _res = list(filter(lambda d: d['id'] == self.data.id, result))
        self.assertEqual(len(_res), 1)
        self.assertEqual(self.data.id, _res[0]['id'])


    # async def test_bb_copy_from_edited_event_table(self):
    #     result = await db_copy_from_edited_event_table(
    #         log_id=self.data.log_id,
    #         organization_id=self.data.organization_id)
    #     print("details: ", result)
    #     self.assertNotEqual(len(result), 0)
    #
    #
    # async def test_c_modify(self):
    #     event_status = EventStatus.ON
    #     self.data.event_status = event_status
    #     result = await db_modify(data=self.data)
    #     print("modified: ", result)
    #     result = await db_bulk_get_log_id(log_id=self.data.log_id)
    #     _res = list(filter(lambda d: d['id'] == self.data.id, result))
    #     self.assertNotEqual(len(_res), 0)
    #     result = _res[0]
    #     _event_status = result.get('event_status', "")
    #     self.assertEqual(event_status, _event_status)


    # bulk delete

    # async def test_zzz_bulk_get_log_id(self):
    #     result = await db_bulk_get(id=self.data_list)
    #     print("removed: ", result)
    #     id = result['id']
    #     self.assertEqual(self.data.id, id)
    #
    #
    # async def test_zzz_bulk_delete(self):
    #     result = await db_remove(id=self.data.id)
    #     print("removed: ", result)
    #     id = result['id']
    #     self.assertEqual(self.data.id, id)

    # async def test_z_remove(self):
    #     result = await db_remove(id=self.data.id)
    #     print("removed: ", result)
    #     id = result['id']
    #     self.assertEqual(self.data.id, id)


aiounittest.run_sync()
