:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a mapping providing access to the local variables in the current execution frame,
    or `NULL` if no frame is currently executing.

    Refer to [`locals()`](../library/functions.html#locals "locals") for details of the mapping returned at different scopes.

    As this function returns a [borrowed reference](../glossary.html#term-borrowed-reference), the dictionary returned for
    [optimized scopes](../glossary.html#term-optimized-scope) is cached on the frame object and will remain
    alive as long as the frame object does. Unlike [`PyEval_GetFrameLocals()`](#c.PyEval_GetFrameLocals "PyEval_GetFrameLocals") and
    [`locals()`](../library/functions.html#locals "locals"), subsequent calls to this function in the same frame will update the
    contents of the cached dictionary to reflect changes in the state of the local variables
    rather than returning a new snapshot.