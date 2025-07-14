Frame Objects
=============

type PyFrameObject
:   *Part of the [Limited API](stable.html#stable) (as an opaque struct).*

    The C structure of the objects used to describe frame objects.

    There are no public members in this structure.

    Changed in version 3.11: The members of this structure were removed from the public C API.
    Refer to the [What’s New entry](../whatsnew/3.11.html#pyframeobject-3-11-hiding)
    for details.

The [`PyEval_GetFrame()`](reflection.html#c.PyEval_GetFrame "PyEval_GetFrame") and [`PyThreadState_GetFrame()`](init.html#c.PyThreadState_GetFrame "PyThreadState_GetFrame") functions
can be used to get a frame object.

See also [Reflection](reflection.html#reflection).

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyFrame\_Type
:   The type of frame objects.
    It is the same object as [`types.FrameType`](../library/types.html#types.FrameType "types.FrameType") in the Python layer.

    Changed in version 3.11: Previously, this type was only available after including
    `<frameobject.h>`.

int PyFrame\_Check([PyObject](structures.html#c.PyObject "PyObject") \*obj)
:   Return non-zero if *obj* is a frame object.

    Changed in version 3.11: Previously, this function was only available after including
    `<frameobject.h>`.

[PyFrameObject](#c.PyFrameObject "PyFrameObject") \*PyFrame\_GetBack([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Get the *frame* next outer frame.

    Return a [strong reference](../glossary.html#term-strong-reference), or `NULL` if *frame* has no outer
    frame.

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetBuiltins([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Get the *frame*’s [`f_builtins`](../reference/datamodel.html#frame.f_builtins "frame.f_builtins") attribute.

    Return a [strong reference](../glossary.html#term-strong-reference). The result cannot be `NULL`.

[PyCodeObject](code.html#c.PyCodeObject "PyCodeObject") \*PyFrame\_GetCode([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Get the *frame* code.

    Return a [strong reference](../glossary.html#term-strong-reference).

    The result (frame code) cannot be `NULL`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetGenerator([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Get the generator, coroutine, or async generator that owns this frame,
    or `NULL` if this frame is not owned by a generator.
    Does not raise an exception, even if the return value is `NULL`.

    Return a [strong reference](../glossary.html#term-strong-reference), or `NULL`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetGlobals([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Get the *frame*’s [`f_globals`](../reference/datamodel.html#frame.f_globals "frame.f_globals") attribute.

    Return a [strong reference](../glossary.html#term-strong-reference). The result cannot be `NULL`.

int PyFrame\_GetLasti([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   Get the *frame*’s [`f_lasti`](../reference/datamodel.html#frame.f_lasti "frame.f_lasti") attribute.

    Returns -1 if `frame.f_lasti` is `None`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetVar([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame, [PyObject](structures.html#c.PyObject "PyObject") \*name)
:   *Return value: New reference.*

    Get the variable *name* of *frame*.

    * Return a [strong reference](../glossary.html#term-strong-reference) to the variable value on success.
    * Raise [`NameError`](../library/exceptions.html#NameError "NameError") and return `NULL` if the variable does not exist.
    * Raise an exception and return `NULL` on error.

    *name* type must be a [`str`](../library/stdtypes.html#str "str").

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetVarString([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame, const char \*name)
:   *Return value: New reference.*

    Similar to [`PyFrame_GetVar()`](#c.PyFrame_GetVar "PyFrame_GetVar"), but the variable name is a C string
    encoded in UTF-8.

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrame\_GetLocals([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Return value: New reference.*

    Get the *frame*’s [`f_locals`](../reference/datamodel.html#frame.f_locals "frame.f_locals") attribute.
    If the frame refers to an [optimized scope](../glossary.html#term-optimized-scope), this returns a
    write-through proxy object that allows modifying the locals.
    In all other cases (classes, modules, [`exec()`](../library/functions.html#exec "exec"), [`eval()`](../library/functions.html#eval "eval")) it returns
    the mapping representing the frame locals directly (as described for
    [`locals()`](../library/functions.html#locals "locals")).

    Return a [strong reference](../glossary.html#term-strong-reference).

int PyFrame\_GetLineNumber([PyFrameObject](#c.PyFrameObject "PyFrameObject") \*frame)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Return the line number that *frame* is currently executing.

Frame Locals Proxies
--------------------

The [`f_locals`](../reference/datamodel.html#frame.f_locals "frame.f_locals") attribute on a [frame object](../reference/datamodel.html#frame-objects)
is an instance of a “frame-locals proxy”. The proxy object exposes a
write-through view of the underlying locals dictionary for the frame. This
ensures that the variables exposed by `f_locals` are always up to date with
the live local variables in the frame itself.

See [**PEP 667**](https://peps.python.org/pep-0667/) for more information.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyFrameLocalsProxy\_Type
:   The type of frame [`locals()`](../library/functions.html#locals "locals") proxy objects.

int PyFrameLocalsProxy\_Check([PyObject](structures.html#c.PyObject "PyObject") \*obj)
:   Return non-zero if *obj* is a frame [`locals()`](../library/functions.html#locals "locals") proxy.

Internal Frames
---------------

Unless using [**PEP 523**](https://peps.python.org/pep-0523/), you will not need this.

struct \_PyInterpreterFrame
:   The interpreter’s internal frame representation.

[PyObject](structures.html#c.PyObject "PyObject") \*PyUnstable\_InterpreterFrame\_GetCode(struct [\_PyInterpreterFrame](#c._PyInterpreterFrame "_PyInterpreterFrame") \*frame);
:   *This is [Unstable API](stable.html#unstable-c-api). It may change without warning in minor releases.*

int PyUnstable\_InterpreterFrame\_GetLasti(struct [\_PyInterpreterFrame](#c._PyInterpreterFrame "_PyInterpreterFrame") \*frame);
:   *This is [Unstable API](stable.html#unstable-c-api). It may change without warning in minor releases.*

    Return the byte offset into the last executed instruction.

int PyUnstable\_InterpreterFrame\_GetLine(struct [\_PyInterpreterFrame](#c._PyInterpreterFrame "_PyInterpreterFrame") \*frame);
:   *This is [Unstable API](stable.html#unstable-c-api). It may change without warning in minor releases.*

    Return the currently executing line number, or -1 if there is no line number.