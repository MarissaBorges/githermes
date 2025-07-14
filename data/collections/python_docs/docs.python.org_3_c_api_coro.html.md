Coroutine Objects
=================

Coroutine objects are what functions declared with an `async` keyword
return.

type PyCoroObject
:   The C structure used for coroutine objects.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyCoro\_Type
:   The type object corresponding to coroutine objects.

int PyCoro\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob*’s type is [`PyCoro_Type`](#c.PyCoro_Type "PyCoro_Type"); *ob* must not be `NULL`.
    This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyCoro\_New([PyFrameObject](frame.html#c.PyFrameObject "PyFrameObject") \*frame, [PyObject](structures.html#c.PyObject "PyObject") \*name, [PyObject](structures.html#c.PyObject "PyObject") \*qualname)
:   *Return value: New reference.*

    Create and return a new coroutine object based on the *frame* object,
    with `__name__` and `__qualname__` set to *name* and *qualname*.
    A reference to *frame* is stolen by this function. The *frame* argument
    must not be `NULL`.