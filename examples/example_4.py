"""
3 concurrent tasks want to acquire the lock
- task_1 locks it right away, sleeps 1 sec then releases it
- task_2 sleeps 1 sec, tries to acquire it but needs to wait for task_1 to release it
- task_3 sleeps 2 secs, checks if the resource is already locked and quits
"""

import asyncio
import logging

from aioredlock import Aioredlock, LockError

from utils import log_config, redis

LOCK_NAME = 'example-4-lock'


async def task_1():
    logger = logging.getLogger('task_1')
    lock_manager = Aioredlock(redis)

    try:
        logger.info('acquiring lock')

        async with await lock_manager.lock(LOCK_NAME) as _:
            logger.info('lock acquired')
            await asyncio.sleep(1)

        logger.info('lock released')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


async def task_2():
    await asyncio.sleep(1)

    logger = logging.getLogger('task_2')
    lock_manager = Aioredlock(redis, retry_count=10, retry_delay_min=1)

    try:
        logger.info('acquiring lock')

        async with await lock_manager.lock(LOCK_NAME) as _:
            logger.info('lock acquired')
            await asyncio.sleep(2)

        logger.info('lock released')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


async def task_3():
    await asyncio.sleep(2)

    logger = logging.getLogger('task_3')
    lock_manager = Aioredlock(redis)

    try:
        logger.info('checking if resource is already locked')
        if await lock_manager.is_locked(LOCK_NAME):
            logger.info(f'lock {LOCK_NAME} is locked: skipping')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


if __name__ == '__main__':
    log_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        asyncio.gather(
            *[task_1(), task_2(), task_3()]
        )
    )
