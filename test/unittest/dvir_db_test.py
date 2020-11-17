import asyncio
from datetime import datetime

import aiounittest

from executors.dvir.dvir_db import *
from executors.utils.enum import DvirStatusDescEnum, DvirStatusCodeEnum


class TestDvirDB(aiounittest.AsyncTestCase):
    data = Dvir({
        "log_id": 1,
        "driver_id": 1,
        "vehicle_id": 1,
        "datetime": datetime.now(),
        "status_code": 1,
        "status_name": "",
        "description": "Someting happened",
        "driver_signature": '',
        "mechanic_signature": '',
    })


    def get_event_loop(self):
        self.my_loop = asyncio.get_event_loop()
        return self.my_loop


    async def test_add(self):
        result = await db_add(data=self.data)
        print("added: ", result)
        self.assertNotEqual(result, None)
        if result:
            self.data.id = result['id']


    async def test_b_details(self):
        result = await db_get_by_log_id(data=self.data)
        print("details: ", result)
        _res = list(filter(lambda d: d['id'] == self.data.id, result))
        self.assertEqual(len(_res), 1)
        self.assertEqual(self.data.id, _res[0]['id'])


    async def test_c_modify(self):
        status_code = DvirStatusCodeEnum.FIXED
        status_name = DvirStatusDescEnum.FIXED
        self.data.status_code = status_code
        self.data.status_name = status_name
        result = await db_modify(data=self.data)
        print("modified: ", result)
        result = await db_get_by_log_id(data=self.data)
        _res = list(filter(lambda d: d['id'] == self.data.id, result))
        self.assertNotEqual(len(_res), 0)
        result = _res[0]
        _status_code = result.get('status_code', "")
        _status_name = result.get('status_name', "")
        self.assertEqual(status_code, _status_code)
        self.assertEqual(status_name, _status_name)


    async def test_d_remove(self):
        result = await db_remove(id=self.data.id)
        print("removed: ", result)
        id = result['id']
        self.assertEqual(self.data.id, id)


aiounittest.run_sync()
