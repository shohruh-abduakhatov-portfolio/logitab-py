import asyncio
from datetime import datetime

import aiounittest

from executors.models.dvir import Dvir


class TestDvirExe(aiounittest.AsyncTestCase):
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

    from executors.dvir.dvir_cli import DvirClient
    client = DvirClient()


    def get_event_loop(self):
        self.my_loop = asyncio.get_event_loop()
        return self.my_loop


    async def test_a_add(self):
        result = await self.client.add(data=self.data.serialize())
        print("added: ", result)
        if result:
            self.data.id = result['id']
        self.assertNotEqual(result, None)


    async def test_d_get_by_log_id(self):
        result = await self.client.get_by_log_id(log_id=self.data.log_id)
        print("got: ", result)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result[str(self.data.id)])


    async def test_z_remove(self):
        result = await self.client.remove(data=self.data.serialize())
        print("removed: ", result)

        result = await self.client.get_by_log_id(log_id=self.data.log_id)
        print("got: ", result)
        self.assertIsNotNone(result)
        self.assertIsNone(result.get(str(self.data.id)))

    # async def test_z_remove_b(self):
    #     result = await self.client.remove(data=self.data)
    #     print("removed: ", result)
    #     id = result['category_id']
    #     self.assertEqual(self.data['category_id'], id)
