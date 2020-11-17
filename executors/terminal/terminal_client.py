from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .terminal_executor import TerminalExecutor


@executor(TerminalExecutor)
class TerminalClient(AbstractClient):
    @lpc
    async def add(self, data):
        pass

    @lpc
    async def modify(self, data):
        pass

    @lpc
    async def get_by_id(self, id):
        pass

    @lpc
    async def remove(self, id):
        pass

    @lpc
    async def get_all(self):
        pass

    @lpc
    async def restore(self, data):
        pass