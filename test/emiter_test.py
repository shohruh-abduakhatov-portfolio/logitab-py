import asyncio
import sys
import os


async def test():
    from test.test.test_cli import TestClient2
    # test_client = TestClient()
    test_client2 = TestClient2()
    # res = await test_client.heavy_operations()
    # print("Finished", res)
    res = await test_client2.heavy_operations()
    print("Finished", res)


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(test())
# aiohttp.ClientSession(loop=asyncio.get_event_loop())
