Generator Objects
=================

Generator objects are what Python uses to implement generator iterators. They
are normally created by iterating over a function that yields values, rather
than explicitly calling [`PyGen_New()`](#c.PyGen_New "PyGen_New") or [`PyGen_NewWithQualName()`](#c.PyGen_NewWithQualName "PyGen_NewWithQualName").

type PyGenObject
:   The C structure used for generator objects.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyGen\_Type
:   The type object corresponding to generator objects.

int PyGen\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is a generator object; *ob* must not be `NULL`. This
    function always succeeds.

int PyGen\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob*’s type is [`PyGen_Type`](#c.PyGen_Type "PyGen_Type"); *ob* must not be
    `NULL`. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyGen\_New([PyFrameObject](frame.html#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Create and return a new generator object based on the *frame* object.
    A reference to *frame* is stolen by this function. The argument must not be
    `NULL`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyGen\_NewWithQualName([PyFrameObject](frame.html#c.PyFrameObject "PyFrameObject") \*frame, [PyObject](structures.html#c.PyObject "PyObject") \*name, [PyObject](structures.html#c.PyObject "PyObject") \*qualname)
:   *Return value: New reference.*

    Create and return a new generator object based on the *frame* object,
    with `__name__` and `__qualname__` set to *name* and *qualname*.
    A reference to *frame* is stolen by this function. The *frame* argument
    must not be `NULL`.