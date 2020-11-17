from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from test.TestExecutor import TestExecutor, TestExecutor2


@executor(TestExecutor)
class TestClient(AbstractClient):

    @rpc
    async def heavy_operations(self):
        pass


@executor(TestExecutor2)
class TestClient2(AbstractClient):

    @rpc
    async def heavy_operations(self):
        pass
