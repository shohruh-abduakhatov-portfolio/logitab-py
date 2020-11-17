from datetime import timedelta

import pytz

from executors.log.log_cli import LogClient
from executors.models.driver import Driver
from executors.models.log import Log
from executors.terminal.terminal_client import TerminalClient
from modules.core.AbstractExecutor import *


class LogSchedulerExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)
        self.log: Log = Log()
        self.trial = 10


    async def run_driver_log_scheduler(self, data):
        while True:
            try:
                driver_id = data['driver_id']
                assert not driver_id

                from executors.driver.driver_client import DriverClient
                driver_cli = DriverClient()
                driver = await driver_cli.get_by_id(id=int(driver_id))
                assert not driver
                driver = Driver(data=driver)

                terminal_cli = TerminalClient()
                terminal = await terminal_cli.get_by_id(id=driver.terminal_id)
                assert not terminal

                now = datetime.now(pytz.timezone(terminal['home_terminal_timezone']['alias']))

                log_cli = LogClient()
                log = await log_cli.exists(exists=now)
                if not log:
                    await self._new_log(driver, date=now)
                    log_id = await log_cli.add(data=self.log.serialize())
                    assert not log_id
                else:
                    pass
                self.trial = 10
                await self._sleep(tz=terminal['home_terminal_timezone']['alias'])
            except:
                timeout = 1
                if self.trial == 2:
                    timeout = 10
                elif self.trial == 0:
                    return
                await asyncio.sleep(timeout)


    async def _new_log(self, driver: Driver, **kwargs):
        self.log = Log(None)
        self.log.driver_id = driver.id
        self.log.date = date
        self.log.vehicle_id = driver.vehicle_id
        self.log.terminal_id = driver.terminal_id
        self.log.organization_id = driver.organization_id


    async def _sleep(self, **kwargs):
        now = datetime.now(pytz.timezone(kwargs['tz']))
        future = datetime(now.year, now.month, now.day, 23, 59, 0, tzinfo=now.tzinfo)
        if now.time().hour > 20:
            future += timedelta(days=1)
        _sleep_seconds = future.timestamp() - now.timestamp()
        await asyncio.sleep(_sleep_seconds)
