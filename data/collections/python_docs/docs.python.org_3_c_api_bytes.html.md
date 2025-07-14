Bytes Objects
=============

These functions raise [`TypeError`](../library/exceptions.html#TypeError "TypeError") when expecting a bytes parameter and
called with a non-bytes parameter.

type PyBytesObject
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python bytes object.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyBytes\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python bytes type; it
    is the same object as [`bytes`](../library/stdtypes.html#bytes "bytes") in the Python layer.

int PyBytes\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if the object *o* is a bytes object or an instance of a subtype
    of the bytes type. This function always succeeds.

int PyBytes\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if the object *o* is a bytes object, but not an instance of a
    subtype of the bytes type. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBytes\_FromString(const char \*v)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new bytes object with a copy of the string *v* as value on success,
    and `NULL` on failure. The parameter *v* must not be `NULL`; it will not be
    checked.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBytes\_FromStringAndSize(const char \*v, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") len)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new bytes object with a copy of the string *v* as value and length
    *len* on success, and `NULL` on failure. If *v* is `NULL`, the contents of
    the bytes object are uninitialized.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBytes\_FromFormat(const char \*format, ...)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Take a C `printf()`-style *format* string and a variable number of
    arguments, calculate the size of the resulting Python bytes object and return
    a bytes object with the values formatted into it. The variable arguments
    must be C types and must correspond exactly to the format characters in the
    *format* string. The following format characters are allowed:

    | Format Characters | Type | Comment |
    | --- | --- | --- |
    | `%%` | *n/a* | The literal % character. |
    | `%c` | int | A single byte, represented as a C int. |
    | `%d` | int | Equivalent to `printf("%d")`. |
    | `%u` | unsigned int | Equivalent to `printf("%u")`. |
    | `%ld` | long | Equivalent to `printf("%ld")`. |
    | `%lu` | unsigned long | Equivalent to `printf("%lu")`. |
    | `%zd` | [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t") | Equivalent to `printf("%zd")`. |
    | `%zu` | size\_t | Equivalent to `printf("%zu")`. |
    | `%i` | int | Equivalent to `printf("%i")`. |
    | `%x` | int | Equivalent to `printf("%x")`. |
    | `%s` | const char\* | A null-terminated C character array. |
    | `%p` | const void\* | The hex representation of a C pointer. Mostly equivalent to `printf("%p")` except that it is guaranteed to start with the literal `0x` regardless of what the platform’s `printf` yields. |

    An unrecognized format character causes all the rest of the format string to be
    copied as-is to the result object, and any extra arguments discarded.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBytes\_FromFormatV(const char \*format, va\_list vargs)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Identical to [`PyBytes_FromFormat()`](#c.PyBytes_FromFormat "PyBytes_FromFormat") except that it takes exactly two
    arguments.

[PyObject](structures.html#c.PyObject "PyObject") \*PyBytes\_FromObject([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the bytes representation of object *o* that implements the buffer
    protocol.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyBytes\_Size([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the length of the bytes in bytes object *o*.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyBytes\_GET\_SIZE([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Similar to [`PyBytes_Size()`](#c.PyBytes_Size "PyBytes_Size"), but without error checking.

char \*PyBytes\_AsString([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return a pointer to the contents of *o*. The pointer
    refers to the internal buffer of *o*, which consists of `len(o) + 1`
    bytes. The last byte in the buffer is always null, regardless of
    whether there are any other null bytes. The data must not be
    modified in any way, unless the object was just created using
    `PyBytes_FromStringAndSize(NULL, size)`. It must not be deallocated. If
    *o* is not a bytes object at all, [`PyBytes_AsString()`](#c.PyBytes_AsString "PyBytes_AsString") returns `NULL`
    and raises [`TypeError`](../library/exceptions.html#TypeError "TypeError").

char \*PyBytes\_AS\_STRING([PyObject](structures.html#c.PyObject "PyObject") \*string)
:   Similar to [`PyBytes_AsString()`](#c.PyBytes_AsString "PyBytes_AsString"), but without error checking.

int PyBytes\_AsStringAndSize([PyObject](structures.html#c.PyObject "PyObject") \*obj, char \*\*buffer, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") \*length)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the null-terminated contents of the object *obj*
    through the output variables *buffer* and *length*.
    Returns `0` on success.

    If *length* is `NULL`, the bytes object
    may not contain embedded null bytes;
    if it does, the function returns `-1` and a [`ValueError`](../library/exceptions.html#ValueError "ValueError") is raised.

    The buffer refers to an internal buffer of *obj*, which includes an
    additional null byte at the end (not counted in *length*). The data
    must not be modified in any way, unless the object was just created using
    `PyBytes_FromStringAndSize(NULL, size)`. It must not be deallocated. If
    *obj* is not a bytes object at all, [`PyBytes_AsStringAndSize()`](#c.PyBytes_AsStringAndSize "PyBytes_AsStringAndSize")
    returns `-1` and raises [`TypeError`](../library/exceptions.html#TypeError "TypeError").

    Changed in version 3.5: Previously, [`TypeError`](../library/exceptions.html#TypeError "TypeError") was raised when embedded null bytes were
    encountered in the bytes object.

void PyBytes\_Concat([PyObject](structures.html#c.PyObject "PyObject") \*\*bytes, [PyObject](structures.html#c.PyObject "PyObject") \*newpart)
:   *Part of the [Stable ABI](stable.html#stable).*

    Create a new bytes object in *\*bytes* containing the contents of *newpart*
    appended to *bytes*; the caller will own the new reference. The reference to
    the old value of *bytes* will be stolen. If the new object cannot be
    created, the old reference to *bytes* will still be discarded and the value
    of *\*bytes* will be set to `NULL`; the appropriate exception will be set.

void PyBytes\_ConcatAndDel([PyObject](structures.html#c.PyObject "PyObject") \*\*bytes, [PyObject](structures.html#c.PyObject "PyObject") \*newpart)
:   *Part of the [Stable ABI](stable.html#stable).*

    Create a new bytes object in *\*bytes* containing the contents of *newpart*
    appended to *bytes*. This version releases the [strong reference](../glossary.html#term-strong-reference)
    to *newpart* (i.e. decrements its reference count).

int \_PyBytes\_Resize([PyObject](structures.html#c.PyObject "PyObject") \*\*bytes, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") newsize)
:   Resize a bytes object. *newsize* will be the new length of the bytes object.
    You can think of it as creating a new bytes object and destroying the old
    one, only more efficiently.
    Pass the address of an
    existing bytes object as an lvalue (it may be written into), and the new size
    desired. On success, *\*bytes* holds the resized bytes object and `0` is
    returned; the address in *\*bytes* may differ from its input value. If the
    reallocation fails, the original bytes object at *\*bytes* is deallocated,
    *\*bytes* is set to `NULL`, [`MemoryError`](../library/exceptions.html#MemoryError "MemoryError") is set, and `-1` is
    returned.