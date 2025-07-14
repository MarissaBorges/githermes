Tuple Objects
=============

type PyTupleObject
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python tuple object.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyTuple\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python tuple type; it
    is the same object as [`tuple`](../library/stdtypes.html#tuple "tuple") in the Python layer.

int PyTuple\_Check([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a tuple object or an instance of a subtype of the
    tuple type. This function always succeeds.

int PyTuple\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a tuple object, but not an instance of a subtype of the
    tuple type. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTuple\_New([Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") len)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new tuple object of size *len*,
    or `NULL` with an exception set on failure.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTuple\_Pack([Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") n, ...)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new tuple object of size *n*,
    or `NULL` with an exception set on failure. The tuple values
    are initialized to the subsequent *n* C arguments pointing to Python objects.
    `PyTuple_Pack(2, a, b)` is equivalent to `Py_BuildValue("(OO)", a, b)`.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyTuple\_Size([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   *Part of the [Stable ABI](stable.html#stable).*

    Take a pointer to a tuple object, and return the size of that tuple.
    On error, return `-1` and with an exception set.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyTuple\_GET\_SIZE([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Like [`PyTuple_Size()`](#c.PyTuple_Size "PyTuple_Size"), but without error checking.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTuple\_GetItem([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos)
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the object at position *pos* in the tuple pointed to by *p*. If *pos* is
    negative or out of bounds, return `NULL` and set an [`IndexError`](../library/exceptions.html#IndexError "IndexError") exception.

    The returned reference is borrowed from the tuple *p*
    (that is: it is only valid as long as you hold a reference to *p*).
    To get a [strong reference](../glossary.html#term-strong-reference), use
    [`Py_NewRef(PyTuple_GetItem(...))`](refcounting.html#c.Py_NewRef "Py_NewRef")
    or [`PySequence_GetItem()`](sequence.html#c.PySequence_GetItem "PySequence_GetItem").

[PyObject](structures.html#c.PyObject "PyObject") \*PyTuple\_GET\_ITEM([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos)
:   *Return value: Borrowed reference.*

    Like [`PyTuple_GetItem()`](#c.PyTuple_GetItem "PyTuple_GetItem"), but does no checking of its arguments.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTuple\_GetSlice([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") low, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") high)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the slice of the tuple pointed to by *p* between *low* and *high*,
    or `NULL` with an exception set on failure.

    This is the equivalent of the Python expression `p[low:high]`.
    Indexing from the end of the tuple is not supported.

int PyTuple\_SetItem([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos, [PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Insert a reference to object *o* at position *pos* of the tuple pointed to by
    *p*. Return `0` on success. If *pos* is out of bounds, return `-1`
    and set an [`IndexError`](../library/exceptions.html#IndexError "IndexError") exception.

    Note

    This function “steals” a reference to *o* and discards a reference to
    an item already in the tuple at the affected position.

void PyTuple\_SET\_ITEM([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos, [PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Like [`PyTuple_SetItem()`](#c.PyTuple_SetItem "PyTuple_SetItem"), but does no error checking, and should *only* be
    used to fill in brand new tuples.

    Bounds checking is performed as an assertion if Python is built in
    [debug mode](../using/configure.html#debug-build) or [`with assertions`](../using/configure.html#cmdoption-with-assertions).

    Note

    This function “steals” a reference to *o*, and, unlike
    [`PyTuple_SetItem()`](#c.PyTuple_SetItem "PyTuple_SetItem"), does *not* discard a reference to any item that
    is being replaced; any reference in the tuple at position *pos* will be
    leaked.

int \_PyTuple\_Resize([PyObject](structures.html#c.PyObject "PyObject") \*\*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") newsize)
:   Can be used to resize a tuple. *newsize* will be the new length of the tuple.
    Because tuples are *supposed* to be immutable, this should only be used if there
    is only one reference to the object. Do *not* use this if the tuple may already
    be known to some other part of the code. The tuple will always grow or shrink
    at the end. Think of this as destroying the old tuple and creating a new one,
    only more efficiently. Returns `0` on success. Client code should never
    assume that the resulting value of `*p` will be the same as before calling
    this function. If the object referenced by `*p` is replaced, the original
    `*p` is destroyed. On failure, returns `-1` and sets `*p` to `NULL`, and
    raises [`MemoryError`](../library/exceptions.html#MemoryError "MemoryError") or [`SystemError`](../library/exceptions.html#SystemError "SystemError").

Struct Sequence Objects
=======================

Struct sequence objects are the C equivalent of [`namedtuple()`](../library/collections.html#collections.namedtuple "collections.namedtuple")
objects, i.e. a sequence whose items can also be accessed through attributes.
To create a struct sequence, you first have to create a specific struct sequence
type.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*PyStructSequence\_NewType([PyStructSequence\_Desc](#c.PyStructSequence_Desc "PyStructSequence_Desc") \*desc)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Create a new struct sequence type from the data in *desc*, described below. Instances
    of the resulting type can be created with [`PyStructSequence_New()`](#c.PyStructSequence_New "PyStructSequence_New").

    Return `NULL` with an exception set on failure.

void PyStructSequence\_InitType([PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*type, [PyStructSequence\_Desc](#c.PyStructSequence_Desc "PyStructSequence_Desc") \*desc)
:   Initializes a struct sequence type *type* from *desc* in place.

int PyStructSequence\_InitType2([PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*type, [PyStructSequence\_Desc](#c.PyStructSequence_Desc "PyStructSequence_Desc") \*desc)
:   Like [`PyStructSequence_InitType()`](#c.PyStructSequence_InitType "PyStructSequence_InitType"), but returns `0` on success
    and `-1` with an exception set on failure.

type PyStructSequence\_Desc
:   *Part of the [Stable ABI](stable.html#stable) (including all members).*

    Contains the meta information of a struct sequence type to create.

    const char \*name
    :   Fully qualified name of the type; null-terminated UTF-8 encoded.
        The name must contain the module name.

    const char \*doc
    :   Pointer to docstring for the type or `NULL` to omit.

    [PyStructSequence\_Field](#c.PyStructSequence_Field "PyStructSequence_Field") \*fields
    :   Pointer to `NULL`-terminated array with field names of the new type.

    int n\_in\_sequence
    :   Number of fields visible to the Python side (if used as tuple).

type PyStructSequence\_Field
:   *Part of the [Stable ABI](stable.html#stable) (including all members).*

    Describes a field of a struct sequence. As a struct sequence is modeled as a
    tuple, all fields are typed as [PyObject](structures.html#c.PyObject "PyObject")\*. The index in the
    [`fields`](#c.PyStructSequence_Desc.fields "PyStructSequence_Desc.fields") array of
    the [`PyStructSequence_Desc`](#c.PyStructSequence_Desc "PyStructSequence_Desc") determines which
    field of the struct sequence is described.

    const char \*name
    :   Name for the field or `NULL` to end the list of named fields,
        set to [`PyStructSequence_UnnamedField`](#c.PyStructSequence_UnnamedField "PyStructSequence_UnnamedField") to leave unnamed.

    const char \*doc
    :   Field docstring or `NULL` to omit.

const char \*const PyStructSequence\_UnnamedField
:   *Part of the [Stable ABI](stable.html#stable) since version 3.11.*

    Special value for a field name to leave it unnamed.

    Changed in version 3.9: The type was changed from `char *`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyStructSequence\_New([PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*type)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Creates an instance of *type*, which must have been created with
    [`PyStructSequence_NewType()`](#c.PyStructSequence_NewType "PyStructSequence_NewType").

    Return `NULL` with an exception set on failure.

[PyObject](structures.html#c.PyObject "PyObject") \*PyStructSequence\_GetItem([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos)
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the object at position *pos* in the struct sequence pointed to by *p*.

    Bounds checking is performed as an assertion if Python is built in
    [debug mode](../using/configure.html#debug-build) or [`with assertions`](../using/configure.html#cmdoption-with-assertions).

[PyObject](structures.html#c.PyObject "PyObject") \*PyStructSequence\_GET\_ITEM([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos)
:   *Return value: Borrowed reference.*

    Alias to [`PyStructSequence_GetItem()`](#c.PyStructSequence_GetItem "PyStructSequence_GetItem").

void PyStructSequence\_SetItem([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") pos, [PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Sets the field at index *pos* of the struct sequence *p* to value *o*. Like
    [`PyTuple_SET_ITEM()`](#c.PyTuple_SET_ITEM "PyTuple_SET_ITEM"), this should only be used to fill in brand new
    instances.

    Bounds checking is performed as an assertion if Python is built in
    [debug mode](../using/configure.html#debug-build) or [`with assertions`](../using/configure.html#cmdoption-with-assertions).

    Note

    This function “steals” a reference to *o*.

void PyStructSequence\_SET\_ITEM([PyObject](structures.html#c.PyObject "PyObject") \*p, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") \*pos, [PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Alias to [`PyStructSequence_SetItem()`](#c.PyStructSequence_SetItem "PyStructSequence_SetItem").