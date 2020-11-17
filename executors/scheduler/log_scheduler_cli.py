from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .log_scheduler_exe import LogSchedulerExecutor


@executor(LogSchedulerExecutor)
class LogSchedulerClient(AbstractClient):

    @lpc
    async def run_driver_log_scheduler(self, data):
        pass
