:   Allocate a new Python object using the C structure type *TYPE* and the
    Python type object *typeobj* (`PyTypeObject*`).
    Fields not defined by the Python object header
    are not initialized. The allocated memory allows for the *TYPE* structure
    plus *size* (`Py_ssize_t`) fields of the size
    given by the [`tp_itemsize`](typeobj.html#c.PyTypeObject.tp_itemsize "PyTypeObject.tp_itemsize") field of
    *typeobj*. This is useful for implementing objects like tuples, which are
    able to determine their size at construction time. Embedding the array of
    fields into the same allocation decreases the number of allocations,
    improving the memory management efficiency.

    Note that this function is unsuitable if *typeobj* has
    [`Py_TPFLAGS_HAVE_GC`](typeobj.html#c.Py_TPFLAGS_HAVE_GC "Py_TPFLAGS_HAVE_GC") set. For such objects,
    use [`PyObject_GC_NewVar()`](gcsupport.html#c.PyObject_GC_NewVar "PyObject_GC_NewVar") instead.