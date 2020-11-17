import asyncio

import os  # NOQA: E402


os.environ['CORE_CONFIG'] = '/var/www/config.py'  # NOQA: E402
print("config path: ", os.environ['CORE_CONFIG'])


async def test():
    from executors.eld.eld_client import EldClient
    # test_client = TestClient()
    eld_client = EldClient()
    # res = await test_client.heavy_operations()
    # print("Finished", res)
    res = await eld_client.paginate(limit=10, offset=0, organization_id=1)
    print("Finished", res)


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(test())
