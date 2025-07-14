The *tp\_call* Protocol
-----------------------

Instances of classes that set [`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") are callable.
The signature of the slot is:

```
PyObject *tp_call(PyObject *callable, PyObject *args, PyObject *kwargs);

```

A call is made using a tuple for the positional arguments
and a dict for the keyword arguments, similarly to
`callable(*args, **kwargs)` in Python code.
*args* must be non-NULL (use an empty tuple if there are no arguments)
but *kwargs* may be *NULL* if there are no keyword arguments.

This convention is not only used by *tp\_call*:
[`tp_new`](typeobj.html#c.PyTypeObject.tp_new "PyTypeObject.tp_new") and [`tp_init`](typeobj.html#c.PyTypeObject.tp_init "PyTypeObject.tp_init")
also pass arguments this way.

To call an object, use [`PyObject_Call()`](#c.PyObject_Call "PyObject_Call") or another
[call API](#capi-call).

The Vectorcall Protocol
-----------------------

The vectorcall protocol was introduced in [**PEP 590**](https://peps.python.org/pep-0590/) as an additional protocol
for making calls more efficient.

As rule of thumb, CPython will prefer the vectorcall for internal calls
if the callable supports it. However, this is not a hard rule.
Additionally, some third-party extensions use *tp\_call* directly
(rather than using [`PyObject_Call()`](#c.PyObject_Call "PyObject_Call")).
Therefore, a class supporting vectorcall must also implement
[`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call").
Moreover, the callable must behave the same
regardless of which protocol is used.
The recommended way to achieve this is by setting
[`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") to [`PyVectorcall_Call()`](#c.PyVectorcall_Call "PyVectorcall_Call").
This bears repeating:

Warning

A class supporting vectorcall **must** also implement
[`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") with the same semantics.

Changed in version 3.12: The [`Py_TPFLAGS_HAVE_VECTORCALL`](typeobj.html#c.Py_TPFLAGS_HAVE_VECTORCALL "Py_TPFLAGS_HAVE_VECTORCALL") flag is now removed from a class
when the class’s [`__call__()`](../reference/datamodel.html#object.__call__ "object.__call__") method is reassigned.
(This internally sets [`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") only, and thus
may make it behave differently than the vectorcall function.)
In earlier Python versions, vectorcall should only be used with
[`immutable`](typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE "Py_TPFLAGS_IMMUTABLETYPE") or static types.

A class should not implement vectorcall if that would be slower
than *tp\_call*. For example, if the callee needs to convert
the arguments to an args tuple and kwargs dict anyway, then there is no point
in implementing vectorcall.

Classes can implement the vectorcall protocol by enabling the
[`Py_TPFLAGS_HAVE_VECTORCALL`](typeobj.html#c.Py_TPFLAGS_HAVE_VECTORCALL "Py_TPFLAGS_HAVE_VECTORCALL") flag and setting
[`tp_vectorcall_offset`](typeobj.html#c.PyTypeObject.tp_vectorcall_offset "PyTypeObject.tp_vectorcall_offset") to the offset inside the
object structure where a *vectorcallfunc* appears.
This is a pointer to a function with the following signature:

typedef [PyObject](structures.html#c.PyObject "PyObject") \*(\*vectorcallfunc)([PyObject](structures.html#c.PyObject "PyObject") \*callable, [PyObject](structures.html#c.PyObject "PyObject") \*const \*args, size\_t nargsf, [PyObject](structures.html#c.PyObject "PyObject") \*kwnames)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.12.*

PY\_VECTORCALL\_ARGUMENTS\_OFFSET
:   *Part of the [Stable ABI](stable.html#stable) since version 3.12.*

    If this flag is set in a vectorcall *nargsf* argument, the callee is allowed
    to temporarily change `args[-1]`. In other words, *args* points to
    argument 1 (not 0) in the allocated vector.
    The callee must restore the value of `args[-1]` before returning.

    For [`PyObject_VectorcallMethod()`](#c.PyObject_VectorcallMethod "PyObject_VectorcallMethod"), this flag means instead that
    `args[0]` may be changed.

    Whenever they can do so cheaply (without additional allocation), callers
    are encouraged to use [`PY_VECTORCALL_ARGUMENTS_OFFSET`](#c.PY_VECTORCALL_ARGUMENTS_OFFSET "PY_VECTORCALL_ARGUMENTS_OFFSET").
    Doing so will allow callables such as bound methods to make their onward
    calls (which include a prepended *self* argument) very efficiently.

To call an object that implements vectorcall, use a [call API](#capi-call)
function as with any other callable.
[`PyObject_Vectorcall()`](#c.PyObject_Vectorcall "PyObject_Vectorcall") will usually be most efficient.

### Recursion Control

When using *tp\_call*, callees do not need to worry about
[recursion](exceptions.html#recursion): CPython uses
[`Py_EnterRecursiveCall()`](exceptions.html#c.Py_EnterRecursiveCall "Py_EnterRecursiveCall") and [`Py_LeaveRecursiveCall()`](exceptions.html#c.Py_LeaveRecursiveCall "Py_LeaveRecursiveCall")
for calls made using *tp\_call*.

For efficiency, this is not the case for calls done using vectorcall:
the callee should use *Py\_EnterRecursiveCall* and *Py\_LeaveRecursiveCall*
if needed.

### Vectorcall Support API

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyVectorcall\_NARGS(size\_t nargsf)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.12.*

    Given a vectorcall *nargsf* argument, return the actual number of
    arguments.
    Currently equivalent to:

    ```
    (Py_ssize_t)(nargsf & ~PY_VECTORCALL_ARGUMENTS_OFFSET)

    ```

    However, the function `PyVectorcall_NARGS` should be used to allow
    for future extensions.

[vectorcallfunc](#c.vectorcallfunc "vectorcallfunc") PyVectorcall\_Function([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   If *op* does not support the vectorcall protocol (either because the type
    does not or because the specific instance does not), return *NULL*.
    Otherwise, return the vectorcall function pointer stored in *op*.
    This function never raises an exception.

    This is mostly useful to check whether or not *op* supports vectorcall,
    which can be done by checking `PyVectorcall_Function(op) != NULL`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyVectorcall\_Call([PyObject](structures.html#c.PyObject "PyObject") \*callable, [PyObject](structures.html#c.PyObject "PyObject") \*tuple, [PyObject](structures.html#c.PyObject "PyObject") \*dict)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.12.*

    Call *callable*’s [`vectorcallfunc`](#c.vectorcallfunc "vectorcallfunc") with positional and keyword
    arguments given in a tuple and dict, respectively.

    This is a specialized function, intended to be put in the
    [`tp_call`](typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") slot or be used in an implementation of `tp_call`.
    It does not check the [`Py_TPFLAGS_HAVE_VECTORCALL`](typeobj.html#c.Py_TPFLAGS_HAVE_VECTORCALL "Py_TPFLAGS_HAVE_VECTORCALL") flag
    and it does not fall back to `tp_call`.