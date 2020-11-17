import smtplib
import ssl

from config_loader import child_config
from modules.core.AbstractExecutor import *


class EmailExecutor(AbstractExecutor):

    def __init__(self, task):
        super().__init__(task)


    async def send_email(self, to_email, message):
        """
        https://realpython.com/python-send-email/
        :param to_email:
        :param message:
        :return:
        """
        port = child_config.email_port  # For SSL
        smtp_server = child_config.smtp_server
        sender_email = child_config.email_from
        password = child_config.email_password

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, message)

        except Exception as e:
            raise e

    async def send_vith_attachment(self, to_email):
        pass

    async def send_forgotten_password(self, to_email, password, **kwargs):
        message = ("To: {}"
                   "Subject: Forgot password\n\n"
                   "Your password is: {}"
                   ).format(to_email, password)
        try:
            await self.send_email(to_email, message)
        except Exception as e:
            return False, e
        return True, None
