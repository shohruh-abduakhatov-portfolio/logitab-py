import asyncio

from executors.groups.groups_client import GroupsClient


data = [
    {
          "organization_id": 1,
        "units": {"1": 1},
        "name": "string 1",
        "note": "string 1",
    } , {
            "organization_id": 1,
        "units": {},
        "name": "string 3",
        "note": "string 3",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 4",
        "note": "string 4",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 5",
        "note": "string 5",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 6",
        "note": "string 6",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 7" ,
        "note": "string 7" ,
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 9",
        "note": "string 9",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 10 ",
        "note": "string 10 ",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 11",
        "note": "string 11",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 12",
        "note": "string 12",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 13",
        "note": "string 13",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 14",
        "note": "string 14",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 15",
        "note": "string 15",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 16",
        "note": "string 16",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 17",
        "note": "string 17",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 18",
        "note": "string 18",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 19",
        "note": "string 19",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 20",
        "note": "string 20",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 21",
        "note": "string 21",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 22",
        "note": "string 22",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 23",
        "note": "string 23",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 24",
        "note": "string 24",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 25",
        "note": "string 25",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 26",
        "note": "string 26",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 27",
        "note": "string 27",
    }, {
            "organization_id": 1,
        "units": {},
        "name": "string 28",
        "note": "string 28",
    }
]


async def fill_data():
      cli = GroupsClient()
      for i in data:
            await cli.add(data=i)
main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(fill_data())