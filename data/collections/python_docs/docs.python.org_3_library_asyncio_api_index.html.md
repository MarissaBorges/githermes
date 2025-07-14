High-level API Index
====================

This page lists all high-level async/await enabled asyncio APIs.

Tasks
-----

Utilities to run asyncio programs, create Tasks, and
await on multiple things with timeouts.

|  |  |
| --- | --- |
| [`run()`](asyncio-runner.html#asyncio.run "asyncio.run") | Create event loop, run a coroutine, close the loop. |
| [`Runner`](asyncio-runner.html#asyncio.Runner "asyncio.Runner") | A context manager that simplifies multiple async function calls. |
| [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") | Task object. |
| [`TaskGroup`](asyncio-task.html#asyncio.TaskGroup "asyncio.TaskGroup") | A context manager that holds a group of tasks. Provides a convenient and reliable way to wait for all tasks in the group to finish. |
| [`create_task()`](asyncio-task.html#asyncio.create_task "asyncio.create_task") | Start an asyncio Task, then returns it. |
| [`current_task()`](asyncio-task.html#asyncio.current_task "asyncio.current_task") | Return the current Task. |
| [`all_tasks()`](asyncio-task.html#asyncio.all_tasks "asyncio.all_tasks") | Return all tasks that are not yet finished for an event loop. |
| `await` [`sleep()`](asyncio-task.html#asyncio.sleep "asyncio.sleep") | Sleep for a number of seconds. |
| `await` [`gather()`](asyncio-task.html#asyncio.gather "asyncio.gather") | Schedule and wait for things concurrently. |
| `await` [`wait_for()`](asyncio-task.html#asyncio.wait_for "asyncio.wait_for") | Run with a timeout. |
| `await` [`shield()`](asyncio-task.html#asyncio.shield "asyncio.shield") | Shield from cancellation. |
| `await` [`wait()`](asyncio-task.html#asyncio.wait "asyncio.wait") | Monitor for completion. |
| [`timeout()`](asyncio-task.html#asyncio.timeout "asyncio.timeout") | Run with a timeout. Useful in cases when `wait_for` is not suitable. |
| [`to_thread()`](asyncio-task.html#asyncio.to_thread "asyncio.to_thread") | Asynchronously run a function in a separate OS thread. |
| [`run_coroutine_threadsafe()`](asyncio-task.html#asyncio.run_coroutine_threadsafe "asyncio.run_coroutine_threadsafe") | Schedule a coroutine from another OS thread. |
| `for in` [`as_completed()`](asyncio-task.html#asyncio.as_completed "asyncio.as_completed") | Monitor for completion with a `for` loop. |

Examples

Queues
------

Queues should be used to distribute work amongst multiple asyncio Tasks,
implement connection pools, and pub/sub patterns.

Examples

Subprocesses
------------

Utilities to spawn subprocesses and run shell commands.

Examples

Streams
-------

High-level APIs to work with network IO.

Examples

Synchronization
---------------

Threading-like synchronization primitives that can be used in Tasks.

Examples