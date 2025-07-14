`sys.monitoring` — Execution event monitoring
=============================================

---

Note

[`sys.monitoring`](#module-sys.monitoring "sys.monitoring: Access and control event monitoring") is a namespace within the [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.") module,
not an independent module, so there is no need to
`import sys.monitoring`, simply `import sys` and then use
`sys.monitoring`.

This namespace provides access to the functions and constants necessary to
activate and control event monitoring.

As programs execute, events occur that might be of interest to tools that
monitor execution. The [`sys.monitoring`](#module-sys.monitoring "sys.monitoring: Access and control event monitoring") namespace provides means to
receive callbacks when events of interest occur.

The monitoring API consists of three components:

Events
------

The following events are supported:

sys.monitoring.events.BRANCH
:   A conditional branch is taken (or not).

sys.monitoring.events.CALL
:   A call in Python code (event occurs before the call).

sys.monitoring.events.C\_RAISE
:   An exception raised from any callable, except for Python functions (event occurs after the exit).

sys.monitoring.events.C\_RETURN
:   Return from any callable, except for Python functions (event occurs after the return).

sys.monitoring.events.EXCEPTION\_HANDLED
:   An exception is handled.

sys.monitoring.events.INSTRUCTION
:   A VM instruction is about to be executed.

sys.monitoring.events.JUMP
:   An unconditional jump in the control flow graph is made.

sys.monitoring.events.LINE
:   An instruction is about to be executed that has a different line number from the preceding instruction.

sys.monitoring.events.PY\_RESUME
:   Resumption of a Python function (for generator and coroutine functions), except for `throw()` calls.

sys.monitoring.events.PY\_RETURN
:   Return from a Python function (occurs immediately before the return, the callee’s frame will be on the stack).

sys.monitoring.events.PY\_START
:   Start of a Python function (occurs immediately after the call, the callee’s frame will be on the stack)

sys.monitoring.events.PY\_THROW
:   A Python function is resumed by a `throw()` call.

sys.monitoring.events.PY\_UNWIND
:   Exit from a Python function during exception unwinding.

sys.monitoring.events.PY\_YIELD
:   Yield from a Python function (occurs immediately before the yield, the callee’s frame will be on the stack).

sys.monitoring.events.RAISE
:   An exception is raised, except those that cause a [`STOP_ITERATION`](#monitoring-event-STOP_ITERATION) event.

sys.monitoring.events.RERAISE
:   An exception is re-raised, for example at the end of a [`finally`](../reference/compound_stmts.html#finally) block.

sys.monitoring.events.STOP\_ITERATION
:   An artificial [`StopIteration`](exceptions.html#StopIteration "StopIteration") is raised; see [the STOP\_ITERATION event](#the-stop-iteration-event).

More events may be added in the future.

These events are attributes of the `sys.monitoring.events` namespace.
Each event is represented as a power-of-2 integer constant.
To define a set of events, simply bitwise OR the individual events together.
For example, to specify both [`PY_RETURN`](#monitoring-event-PY_RETURN) and [`PY_START`](#monitoring-event-PY_START)
events, use the expression `PY_RETURN | PY_START`.

sys.monitoring.events.NO\_EVENTS
:   An alias for `0` so users can do explicit comparisons like:

    Copy

    ```
    if get_events(DEBUGGER_ID) == NO_EVENTS:
        ...

    ```

Events are divided into three groups:

### Local events

Local events are associated with normal execution of the program and happen
at clearly defined locations. All local events can be disabled.
The local events are:

### Ancillary events

Ancillary events can be monitored like other events, but are controlled
by another event:

The [`C_RETURN`](#monitoring-event-C_RETURN) and [`C_RAISE`](#monitoring-event-C_RAISE) events
are controlled by the [`CALL`](#monitoring-event-CALL) event.
[`C_RETURN`](#monitoring-event-C_RETURN) and [`C_RAISE`](#monitoring-event-C_RAISE) events will only be seen if the
corresponding [`CALL`](#monitoring-event-CALL) event is being monitored.

### Other events

Other events are not necessarily tied to a specific location in the
program and cannot be individually disabled.

The other events that can be monitored are:

### The STOP\_ITERATION event

[**PEP 380**](https://peps.python.org/pep-0380/#use-of-stopiteration-to-return-values)
specifies that a [`StopIteration`](exceptions.html#StopIteration "StopIteration") exception is raised when returning a value
from a generator or coroutine. However, this is a very inefficient way to
return a value, so some Python implementations, notably CPython 3.12+, do not
raise an exception unless it would be visible to other code.

To allow tools to monitor for real exceptions without slowing down generators
and coroutines, the [`STOP_ITERATION`](#monitoring-event-STOP_ITERATION) event is provided.
[`STOP_ITERATION`](#monitoring-event-STOP_ITERATION) can be locally disabled, unlike [`RAISE`](#monitoring-event-RAISE).

Turning events on and off
-------------------------

In order to monitor an event, it must be turned on and a corresponding callback
must be registered.
Events can be turned on or off by setting the events either globally or
for a particular code object.

### Setting events globally

Events can be controlled globally by modifying the set of events being monitored.

sys.monitoring.get\_events(*tool\_id: [int](functions.html#int "int")*, */*) → [int](functions.html#int "int")
:   Returns the `int` representing all the active events.

sys.monitoring.set\_events(*tool\_id: [int](functions.html#int "int")*, *event\_set: [int](functions.html#int "int")*, */*) → [None](constants.html#None "None")
:   Activates all events which are set in *event\_set*.
    Raises a [`ValueError`](exceptions.html#ValueError "ValueError") if *tool\_id* is not in use.

No events are active by default.

### Per code object events

Events can also be controlled on a per code object basis. The functions
defined below which accept a [`types.CodeType`](types.html#types.CodeType "types.CodeType") should be prepared
to accept a look-alike object from functions which are not defined
in Python (see [Monitoring C API](../c-api/monitoring.html#c-api-monitoring)).

sys.monitoring.get\_local\_events(*tool\_id: [int](functions.html#int "int")*, *code: [CodeType](types.html#types.CodeType "types.CodeType")*, */*) → [int](functions.html#int "int")
:   Returns all the local events for *code*

sys.monitoring.set\_local\_events(*tool\_id: [int](functions.html#int "int")*, *code: [CodeType](types.html#types.CodeType "types.CodeType")*, *event\_set: [int](functions.html#int "int")*, */*) → [None](constants.html#None "None")
:   Activates all the local events for *code* which are set in *event\_set*.
    Raises a [`ValueError`](exceptions.html#ValueError "ValueError") if *tool\_id* is not in use.

Local events add to global events, but do not mask them.
In other words, all global events will trigger for a code object,
regardless of the local events.

### Disabling events

sys.monitoring.DISABLE
:   A special value that can be returned from a callback function to disable
    events for the current code location.

Local events can be disabled for a specific code location by returning
[`sys.monitoring.DISABLE`](#sys.monitoring.DISABLE "sys.monitoring.DISABLE") from a callback function. This does not change
which events are set, or any other code locations for the same event.

Disabling events for specific locations is very important for high
performance monitoring. For example, a program can be run under a
debugger with no overhead if the debugger disables all monitoring
except for a few breakpoints.

sys.monitoring.restart\_events() → [None](constants.html#None "None")
:   Enable all the events that were disabled by [`sys.monitoring.DISABLE`](#sys.monitoring.DISABLE "sys.monitoring.DISABLE")
    for all tools.

Registering callback functions
------------------------------

To register a callable for events call

sys.monitoring.register\_callback(*tool\_id: [int](functions.html#int "int")*, *event: [int](functions.html#int "int")*, *func: [Callable](collections.abc.html#collections.abc.Callable "collections.abc.Callable") | [None](constants.html#None "None")*, */*) → [Callable](collections.abc.html#collections.abc.Callable "collections.abc.Callable") | [None](constants.html#None "None")
:   Registers the callable *func* for the *event* with the given *tool\_id*

    If another callback was registered for the given *tool\_id* and *event*,
    it is unregistered and returned.
    Otherwise [`register_callback()`](#sys.monitoring.register_callback "sys.monitoring.register_callback") returns `None`.

Functions can be unregistered by calling
`sys.monitoring.register_callback(tool_id, event, None)`.

Callback functions can be registered and unregistered at any time.

Registering or unregistering a callback function will generate a [`sys.audit()`](sys.html#sys.audit "sys.audit") event.

### Callback function arguments

sys.monitoring.MISSING
:   A special value that is passed to a callback function to indicate
    that there are no arguments to the call.

When an active event occurs, the registered callback function is called.
Different events will provide the callback function with different arguments, as follows:

* [`PY_START`](#monitoring-event-PY_START) and [`PY_RESUME`](#monitoring-event-PY_RESUME):

  Copy

  ```
  func(code: CodeType, instruction_offset: int) -> DISABLE | Any

  ```
* [`PY_RETURN`](#monitoring-event-PY_RETURN) and [`PY_YIELD`](#monitoring-event-PY_YIELD):

  Copy

  ```
  func(code: CodeType, instruction_offset: int, retval: object) -> DISABLE | Any

  ```
* [`CALL`](#monitoring-event-CALL), [`C_RAISE`](#monitoring-event-C_RAISE) and [`C_RETURN`](#monitoring-event-C_RETURN):

  Copy

  ```
  func(code: CodeType, instruction_offset: int, callable: object, arg0: object | MISSING) -> DISABLE | Any

  ```

  If there are no arguments, *arg0* is set to [`sys.monitoring.MISSING`](#sys.monitoring.MISSING "sys.monitoring.MISSING").
* [`RAISE`](#monitoring-event-RAISE), [`RERAISE`](#monitoring-event-RERAISE), [`EXCEPTION_HANDLED`](#monitoring-event-EXCEPTION_HANDLED),
  [`PY_UNWIND`](#monitoring-event-PY_UNWIND), [`PY_THROW`](#monitoring-event-PY_THROW) and [`STOP_ITERATION`](#monitoring-event-STOP_ITERATION):

  Copy

  ```
  func(code: CodeType, instruction_offset: int, exception: BaseException) -> DISABLE | Any

  ```
* [`LINE`](#monitoring-event-LINE):

  Copy

  ```
  func(code: CodeType, line_number: int) -> DISABLE | Any

  ```
* [`BRANCH`](#monitoring-event-BRANCH) and [`JUMP`](#monitoring-event-JUMP):

  Copy

  ```
  func(code: CodeType, instruction_offset: int, destination_offset: int) -> DISABLE | Any

  ```

  Note that the *destination\_offset* is where the code will next execute.
  For an untaken branch this will be the offset of the instruction following
  the branch.
* [`INSTRUCTION`](#monitoring-event-INSTRUCTION):

  Copy

  ```
  func(code: CodeType, instruction_offset: int) -> DISABLE | Any

  ```