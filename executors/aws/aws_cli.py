from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .aws_exe import AwsExecutor


@executor(AwsExecutor)
class AwsClient(AbstractClient):
    @lpc
    async def test(self):
        pass


    @lpc
    async def delete_file(self, filename):
        pass


    @lpc
    async def push_file(self, file, filename: str):
        pass


    @lpc
    async def push_report(self, file, filename):
        pass


    @lpc
    async def push_signature(self, file, filename):
        pass
