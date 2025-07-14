Queues
======

**Source code:** [Lib/asyncio/queues.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/queues.py)

---

asyncio queues are designed to be similar to classes of the
[`queue`](queue.html#module-queue "queue: A synchronized queue class.") module. Although asyncio queues are not thread-safe,
they are designed to be used specifically in async/await code.

Note that methods of asyncio queues don’t have a *timeout* parameter;
use [`asyncio.wait_for()`](asyncio-task.html#asyncio.wait_for "asyncio.wait_for") function to do queue operations with a
timeout.

See also the [Examples](#examples) section below.

Queue
-----

*class* asyncio.Queue(*maxsize=0*)
:   A first in, first out (FIFO) queue.

    If *maxsize* is less than or equal to zero, the queue size is
    infinite. If it is an integer greater than `0`, then
    `await put()` blocks when the queue reaches *maxsize*
    until an item is removed by [`get()`](#asyncio.Queue.get "asyncio.Queue.get").

    Unlike the standard library threading [`queue`](queue.html#module-queue "queue: A synchronized queue class."), the size of
    the queue is always known and can be returned by calling the
    [`qsize()`](#asyncio.Queue.qsize "asyncio.Queue.qsize") method.

    Changed in version 3.10: Removed the *loop* parameter.

    This class is [not thread safe](asyncio-dev.html#asyncio-multithreading).

    maxsize
    :   Number of items allowed in the queue.

    empty()
    :   Return `True` if the queue is empty, `False` otherwise.

    full()
    :   Return `True` if there are [`maxsize`](#asyncio.Queue.maxsize "asyncio.Queue.maxsize") items in the queue.

        If the queue was initialized with `maxsize=0` (the default),
        then [`full()`](#asyncio.Queue.full "asyncio.Queue.full") never returns `True`.

    *async* get()
    :   Remove and return an item from the queue. If queue is empty,
        wait until an item is available.

        Raises [`QueueShutDown`](#asyncio.QueueShutDown "asyncio.QueueShutDown") if the queue has been shut down and
        is empty, or if the queue has been shut down immediately.

    get\_nowait()
    :   Return an item if one is immediately available, else raise
        [`QueueEmpty`](#asyncio.QueueEmpty "asyncio.QueueEmpty").

    *async* join()
    :   Block until all items in the queue have been received and processed.

        The count of unfinished tasks goes up whenever an item is added
        to the queue. The count goes down whenever a consumer coroutine calls
        [`task_done()`](#asyncio.Queue.task_done "asyncio.Queue.task_done") to indicate that the item was retrieved and all
        work on it is complete. When the count of unfinished tasks drops
        to zero, [`join()`](#asyncio.Queue.join "asyncio.Queue.join") unblocks.

    *async* put(*item*)
    :   Put an item into the queue. If the queue is full, wait until a
        free slot is available before adding the item.

        Raises [`QueueShutDown`](#asyncio.QueueShutDown "asyncio.QueueShutDown") if the queue has been shut down.

    put\_nowait(*item*)
    :   Put an item into the queue without blocking.

        If no free slot is immediately available, raise [`QueueFull`](#asyncio.QueueFull "asyncio.QueueFull").

    qsize()
    :   Return the number of items in the queue.

    shutdown(*immediate=False*)
    :   Shut down the queue, making [`get()`](#asyncio.Queue.get "asyncio.Queue.get") and [`put()`](#asyncio.Queue.put "asyncio.Queue.put")
        raise [`QueueShutDown`](#asyncio.QueueShutDown "asyncio.QueueShutDown").

        By default, [`get()`](#asyncio.Queue.get "asyncio.Queue.get") on a shut down queue will only
        raise once the queue is empty. Set *immediate* to true to make
        [`get()`](#asyncio.Queue.get "asyncio.Queue.get") raise immediately instead.

        All blocked callers of [`put()`](#asyncio.Queue.put "asyncio.Queue.put") and [`get()`](#asyncio.Queue.get "asyncio.Queue.get")
        will be unblocked. If *immediate* is true, a task will be marked
        as done for each remaining item in the queue, which may unblock
        callers of [`join()`](#asyncio.Queue.join "asyncio.Queue.join").

    task\_done()
    :   Indicate that a formerly enqueued work item is complete.

        Used by queue consumers. For each [`get()`](#asyncio.Queue.get "asyncio.Queue.get") used to
        fetch a work item, a subsequent call to [`task_done()`](#asyncio.Queue.task_done "asyncio.Queue.task_done") tells the
        queue that the processing on the work item is complete.

        If a [`join()`](#asyncio.Queue.join "asyncio.Queue.join") is currently blocking, it will resume when all
        items have been processed (meaning that a [`task_done()`](#asyncio.Queue.task_done "asyncio.Queue.task_done")
        call was received for every item that had been [`put()`](#asyncio.Queue.put "asyncio.Queue.put")
        into the queue).

        `shutdown(immediate=True)` calls [`task_done()`](#asyncio.Queue.task_done "asyncio.Queue.task_done") for each
        remaining item in the queue.

        Raises [`ValueError`](exceptions.html#ValueError "ValueError") if called more times than there were
        items placed in the queue.

Priority Queue
--------------

*class* asyncio.PriorityQueue
:   A variant of [`Queue`](#asyncio.Queue "asyncio.Queue"); retrieves entries in priority order
    (lowest first).

    Entries are typically tuples of the form
    `(priority_number, data)`.

LIFO Queue
----------

*class* asyncio.LifoQueue
:   A variant of [`Queue`](#asyncio.Queue "asyncio.Queue") that retrieves most recently added
    entries first (last in, first out).

Exceptions
----------

*exception* asyncio.QueueEmpty
:   This exception is raised when the [`get_nowait()`](#asyncio.Queue.get_nowait "asyncio.Queue.get_nowait") method
    is called on an empty queue.

*exception* asyncio.QueueFull
:   Exception raised when the [`put_nowait()`](#asyncio.Queue.put_nowait "asyncio.Queue.put_nowait") method is called
    on a queue that has reached its *maxsize*.

*exception* asyncio.QueueShutDown
:   Exception raised when [`put()`](#asyncio.Queue.put "asyncio.Queue.put") or [`get()`](#asyncio.Queue.get "asyncio.Queue.get") is
    called on a queue which has been shut down.

Examples
--------

Queues can be used to distribute workload between several
concurrent tasks:

Copy

```
import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())

```