Objects for Type Hinting
========================

Various built-in types for type hinting are provided. Currently,
two types exist – [GenericAlias](../library/stdtypes.html#types-genericalias) and
[Union](../library/stdtypes.html#types-union). Only `GenericAlias` is exposed to C.

[PyObject](structures.html#c.PyObject "PyObject") \*Py\_GenericAlias([PyObject](structures.html#c.PyObject "PyObject") \*origin, [PyObject](structures.html#c.PyObject "PyObject") \*args)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.9.*

    Create a [GenericAlias](../library/stdtypes.html#types-genericalias) object.
    Equivalent to calling the Python class
    [`types.GenericAlias`](../library/types.html#types.GenericAlias "types.GenericAlias"). The *origin* and *args* arguments set the
    `GenericAlias`‘s `__origin__` and `__args__` attributes respectively.
    *origin* should be a [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject")\*, and *args* can be a
    [PyTupleObject](tuple.html#c.PyTupleObject "PyTupleObject")\* or any `PyObject*`. If *args* passed is
    not a tuple, a 1-tuple is automatically constructed and `__args__` is set
    to `(args,)`.
    Minimal checking is done for the arguments, so the function will succeed even
    if *origin* is not a type.
    The `GenericAlias`‘s `__parameters__` attribute is constructed lazily
    from `__args__`. On failure, an exception is raised and `NULL` is
    returned.

    Here’s an example of how to make an extension type generic:

    ```
    ...
    static PyMethodDef my_obj_methods[] = {
        // Other methods.
        ...
        {"__class_getitem__", Py_GenericAlias, METH_O|METH_CLASS, "See PEP 585"}
        ...
    }

    ```

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") Py\_GenericAliasType
:   *Part of the [Stable ABI](stable.html#stable) since version 3.9.*

    The C type of the object returned by [`Py_GenericAlias()`](#c.Py_GenericAlias "Py_GenericAlias"). Equivalent to
    [`types.GenericAlias`](../library/types.html#types.GenericAlias "types.GenericAlias") in Python.