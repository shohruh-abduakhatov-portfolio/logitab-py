import asyncio
from datetime import datetime

import aiounittest

from executors.edit_request_history.edit_request_history_db import *
from executors.utils.enum import EditRequestHistoryDescEnum, EditRequestHistoryCodeEnum


class TestEditRequestHistoryDB(aiounittest.AsyncTestCase):
    data = EditRequestHistory({
        # "id": 0,
        "log_id": 1,
        "created_datetime": datetime.now(),
        "status_name": EditRequestHistoryCodeEnum.WAITING,
        "status_desc": EditRequestHistoryDescEnum.WAITING,
    })


    def get_event_loop(self):
        self.my_loop = asyncio.get_event_loop()
        return self.my_loop


    async def test_a_add(self):
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
        status_name = EditRequestHistoryCodeEnum.APPROVED
        status_desc = EditRequestHistoryDescEnum.APPROVED
        self.data.status_name = status_name
        self.data.status_desc = status_desc
        result = await db_modify(data=self.data)
        print("modified: ", result)
        result = await db_get_by_log_id(data=self.data)
        _res = list(filter(lambda d: d['id'] == self.data.id, result))
        self.assertNotEqual(len(_res), 0)
        result = _res[0]
        _status_name = result.get('status_name', "")
        _status_desc = result.get('status_desc', "")
        self.assertEqual(status_name, _status_name)
        self.assertEqual(status_desc, _status_desc)


    async def test_d_remove(self):
        result = await db_remove(id=self.data.id)
        print("removed: ", result)
        id = result['id']
        self.assertEqual(self.data.id, id)


aiounittest.run_sync()
