"""
Show simple lock/unlock operations
"""

import asyncio
import logging

from aioredlock import Aioredlock, LockError

from utils import log_config, redis


LOCK_NAME = 'example-1-lock'


async def task():
    logger = logging.getLogger('example_1')
    lock_manager = Aioredlock(redis, internal_lock_timeout=3600)

    try:
        # Acquire lock
        logger.info('acquiring lock')
        lock = await lock_manager.lock(LOCK_NAME)
        logger.info('lock acquired')

        assert await lock_manager.is_locked(LOCK_NAME)
        assert lock.valid is True

        # Do stuff
        await asyncio.sleep(1)

        # Release the lock
        await lock_manager.unlock(lock)

        assert not await lock_manager.is_locked(LOCK_NAME)
        assert lock.valid is False
        logger.info('lock released')

    except LockError as e:
        logger.error(e)
        raise

    finally:
        await lock_manager.destroy()


if __name__ == '__main__':
    log_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task())
