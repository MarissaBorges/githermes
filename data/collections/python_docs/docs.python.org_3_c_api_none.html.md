The `None` Object
=================

Note that the [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") for `None` is not directly exposed in the
Python/C API. Since `None` is a singleton, testing for object identity (using
`==` in C) is sufficient. There is no `PyNone_Check()` function for the
same reason.

[PyObject](structures.html#c.PyObject "PyObject") \*Py\_None
:   The Python `None` object, denoting lack of value. This object has no methods
    and is [immortal](../glossary.html#term-immortal).

Py\_RETURN\_NONE
:   Return [`Py_None`](#c.Py_None "Py_None") from a function.