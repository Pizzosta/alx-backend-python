#!/usr/bin/env python3
'''Measure Runtime'''

import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: int) -> float:
    '''
    Measures the average execution time of calling wait_n asynchronously.

    Args:
        n (int): The number of times to call wait_n.
        max_delay (int): The maximum delay for each wait_n call.

    Returns:
        float: The average time taken for wait_n calls.
    '''
    start_time = time.time()
    await asyncio.run(wait_n(n, max_delay))
    end_time = time.time()
    total_time = end_time - start_time

    return total_time / n
