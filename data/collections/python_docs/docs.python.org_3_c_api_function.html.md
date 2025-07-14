:   Type of a function watcher callback function.

    If *event* is `PyFunction_EVENT_CREATE` or `PyFunction_EVENT_DESTROY`
    then *new\_value* will be `NULL`. Otherwise, *new\_value* will hold a
    [borrowed reference](../glossary.html#term-borrowed-reference) to the new value that is about to be stored in
    *func* for the attribute that is being modified.

    The callback may inspect but must not modify *func*; doing so could have
    unpredictable effects, including infinite recursion.

    If *event* is `PyFunction_EVENT_CREATE`, then the callback is invoked
    after *func* has been fully initialized. Otherwise, the callback is invoked
    before the modification to *func* takes place, so the prior state of *func*
    can be inspected. The runtime is permitted to optimize away the creation of
    function objects when possible. In such cases no event will be emitted.
    Although this creates the possibility of an observable difference of
    runtime behavior depending on optimization decisions, it does not change
    the semantics of the Python code being executed.

    If *event* is `PyFunction_EVENT_DESTROY`, Taking a reference in the
    callback to the about-to-be-destroyed function will resurrect it, preventing
    it from being freed at this time. When the resurrected object is destroyed
    later, any watcher callbacks active at that time will be called again.

    If the callback sets an exception, it must return `-1`; this exception will
    be printed as an unraisable exception using [`PyErr_WriteUnraisable()`](exceptions.html#c.PyErr_WriteUnraisable "PyErr_WriteUnraisable").
    Otherwise it should return `0`.

    There may already be a pending exception set on entry to the callback. In
    this case, the callback should return `0` with the same exception still
    set. This means the callback may not call any other API that can set an
    exception unless it saves and clears the exception state first, and restores
    it before returning.