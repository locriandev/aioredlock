"""
Show how to use a context manager to lock/unlock resources
"""

import asyncio
import logging

from aioredlock import Aioredlock, LockError

from utils import log_config, redis


LOCK_NAME = 'example-2-lock'


async def task():
    logger = logging.getLogger('example_2')
    lock_manager = Aioredlock(redis)

    try:
        logger.info('acquiring lock')

        # Acquire the lock with a context manager - no need to explicitly unlock
        async with await lock_manager.lock(LOCK_NAME, lock_timeout=3600) as _:
            logger.info('lock acquired')
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
    loop.run_until_complete(task())
