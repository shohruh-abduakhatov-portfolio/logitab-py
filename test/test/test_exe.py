from modules.core.AbstractExecutor import AbstractExecutor


class TestExecutor(AbstractExecutor):

    async def heavy_operations(self):
        print(">> TestExecutor")
        # await asyncio.sleep(5)
        return "TestExecutor > heavy_operations - [OK]"


class TestExecutor2(AbstractExecutor):

    async def heavy_operations(self):
        print(">> TestExecutor2")
        from test.test.test_cli import TestClient
        res = await TestClient().heavy_operations()
        print(">> TestExecutor2", res)
        return "TestExecutor2 > heavy_operations - [OK]"
