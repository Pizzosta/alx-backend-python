#!/usr/bin/env python3
'''Task Module'''
import asyncio
from asyncio import Task

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> Task:
    '''
    Creates and returns an asyncio.Task for wait_random(max_delay).

    Args:
        max_delay (int): The maximum delay for wait_random.

    Returns:
        asyncio.Task: A task representing the execution of wait_random(max_delay).
    '''
    task = asyncio.create_task(wait_random(max_delay))
    return task
