Policies
========

An event loop policy is a global object
used to get and set the current [event loop](asyncio-eventloop.html#asyncio-event-loop),
as well as create new event loops.
The default policy can be [replaced](#asyncio-policy-get-set) with
[built-in alternatives](#asyncio-policy-builtin)
to use different event loop implementations,
or substituted by a [custom policy](#asyncio-custom-policies)
that can override these behaviors.

The [policy object](#asyncio-policy-objects)
gets and sets a separate event loop per *context*.
This is per-thread by default,
though custom policies could define *context* differently.

Custom event loop policies can control the behavior of
[`get_event_loop()`](asyncio-eventloop.html#asyncio.get_event_loop "asyncio.get_event_loop"), [`set_event_loop()`](asyncio-eventloop.html#asyncio.set_event_loop "asyncio.set_event_loop"), and [`new_event_loop()`](asyncio-eventloop.html#asyncio.new_event_loop "asyncio.new_event_loop").

Policy objects should implement the APIs defined
in the [`AbstractEventLoopPolicy`](#asyncio.AbstractEventLoopPolicy "asyncio.AbstractEventLoopPolicy") abstract base class.

Getting and Setting the Policy
------------------------------

The following functions can be used to get and set the policy
for the current process:

asyncio.get\_event\_loop\_policy()
:   Return the current process-wide policy.

asyncio.set\_event\_loop\_policy(*policy*)
:   Set the current process-wide policy to *policy*.

    If *policy* is set to `None`, the default policy is restored.

Policy Objects
--------------

The abstract event loop policy base class is defined as follows:

*class* asyncio.AbstractEventLoopPolicy
:   An abstract base class for asyncio policies.

    get\_event\_loop()
    :   Get the event loop for the current context.

        Return an event loop object implementing the
        [`AbstractEventLoop`](asyncio-eventloop.html#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") interface.

        This method should never return `None`.

    set\_event\_loop(*loop*)
    :   Set the event loop for the current context to *loop*.

    new\_event\_loop()
    :   Create and return a new event loop object.

        This method should never return `None`.

    get\_child\_watcher()
    :   Get a child process watcher object.

        Return a watcher object implementing the
        [`AbstractChildWatcher`](#asyncio.AbstractChildWatcher "asyncio.AbstractChildWatcher") interface.

        This function is Unix specific.

        Deprecated since version 3.12.

    set\_child\_watcher(*watcher*)
    :   Set the current child process watcher to *watcher*.

        This function is Unix specific.

        Deprecated since version 3.12.

asyncio ships with the following built-in policies:

*class* asyncio.DefaultEventLoopPolicy
:   The default asyncio policy. Uses [`SelectorEventLoop`](asyncio-eventloop.html#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop")
    on Unix and [`ProactorEventLoop`](asyncio-eventloop.html#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") on Windows.

    There is no need to install the default policy manually. asyncio
    is configured to use the default policy automatically.

    Deprecated since version 3.12: The [`get_event_loop()`](asyncio-eventloop.html#asyncio.get_event_loop "asyncio.get_event_loop") method of the default asyncio policy now emits
    a [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning") if there is no current event loop set and it
    decides to create one.
    In some future Python release this will become an error.

*class* asyncio.WindowsSelectorEventLoopPolicy
:   An alternative event loop policy that uses the
    [`SelectorEventLoop`](asyncio-eventloop.html#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") event loop implementation.

*class* asyncio.WindowsProactorEventLoopPolicy
:   An alternative event loop policy that uses the
    [`ProactorEventLoop`](asyncio-eventloop.html#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") event loop implementation.

Process Watchers
----------------

A process watcher allows customization of how an event loop monitors
child processes on Unix. Specifically, the event loop needs to know
when a child process has exited.

In asyncio, child processes are created with
[`create_subprocess_exec()`](asyncio-subprocess.html#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") and [`loop.subprocess_exec()`](asyncio-eventloop.html#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec")
functions.

asyncio defines the [`AbstractChildWatcher`](#asyncio.AbstractChildWatcher "asyncio.AbstractChildWatcher") abstract base class, which child
watchers should implement, and has four different implementations:
[`ThreadedChildWatcher`](#asyncio.ThreadedChildWatcher "asyncio.ThreadedChildWatcher") (configured to be used by default),
[`MultiLoopChildWatcher`](#asyncio.MultiLoopChildWatcher "asyncio.MultiLoopChildWatcher"), [`SafeChildWatcher`](#asyncio.SafeChildWatcher "asyncio.SafeChildWatcher"), and
[`FastChildWatcher`](#asyncio.FastChildWatcher "asyncio.FastChildWatcher").

See also the [Subprocess and Threads](asyncio-subprocess.html#asyncio-subprocess-threads)
section.

The following two functions can be used to customize the child process watcher
implementation used by the asyncio event loop:

asyncio.get\_child\_watcher()
:   Return the current child watcher for the current policy.

    Deprecated since version 3.12.

asyncio.set\_child\_watcher(*watcher*)
:   Set the current child watcher to *watcher* for the current
    policy. *watcher* must implement methods defined in the
    [`AbstractChildWatcher`](#asyncio.AbstractChildWatcher "asyncio.AbstractChildWatcher") base class.

    Deprecated since version 3.12.

Note

Third-party event loops implementations might not support
custom child watchers. For such event loops, using
[`set_child_watcher()`](#asyncio.set_child_watcher "asyncio.set_child_watcher") might be prohibited or have no effect.

*class* asyncio.AbstractChildWatcher
:   add\_child\_handler(*pid*, *callback*, *\*args*)
    :   Register a new child handler.

        Arrange for `callback(pid, returncode, *args)` to be called
        when a process with PID equal to *pid* terminates. Specifying
        another callback for the same process replaces the previous
        handler.

        The *callback* callable must be thread-safe.

    remove\_child\_handler(*pid*)
    :   Removes the handler for process with PID equal to *pid*.

        The function returns `True` if the handler was successfully
        removed, `False` if there was nothing to remove.

    attach\_loop(*loop*)
    :   Attach the watcher to an event loop.

        If the watcher was previously attached to an event loop, then
        it is first detached before attaching to the new loop.

        Note: loop may be `None`.

    is\_active()
    :   Return `True` if the watcher is ready to use.

        Spawning a subprocess with *inactive* current child watcher raises
        [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

    close()
    :   Close the watcher.

        This method has to be called to ensure that underlying
        resources are cleaned-up.

    Deprecated since version 3.12.

*class* asyncio.ThreadedChildWatcher
:   This implementation starts a new waiting thread for every subprocess spawn.

    It works reliably even when the asyncio event loop is run in a non-main OS thread.

    There is no noticeable overhead when handling a big number of children (*O*(1) each
    time a child terminates), but starting a thread per process requires extra memory.

    This watcher is used by default.

*class* asyncio.MultiLoopChildWatcher
:   This implementation registers a `SIGCHLD` signal handler on
    instantiation. That can break third-party code that installs a custom handler for
    `SIGCHLD` signal.

    The watcher avoids disrupting other code spawning processes
    by polling every process explicitly on a `SIGCHLD` signal.

    There is no limitation for running subprocesses from different threads once the
    watcher is installed.

    The solution is safe but it has a significant overhead when
    handling a big number of processes (*O*(*n*) each time a
    `SIGCHLD` is received).

    Deprecated since version 3.12.

*class* asyncio.SafeChildWatcher
:   This implementation uses active event loop from the main thread to handle
    `SIGCHLD` signal. If the main thread has no running event loop another
    thread cannot spawn a subprocess ([`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised).

    The watcher avoids disrupting other code spawning processes
    by polling every process explicitly on a `SIGCHLD` signal.

    This solution is as safe as [`MultiLoopChildWatcher`](#asyncio.MultiLoopChildWatcher "asyncio.MultiLoopChildWatcher") and has the same *O*(*n*)
    complexity but requires a running event loop in the main thread to work.

    Deprecated since version 3.12.

*class* asyncio.FastChildWatcher
:   This implementation reaps every terminated processes by calling
    `os.waitpid(-1)` directly, possibly breaking other code spawning
    processes and waiting for their termination.

    There is no noticeable overhead when handling a big number of
    children (*O*(1) each time a child terminates).

    This solution requires a running event loop in the main thread to work, as
    [`SafeChildWatcher`](#asyncio.SafeChildWatcher "asyncio.SafeChildWatcher").

    Deprecated since version 3.12.

*class* asyncio.PidfdChildWatcher
:   This implementation polls process file descriptors (pidfds) to await child
    process termination. In some respects, [`PidfdChildWatcher`](#asyncio.PidfdChildWatcher "asyncio.PidfdChildWatcher") is a
    “Goldilocks” child watcher implementation. It doesn’t require signals or
    threads, doesn’t interfere with any processes launched outside the event
    loop, and scales linearly with the number of subprocesses launched by the
    event loop. The main disadvantage is that pidfds are specific to Linux, and
    only work on recent (5.3+) kernels.

Custom Policies
---------------

To implement a new event loop policy, it is recommended to subclass
[`DefaultEventLoopPolicy`](#asyncio.DefaultEventLoopPolicy "asyncio.DefaultEventLoopPolicy") and override the methods for which
custom behavior is wanted, e.g.:

Copy

```
class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

    def get_event_loop(self):
        """Get the event loop.

        This may be None or an instance of EventLoop.
        """
        loop = super().get_event_loop()
        # Do something with loop ...
        return loop

asyncio.set_event_loop_policy(MyEventLoopPolicy())

```