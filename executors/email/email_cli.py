from modules.core.AbstractClient import *
from modules.core.AbstractExecutor import executor
from .email_exe import EmailExecutor


@executor(EmailExecutor)
class EmailClient(AbstractClient):
    @lpc
    async def send_email(self, to_email, message):
        pass


    @lpc
    async def send_forgotten_password(self, to_email, password, **kwargs):
        pass
