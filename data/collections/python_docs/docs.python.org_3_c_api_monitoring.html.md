Monitoring C API
================

Added in version 3.13.

An extension may need to interact with the event monitoring system. Subscribing
to events and registering callbacks can be done via the Python API exposed in
[`sys.monitoring`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring").

Generating Execution Events
===========================

The functions below make it possible for an extension to fire monitoring
events as it emulates the execution of Python code. Each of these functions
accepts a `PyMonitoringState` struct which contains concise information
about the activation state of events, as well as the event arguments, which
include a `PyObject*` representing the code object, the instruction offset
and sometimes additional, event-specific arguments (see [`sys.monitoring`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring")
for details about the signatures of the different event callbacks).
The `codelike` argument should be an instance of [`types.CodeType`](../library/types.html#types.CodeType "types.CodeType")
or of a type that emulates it.

The VM disables tracing when firing an event, so there is no need for user
code to do that.

Monitoring functions should not be called with an exception set,
except those listed below as working with the current exception.

type PyMonitoringState
:   Representation of the state of an event type. It is allocated by the user
    while its contents are maintained by the monitoring API functions described below.

All of the functions below return 0 on success and -1 (with an exception set) on error.

See [`sys.monitoring`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring") for descriptions of the events.

int PyMonitoring\_FirePyStartEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `PY_START` event.

int PyMonitoring\_FirePyResumeEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `PY_RESUME` event.

int PyMonitoring\_FirePyReturnEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*retval)
:   Fire a `PY_RETURN` event.

int PyMonitoring\_FirePyYieldEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*retval)
:   Fire a `PY_YIELD` event.

int PyMonitoring\_FireCallEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*callable, [PyObject](structures.html#c.PyObject "PyObject") \*arg0)
:   Fire a `CALL` event.

int PyMonitoring\_FireLineEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, int lineno)
:   Fire a `LINE` event.

int PyMonitoring\_FireJumpEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*target\_offset)
:   Fire a `JUMP` event.

int PyMonitoring\_FireBranchEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*target\_offset)
:   Fire a `BRANCH` event.

int PyMonitoring\_FireCReturnEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*retval)
:   Fire a `C_RETURN` event.

int PyMonitoring\_FirePyThrowEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `PY_THROW` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FireRaiseEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `RAISE` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FireCRaiseEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `C_RAISE` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FireReraiseEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `RERAISE` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FireExceptionHandledEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire an `EXCEPTION_HANDLED` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FirePyUnwindEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset)
:   Fire a `PY_UNWIND` event with the current exception (as returned by
    [`PyErr_GetRaisedException()`](exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException")).

int PyMonitoring\_FireStopIterationEvent([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state, [PyObject](structures.html#c.PyObject "PyObject") \*codelike, int32\_t offset, [PyObject](structures.html#c.PyObject "PyObject") \*value)
:   Fire a `STOP_ITERATION` event. If `value` is an instance of [`StopIteration`](../library/exceptions.html#StopIteration "StopIteration"), it is used. Otherwise,
    a new [`StopIteration`](../library/exceptions.html#StopIteration "StopIteration") instance is created with `value` as its argument.

Managing the Monitoring State
-----------------------------

Monitoring states can be managed with the help of monitoring scopes. A scope
would typically correspond to a python function.

int PyMonitoring\_EnterScope([PyMonitoringState](#c.PyMonitoringState "PyMonitoringState") \*state\_array, uint64\_t \*version, const uint8\_t \*event\_types, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") length)
:   Enter a monitored scope. `event_types` is an array of the event IDs for
    events that may be fired from the scope. For example, the ID of a `PY_START`
    event is the value `PY_MONITORING_EVENT_PY_START`, which is numerically equal
    to the base-2 logarithm of `sys.monitoring.events.PY_START`.
    `state_array` is an array with a monitoring state entry for each event in
    `event_types`, it is allocated by the user but populated by
    `PyMonitoring_EnterScope()` with information about the activation state of
    the event. The size of `event_types` (and hence also of `state_array`)
    is given in `length`.

    The `version` argument is a pointer to a value which should be allocated
    by the user together with `state_array` and initialized to 0,
    and then set only by `PyMonitoring_EnterScope()` itself. It allows this
    function to determine whether event states have changed since the previous call,
    and to return quickly if they have not.

    The scopes referred to here are lexical scopes: a function, class or method.
    `PyMonitoring_EnterScope()` should be called whenever the lexical scope is
    entered. Scopes can be reentered, reusing the same *state\_array* and *version*,
    in situations like when emulating a recursive Python function. When a code-like’s
    execution is paused, such as when emulating a generator, the scope needs to
    be exited and re-entered.

    The macros for *event\_types* are:

int PyMonitoring\_ExitScope(void)
:   Exit the last scope that was entered with `PyMonitoring_EnterScope()`.

int PY\_MONITORING\_IS\_INSTRUMENTED\_EVENT(uint8\_t ev)
:   Return true if the event corresponding to the event ID *ev* is
    a [local event](../library/sys.monitoring.html#monitoring-event-local).