"""
Similar to example_4, but each task runs in a dedicated process
"""

import asyncio
import logging
import multiprocessing
import os

from aioredlock import Aioredlock, LockError

from utils import log_config, redis

lock_name = 'example-5-lock'


async def task_1():
    logger = logging.getLogger(f'task_1 [{os.getpid()}]')
    lock_manager = Aioredlock(redis)

    try:
        async with await lock_manager.lock(lock_name) as _:
            logger.info('lock acquired')
            await asyncio.sleep(1)

        logger.info('lock released')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


async def task_2():
    logger = logging.getLogger(f'task_2 [{os.getpid()}]')
    lock_manager = Aioredlock(redis, retry_count=10, retry_delay_min=1)

    try:
        async with await lock_manager.lock(lock_name) as _:
            logger.info('lock acquired')
            await asyncio.sleep(1)

        logger.info('lock released')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


async def task_3():
    logger = logging.getLogger(f'task_3 [{os.getpid()}]')
    lock_manager = Aioredlock(redis, retry_count=10, retry_delay_min=1)

    try:
        await asyncio.sleep(2)
        if await lock_manager.is_locked(lock_name):
            logger.info(f'{lock_name} already locked: skipping')

    finally:
        await lock_manager.destroy()


if __name__ == '__main__':
    log_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    multiprocessing.Process(target=lambda: loop.run_until_complete(task_1())).start()
    multiprocessing.Process(target=lambda: loop.run_until_complete(task_2())).start()
    multiprocessing.Process(target=lambda: loop.run_until_complete(task_3())).start()
