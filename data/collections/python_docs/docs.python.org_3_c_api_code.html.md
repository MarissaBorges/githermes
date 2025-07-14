:   Type of a code object watcher callback function.

    If *event* is `PY_CODE_EVENT_CREATE`, then the callback is invoked
    after *co* has been fully initialized. Otherwise, the callback is invoked
    before the destruction of *co* takes place, so the prior state of *co*
    can be inspected.

    If *event* is `PY_CODE_EVENT_DESTROY`, taking a reference in the callback
    to the about-to-be-destroyed code object will resurrect it and prevent it
    from being freed at this time. When the resurrected object is destroyed
    later, any watcher callbacks active at that time will be called again.

    Users of this API should not rely on internal runtime implementation
    details. Such details may include, but are not limited to, the exact
    order and timing of creation and destruction of code objects. While
    changes in these details may result in differences observable by watchers
    (including whether a callback is invoked or not), it does not change
    the semantics of the Python code being executed.

    If the callback sets an exception, it must return `-1`; this exception will
    be printed as an unraisable exception using [`PyErr_WriteUnraisable()`](exceptions.html#c.PyErr_WriteUnraisable "PyErr_WriteUnraisable").
    Otherwise it should return `0`.

    There may already be a pending exception set on entry to the callback. In
    this case, the callback should return `0` with the same exception still
    set. This means the callback may not call any other API that can set an
    exception unless it saves and clears the exception state first, and restores
    it before returning.