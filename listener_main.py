#!/usr/local/bin/python3.6

import os  # NOQA: E402

import uvloop  # NOQA: E402


os.environ['CORE_CONFIG'] = '/var/www/config.py'  # NOQA: E402
print("config path: ", os.environ['CORE_CONFIG'])
uvloop.install()  # NOQA: E402

from executors.driver.driver_executor import DriverExecutor
from executors.eld.eld_executor import EldExecutor
from executors.groups.groups_executor import GroupsExecutor
from executors.terminal.terminal_executor import TerminalExecutor
from executors.vehicle.vehicle_executor import VehicleExecutor
from executors.fuel_type.fuel_type_exe import FuelTypeExecutor
from executors.issue_states.issue_state_exe import IssueStateExecutor
from executors.unit.unit_executor import UnitExecutor
from executors.user.user_executor import UserExecutor
# import sys
# sys.path.append(os.path.abspath(__file__ + "/../modules/iwpp/"))

# print('>>>%s' % (sys.path))

from modules.core import Logger
from modules.core.QueueListener import QueueListener

from executors.driving_event.driving_event_executor import *


main_loop = asyncio.get_event_loop()

Logger.init(level=logging.DEBUG)


@executor(DrivingEventExecutor)
class DrivingEventExecutorListener(QueueListener):
    async def parse(self, task):
        await DrivingEventExecutor(task).parse()


@executor(TerminalExecutor)
class TerminalExecutorListener(QueueListener):
    async def parse(self, task):
        await TerminalExecutor(task).parse()


@executor(DriverExecutor)
class DriverExecutorListener(QueueListener):
    async def parse(self, task):
        await DriverExecutor(task).parse()


@executor(VehicleExecutor)
class VehicleExecutorListener(QueueListener):
    async def parse(self, task):
        await VehicleExecutor(task).parse()


@executor(EldExecutor)
class EldExecutorListener(QueueListener):
    async def parse(self, task):
        await EldExecutor(task).parse()


@executor(GroupsExecutor)
class GroupsExecutorListener(QueueListener):
    async def parse(self, task):
        await GroupsExecutor(task).parse()


@executor(FuelTypeExecutor)
class FuelTypeExecutorListener(QueueListener):
    async def parse(self, task):
        await FuelTypeExecutor(task).parse()


@executor(IssueStateExecutor)
class IssueStateExecutorListener(QueueListener):
    async def parse(self, task):
        await IssueStateExecutor(task).parse()


@executor(UnitExecutor)
class UnitExecutorListener(QueueListener):
    async def parse(self, task):
        await UnitExecutor(task).parse()


@executor(UserExecutor)
class UserExecutorListener(QueueListener):
    async def parse(self, task):
        await UserExecutor(task).parse()


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
async def initialize_driver_event():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] DrivingEventExecutor")
    main_loop.create_task(DrivingEventExecutorListener().register_listener(main_loop))


async def initialize_terminal():
    await db.query("select current_timestamp")
    inf = await  AbstractExecutor.es.info()
    print("[OK] TerminalExecutor", inf)
    main_loop.create_task(TerminalExecutorListener().register_listener(main_loop))


async def initialize_driver():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] DriverExecutor")
    main_loop.create_task(DriverExecutorListener().register_listener(main_loop))


async def initialize_vehicle():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] VehicleExecutor")
    main_loop.create_task(VehicleExecutorListener().register_listener(main_loop))


async def initialize_eld():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] EldExecutor")
    main_loop.create_task(EldExecutorListener().register_listener(main_loop))


async def initialize_groups():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] GroupsExecutor: ")
    main_loop.create_task(GroupsExecutorListener().register_listener(main_loop))


async def initialize_fuel_type():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] FuelTypeExecutor: ")
    main_loop.create_task(FuelTypeExecutorListener().register_listener(main_loop))


async def initialize_issue_state():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] IssueStateExecutor: ")
    main_loop.create_task(IssueStateExecutorListener().register_listener(main_loop))


async def initialize_unit():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] UnitExecutor: ")
    main_loop.create_task(UnitExecutorListener().register_listener(main_loop))


async def initialize_user():
    await db.query("select current_timestamp")
    # inf = await AbstractExecutor.es.info()
    print("[OK] UserExecutor: ")
    main_loop.create_task(UserExecutorListener().register_listener(main_loop))


main_loop.create_task(initialize_driver())
main_loop.create_task(initialize_driver_event())
main_loop.create_task(initialize_eld())
main_loop.create_task(initialize_fuel_type())
main_loop.create_task(initialize_groups())
main_loop.create_task(initialize_issue_state())
main_loop.create_task(initialize_terminal())
main_loop.create_task(initialize_unit())
main_loop.create_task(initialize_user())
main_loop.create_task(initialize_vehicle())
main_loop.run_forever()
