#!/usr/bin/env python3
'''Measure Runtime Module'''

from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''
    Creates and returns a list of asyncio.Tasks for task_wait_random(max_delay).

    Args:
        n (int): The number of tasks to create.
        max_delay (int): The maximum delay for task_wait_random.

    Returns:
        List[float]: A list of float values representing the delays from task_wait_random.
    '''
    tasks = []
    for _ in range(n):
        task = task_wait_random(max_delay)
        tasks.append(task)

    delays = []
    for task in tasks:
        delay = await task
        delays.append(delay)

    return sorted(delays)
