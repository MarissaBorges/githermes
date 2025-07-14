:   Type of a dict watcher callback function.

    If *event* is `PyDict_EVENT_CLEARED` or `PyDict_EVENT_DEALLOCATED`, both
    *key* and *new\_value* will be `NULL`. If *event* is `PyDict_EVENT_ADDED`
    or `PyDict_EVENT_MODIFIED`, *new\_value* will be the new value for *key*.
    If *event* is `PyDict_EVENT_DELETED`, *key* is being deleted from the
    dictionary and *new\_value* will be `NULL`.

    `PyDict_EVENT_CLONED` occurs when *dict* was previously empty and another
    dict is merged into it. To maintain efficiency of this operation, per-key
    `PyDict_EVENT_ADDED` events are not issued in this case; instead a
    single `PyDict_EVENT_CLONED` is issued, and *key* will be the source
    dictionary.

    The callback may inspect but must not modify *dict*; doing so could have
    unpredictable effects, including infinite recursion. Do not trigger Python
    code execution in the callback, as it could modify the dict as a side effect.

    If *event* is `PyDict_EVENT_DEALLOCATED`, taking a new reference in the
    callback to the about-to-be-destroyed dictionary will resurrect it and
    prevent it from being freed at this time. When the resurrected object is
    destroyed later, any watcher callbacks active at that time will be called
    again.

    Callbacks occur before the notified modification to *dict* takes place, so
    the prior state of *dict* can be inspected.

    If the callback sets an exception, it must return `-1`; this exception will
    be printed as an unraisable exception using [`PyErr_WriteUnraisable()`](exceptions.html#c.PyErr_WriteUnraisable "PyErr_WriteUnraisable").
    Otherwise it should return `0`.

    There may already be a pending exception set on entry to the callback. In
    this case, the callback should return `0` with the same exception still
    set. This means the callback may not call any other API that can set an
    exception unless it saves and clears the exception state first, and restores
    it before returning.