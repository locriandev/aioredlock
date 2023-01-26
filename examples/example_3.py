"""
2 concurrent tasks:
- task_1 creates a lock with an expire time of 2 secs
- task_1 acquires the lock right away and enters a sleep time.
- task_2 sleeps 2 secs, then tries to acquire the lock
- task_2 acquires the lock that has expired while task_1 was holding it, then enters a sleep time
- task_1 exits sleep time and its context manager goes out of scope, trying to release the lock.
  This will raise an exception, caught by the except block.
- task_2 exits sleeps time, then releases the lock
"""

import asyncio
import logging

from aioredlock import Aioredlock, LockError, LockAcquiringError

from utils import log_config, redis

LOCK_NAME = 'example-3-lock'


async def task_1():
    lock_manager = Aioredlock(redis)
    logger = logging.getLogger('task_1')

    try:
        logger.info('acquiring lock')

        async with await lock_manager.lock(LOCK_NAME, lock_timeout=2) as _:
            logger.info('lock acquired')

            # Do stuff
            await asyncio.sleep(3)

    except LockAcquiringError:
        logger.info('lock timed out')
        assert not await lock_manager.is_locked(LOCK_NAME)

    finally:
        await lock_manager.destroy()


async def task_2():
    lock_manager = Aioredlock(redis)
    logger = logging.getLogger('task_2')
    await asyncio.sleep(2)

    try:
        logger.info('acquiring lock')

        async with await lock_manager.lock(LOCK_NAME) as _:
            logger.info('lock acquired')

            # Do stuff
            await asyncio.sleep(1)

        assert not await lock_manager.is_locked(LOCK_NAME)
        logger.info('lock released')

    except LockError as e:
        logger.error(e)

    finally:
        await lock_manager.destroy()


if __name__ == '__main__':
    log_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*[task_1(), task_2()]))
