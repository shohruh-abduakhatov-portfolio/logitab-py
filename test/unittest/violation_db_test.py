import asyncio

import aiounittest

from executors.utils.enum import *
from executors.violation.violation_db import *


class TestViolationDB(aiounittest.AsyncTestCase):
    data = Violation({
        # "id": 0,
        "log_id": 1,
        "violation": "",
        "name": ViolationName.MISSING_SIGNATURE,
        "description": ViolationDesc.MISSING_SIGNATURE,
        "error_level_code": ViolationLevelCodeEnum.FORM_MANAGER_ERRORS,
        "error_level_desc": ViolationLevelCodeClass.FORM_MANAGER_ERRORS,
        "object_name": 'log',
        "field_name": 'signature',
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
        error_level_code = ViolationLevelCodeEnum.APPROACHING_VIOLATIONS
        error_level_desc = ViolationLevelCodeClass.APPROACHING_VIOLATIONS
        self.data.error_level_code = error_level_code
        self.data.error_level_desc = error_level_desc
        result = await db_modify(data=self.data)
        print("modified: ", result)
        result = await db_get_by_log_id(data=self.data)
        _res = list(filter(lambda d: d['id'] == self.data.id, result))
        self.assertNotEqual(len(_res), 0)
        result = _res[0]
        _error_level_code = result.get('error_level_code', "")
        _error_level_desc = result.get('error_level_desc', "")
        self.assertEqual(error_level_code, _error_level_code)
        self.assertEqual(error_level_desc, _error_level_desc)


    async def test_d_remove(self):
        result = await db_remove(id=self.data.id)
        print("removed: ", result)
        id = result['id']
        self.assertEqual(self.data.id, id)


aiounittest.run_sync()
