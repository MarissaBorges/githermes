Instance Method Objects
=======================

An instance method is a wrapper for a [`PyCFunction`](structures.html#c.PyCFunction "PyCFunction") and the new way
to bind a [`PyCFunction`](structures.html#c.PyCFunction "PyCFunction") to a class object. It replaces the former call
`PyMethod_New(func, NULL, class)`.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyInstanceMethod\_Type
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python instance
    method type. It is not exposed to Python programs.

int PyInstanceMethod\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is an instance method object (has type
    [`PyInstanceMethod_Type`](#c.PyInstanceMethod_Type "PyInstanceMethod_Type")). The parameter must not be `NULL`.
    This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyInstanceMethod\_New([PyObject](structures.html#c.PyObject "PyObject") \*func)
:   *Return value: New reference.*

    Return a new instance method object, with *func* being any callable object.
    *func* is the function that will be called when the instance method is
    called.

[PyObject](structures.html#c.PyObject "PyObject") \*PyInstanceMethod\_Function([PyObject](structures.html#c.PyObject "PyObject") \*im)
:   *Return value: Borrowed reference.*

    Return the function object associated with the instance method *im*.

[PyObject](structures.html#c.PyObject "PyObject") \*PyInstanceMethod\_GET\_FUNCTION([PyObject](structures.html#c.PyObject "PyObject") \*im)
:   *Return value: Borrowed reference.*

    Macro version of [`PyInstanceMethod_Function()`](#c.PyInstanceMethod_Function "PyInstanceMethod_Function") which avoids error checking.

Method Objects
==============

Methods are bound function objects. Methods are always bound to an instance of
a user-defined class. Unbound methods (methods bound to a class object) are
no longer available.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyMethod\_Type
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python method type. This
    is exposed to Python programs as `types.MethodType`.

int PyMethod\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is a method object (has type [`PyMethod_Type`](#c.PyMethod_Type "PyMethod_Type")). The
    parameter must not be `NULL`. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMethod\_New([PyObject](structures.html#c.PyObject "PyObject") \*func, [PyObject](structures.html#c.PyObject "PyObject") \*self)
:   *Return value: New reference.*

    Return a new method object, with *func* being any callable object and *self*
    the instance the method should be bound. *func* is the function that will
    be called when the method is called. *self* must not be `NULL`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMethod\_Function([PyObject](structures.html#c.PyObject "PyObject") \*meth)
:   *Return value: Borrowed reference.*

    Return the function object associated with the method *meth*.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMethod\_GET\_FUNCTION([PyObject](structures.html#c.PyObject "PyObject") \*meth)
:   *Return value: Borrowed reference.*

    Macro version of [`PyMethod_Function()`](#c.PyMethod_Function "PyMethod_Function") which avoids error checking.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMethod\_Self([PyObject](structures.html#c.PyObject "PyObject") \*meth)
:   *Return value: Borrowed reference.*

    Return the instance associated with the method *meth*.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMethod\_GET\_SELF([PyObject](structures.html#c.PyObject "PyObject") \*meth)
:   *Return value: Borrowed reference.*

    Macro version of [`PyMethod_Self()`](#c.PyMethod_Self "PyMethod_Self") which avoids error checking.