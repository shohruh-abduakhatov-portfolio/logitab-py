import asyncio
import os  # NOQA: E402
import sys

from executors.event.event_cli import EventClient


sys.path.append(os.path.abspath(__file__ + "/../../../modules/core/"))
sys.path.append(os.path.abspath(__file__ + "/../../../"))
print('>>>%s' % (sys.path))
print(">>>", os.path.abspath(__file__ + "/../../../"))

os.environ['CORE_CONFIG'] = '/var/www/config.py'  # NOQA: E402
print("config path: ", os.environ['CORE_CONFIG'])

from executors.eld.eld_client import EldClient
from executors.eld.eld_db import get_all as EldClient_db

from executors.driver.driver_client import DriverClient
from executors.driver.driver_db import get_all as DriverClient_db

from executors.driving_event.driving_event_client import DrivingEventClient
from executors.driving_event.driving_event_db import get_all as DrivingEventClient_db

from executors.fuel_type.fuel_type_cli import FuelTypeClient
from executors.fuel_type.fuel_type_db import get_all as FuelTypeClient_db

from executors.groups.groups_client import GroupsClient
from executors.groups.groups_db import get_all as GroupsClient_db

from executors.issue_states.issue_state_cli import IssueStateClient
from executors.issue_states.issue_state_db import get_all as IssueStateClient_db

from executors.terminal.terminal_client import TerminalClient
from executors.terminal.terminal_db import get_all as TerminalClient_db

from executors.unit.unit_client import UnitClient
from executors.unit.unit_db import get_all as UnitClient_db

from executors.user.user_client import UserClient
from executors.user.user_db import get_all as UserClient_db

from executors.vehicle.vehicle_client import VehicleClient
from executors.vehicle.vehicle_db import get_all as VehicleClient_db


clients = {
    "eld": (EldClient(), True, EldClient_db),
    "drivers": (DriverClient(), True, DriverClient_db),
    "driving_events": (EventClient(), True, DrivingEventClient_db),
    "fuel_types": (FuelTypeClient(), True, FuelTypeClient_db),
    "groups": (GroupsClient(), True, GroupsClient_db),
    "issue_states": (IssueStateClient(), True, IssueStateClient_db),
    "terminals": (TerminalClient(), True, TerminalClient_db),
    "units": (UnitClient(), True, UnitClient_db),
    "users": (UserClient(), True, UserClient_db),
    "vehicles": (VehicleClient(), True, VehicleClient_db)
}



async def fill_redis():
    for table, (client, allowed, _all) in clients.items():
        if not allowed: continue
        print(table)
        data = await _all()
        length = len(data)
        print("\tsaving")
        for ind, val in enumerate(data):
            print("\t\t", ind + 1, "/", length)
            complete = False
            while not complete:
                try:
                    complete = await client.restore(data=val)
                except Exception as e:
                    raise e
                    print("\t\t[>>] retry", e)
                    await asyncio.sleep(1)
        await asyncio.sleep(3)


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(fill_redis())
