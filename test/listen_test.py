#!/usr/local/bin/python3.6

from test.test.test_exe import TestExecutor, TestExecutor2
from modules.core.QueueListener import QueueListener
from modules.core.AbstractExecutor import executor
from modules.core import Logger
import asyncio
import logging

import os


os.environ['CORE_CONFIG'] = '/var/www/config.py'


main_loop = asyncio.get_event_loop()

Logger.init(level=logging.DEBUG)


# Регистрируем наш слушатель - он принимает сообщения из очереди rabbitMQ

@executor(TestExecutor)
class TestExecutorListener(QueueListener):
    async def parse(self, task):
        await TestExecutor(task).parse()


@executor(TestExecutor2)
class TestExecutorListener2(QueueListener):
    async def parse(self, task):
        await TestExecutor2(task).parse()


async def initialize():
    main_loop.create_task(TestExecutorListener()
                          .register_listener(main_loop))


async def initialize2():
    main_loop.create_task(TestExecutorListener2()
                          .register_listener(main_loop))


main_loop.create_task(initialize())
main_loop.create_task(initialize2())
main_loop.run_forever()
#


# main_loop.create_task(TestExecutorListener().register_listener(main_loop))
# main_loop.run_forever()
