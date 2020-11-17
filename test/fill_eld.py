import asyncio

from executors.eld.eld_client import EldClient


data = [
    {
        "organization_id": 1,
        "serial_no": "string 1",
        "device_version": "string _1",
        "notes": "string 1",
    }, {
        "organization_id": 1,
        "serial_no": "string 3",
        "device_version": "string _3",
        "notes": "string 3",
    }, {
        "organization_id": 1,
        "serial_no": "string 4",
        "device_version": "string _4",
        "notes": "string 4",
    }, {
        "organization_id": 1,
        "serial_no": "string 5",
        "device_version": "string _5",
        "notes": "string 5",
    }, {
        "organization_id": 1,
        "serial_no": "string 6",
        "device_version": "string _6",
        "notes": "string 6",
    }, {
        "organization_id": 1,
        "serial_no": "string 7",
        "device_version": "string _7",
        "notes": "string 7",
    }, {
        "organization_id": 1,
        "serial_no": "string 9",
        "device_version": "string _9",
        "notes": "string 9",
    }, {
        "organization_id": 1,
        "serial_no": "string 10 ",
        "device_version": "string _10",
        "notes": "string 10 ",
    }, {
        "organization_id": 1,
        "serial_no": "string 11",
        "device_version": "string _11",
        "notes": "string 11",
    }, {
        "organization_id": 1,
        "serial_no": "string 12",
        "device_version": "string _12",
        "notes": "string 12",
    }, {
        "organization_id": 1,
        "serial_no": "string 13",
        "device_version": "string _13",
        "notes": "string 13",
    }, {
        "organization_id": 1,
        "serial_no": "string 14",
        "device_version": "string _14",
        "notes": "string 14",
    }, {
        "organization_id": 1,
        "serial_no": "string 15",
        "device_version": "string _15",
        "notes": "string 15",
    }, {
        "organization_id": 1,
        "serial_no": "string 16",
        "device_version": "string _16",
        "notes": "string 16",
    }, {
        "organization_id": 1,
        "serial_no": "string 17",
        "device_version": "string _17",
        "notes": "string 17",
    }, {
        "organization_id": 1,
        "serial_no": "string 18",
        "device_version": "string _18",
        "notes": "string 18",
    }, {
        "organization_id": 1,
        "serial_no": "string 19",
        "device_version": "string _19",
        "notes": "string 19",
    }, {
        "organization_id": 1,
        "serial_no": "string 20",
        "device_version": "string _20",
        "notes": "string 20",
    }, {
        "organization_id": 1,
        "serial_no": "string 21",
        "device_version": "string _21",
        "notes": "string 21",
    }, {
        "organization_id": 1,
        "serial_no": "string 22",
        "device_version": "string _22",
        "notes": "string 22",
    }, {
        "organization_id": 1,
        "serial_no": "string 23",
        "device_version": "string _23",
        "notes": "string 23",
    }, {
        "organization_id": 1,
        "serial_no": "string 24",
        "device_version": "string _24",
        "notes": "string 24",
    }, {
        "organization_id": 1,
        "serial_no": "string 25",
        "device_version": "string _25",
        "notes": "string 25",
    }, {
        "organization_id": 1,
        "serial_no": "string 26",
        "device_version": "string _26",
        "notes": "string 26",
    }, {
        "organization_id": 1,
        "serial_no": "string 27",
        "device_version": "string _27",
        "notes": "string 27",
    }, {
        "organization_id": 1,
        "serial_no": "string 28",
        "device_version": "string _28",
        "notes": "string 28",
    }
]


async def fill_data():
    cli = EldClient()
    for i in data:
        await cli.add(data=i)


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(fill_data())
