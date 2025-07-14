Boolean Objects
===============

Booleans in Python are implemented as a subclass of integers. There are only
two booleans, [`Py_False`](#c.Py_False "Py_False") and [`Py_True`](#c.Py_True "Py_True"). As such, the normal
creation and deletion functions don’t apply to booleans. The following macros
are available, however.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyBool\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python boolean type; it
    is the same object as [`bool`](../library/functions.html#bool "bool") in the Python layer.

int PyBool\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is of type [`PyBool_Type`](#c.PyBool_Type "PyBool_Type"). This function always
    succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*Py\_False
:   The Python `False` object. This object has no methods and is
    [immortal](../glossary.html#term-immortal).

[PyObject](structures.html#c.PyObject "PyObject") \*Py\_True
:   The Python `True` object. This object has no methods and is
    [immortal](../glossary.html#term-immortal).

Py\_RETURN\_FALSE
:   Return [`Py_False`](#c.Py_False "Py_False") from a function.

Py\_RETURN\_TRUE
:   Return [`Py_True`](#c.Py_True "Py_True") from a function.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBool\_FromLong(long v)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return [`Py_True`](#c.Py_True "Py_True") or [`Py_False`](#c.Py_False "Py_False"), depending on the truth value of *v*.