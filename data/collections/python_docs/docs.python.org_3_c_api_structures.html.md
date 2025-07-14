Common Object Structures
========================

There are a large number of structures which are used in the definition of
object types for Python. This section describes these structures and how they
are used.

Base object types and macros
----------------------------

All Python objects ultimately share a small number of fields at the beginning
of the object’s representation in memory. These are represented by the
[`PyObject`](#c.PyObject "PyObject") and [`PyVarObject`](#c.PyVarObject "PyVarObject") types, which are defined, in turn,
by the expansions of some macros also used, whether directly or indirectly, in
the definition of all other Python objects. Additional macros can be found
under [reference counting](refcounting.html#countingrefs).

type PyObject
:   *Part of the [Limited API](stable.html#stable). (Only some members are part of the stable ABI.)*

    All object types are extensions of this type. This is a type which
    contains the information Python needs to treat a pointer to an object as an
    object. In a normal “release” build, it contains only the object’s
    reference count and a pointer to the corresponding type object.
    Nothing is actually declared to be a [`PyObject`](#c.PyObject "PyObject"), but every pointer
    to a Python object can be cast to a [PyObject](#c.PyObject "PyObject")\*. Access to the
    members must be done by using the macros [`Py_REFCNT`](refcounting.html#c.Py_REFCNT "Py_REFCNT") and
    [`Py_TYPE`](#c.Py_TYPE "Py_TYPE").

type PyVarObject
:   *Part of the [Limited API](stable.html#stable). (Only some members are part of the stable ABI.)*

    This is an extension of [`PyObject`](#c.PyObject "PyObject") that adds the [`ob_size`](typeobj.html#c.PyVarObject.ob_size "PyVarObject.ob_size")
    field. This is only used for objects that have some notion of *length*.
    This type does not often appear in the Python/C API.
    Access to the members must be done by using the macros
    [`Py_REFCNT`](refcounting.html#c.Py_REFCNT "Py_REFCNT"), [`Py_TYPE`](#c.Py_TYPE "Py_TYPE"), and [`Py_SIZE`](#c.Py_SIZE "Py_SIZE").

PyObject\_HEAD
:   This is a macro used when declaring new types which represent objects
    without a varying length. The PyObject\_HEAD macro expands to:

    See documentation of [`PyObject`](#c.PyObject "PyObject") above.

PyObject\_VAR\_HEAD
:   This is a macro used when declaring new types which represent objects
    with a length that varies from instance to instance.
    The PyObject\_VAR\_HEAD macro expands to:

    See documentation of [`PyVarObject`](#c.PyVarObject "PyVarObject") above.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyBaseObject\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    The base class of all other objects, the same as [`object`](../library/functions.html#object "object") in Python.

int Py\_Is([PyObject](#c.PyObject "PyObject") \*x, [PyObject](#c.PyObject "PyObject") \*y)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Test if the *x* object is the *y* object, the same as `x is y` in Python.

int Py\_IsNone([PyObject](#c.PyObject "PyObject") \*x)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Test if an object is the `None` singleton,
    the same as `x is None` in Python.

int Py\_IsTrue([PyObject](#c.PyObject "PyObject") \*x)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Test if an object is the `True` singleton,
    the same as `x is True` in Python.

int Py\_IsFalse([PyObject](#c.PyObject "PyObject") \*x)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Test if an object is the `False` singleton,
    the same as `x is False` in Python.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*Py\_TYPE([PyObject](#c.PyObject "PyObject") \*o)
:   *Return value: Borrowed reference.*

    Get the type of the Python object *o*.

    Return a [borrowed reference](../glossary.html#term-borrowed-reference).

    Use the [`Py_SET_TYPE()`](#c.Py_SET_TYPE "Py_SET_TYPE") function to set an object type.

    Changed in version 3.11: [`Py_TYPE()`](#c.Py_TYPE "Py_TYPE") is changed to an inline static function.
    The parameter type is no longer const [PyObject](#c.PyObject "PyObject")\*.

int Py\_IS\_TYPE([PyObject](#c.PyObject "PyObject") \*o, [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*type)
:   Return non-zero if the object *o* type is *type*. Return zero otherwise.
    Equivalent to: `Py_TYPE(o) == type`.

void Py\_SET\_TYPE([PyObject](#c.PyObject "PyObject") \*o, [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*type)
:   Set the object *o* type to *type*.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") Py\_SIZE([PyVarObject](#c.PyVarObject "PyVarObject") \*o)
:   Get the size of the Python object *o*.

    Use the [`Py_SET_SIZE()`](#c.Py_SET_SIZE "Py_SET_SIZE") function to set an object size.

    Changed in version 3.11: [`Py_SIZE()`](#c.Py_SIZE "Py_SIZE") is changed to an inline static function.
    The parameter type is no longer const [PyVarObject](#c.PyVarObject "PyVarObject")\*.

void Py\_SET\_SIZE([PyVarObject](#c.PyVarObject "PyVarObject") \*o, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") size)
:   Set the object *o* size to *size*.

PyObject\_HEAD\_INIT(type)
:   This is a macro which expands to initialization values for a new
    [`PyObject`](#c.PyObject "PyObject") type. This macro expands to:

    ```
    _PyObject_EXTRA_INIT
    1, type,

    ```

PyVarObject\_HEAD\_INIT(type, size)
:   This is a macro which expands to initialization values for a new
    [`PyVarObject`](#c.PyVarObject "PyVarObject") type, including the [`ob_size`](typeobj.html#c.PyVarObject.ob_size "PyVarObject.ob_size") field.
    This macro expands to:

    ```
    _PyObject_EXTRA_INIT
    1, type, size,

    ```

Implementing functions and methods
----------------------------------

type PyCFunction
:   *Part of the [Stable ABI](stable.html#stable).*

    Type of the functions used to implement most Python callables in C.
    Functions of this type take two [PyObject](#c.PyObject "PyObject")\* parameters and return
    one such value. If the return value is `NULL`, an exception shall have
    been set. If not `NULL`, the return value is interpreted as the return
    value of the function as exposed in Python. The function must return a new
    reference.

    The function signature is:

    ```
    PyObject *PyCFunction(PyObject *self,
                          PyObject *args);

    ```

type PyCFunctionWithKeywords
:   *Part of the [Stable ABI](stable.html#stable).*

    Type of the functions used to implement Python callables in C
    with signature [METH\_VARARGS | METH\_KEYWORDS](#meth-varargs-meth-keywords).
    The function signature is:

    ```
    PyObject *PyCFunctionWithKeywords(PyObject *self,
                                      PyObject *args,
                                      PyObject *kwargs);

    ```

type PyCFunctionFast
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Type of the functions used to implement Python callables in C
    with signature [`METH_FASTCALL`](#c.METH_FASTCALL "METH_FASTCALL").
    The function signature is:

    ```
    PyObject *PyCFunctionFast(PyObject *self,
                              PyObject *const *args,
                              Py_ssize_t nargs);

    ```

type PyCFunctionFastWithKeywords
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Type of the functions used to implement Python callables in C
    with signature [METH\_FASTCALL | METH\_KEYWORDS](#meth-fastcall-meth-keywords).
    The function signature is:

    ```
    PyObject *PyCFunctionFastWithKeywords(PyObject *self,
                                          PyObject *const *args,
                                          Py_ssize_t nargs,
                                          PyObject *kwnames);

    ```

type PyCMethod
:   Type of the functions used to implement Python callables in C
    with signature [METH\_METHOD | METH\_FASTCALL | METH\_KEYWORDS](#meth-method-meth-fastcall-meth-keywords).
    The function signature is:

    ```
    PyObject *PyCMethod(PyObject *self,
                        PyTypeObject *defining_class,
                        PyObject *const *args,
                        Py_ssize_t nargs,
                        PyObject *kwnames)

    ```

type PyMethodDef
:   *Part of the [Stable ABI](stable.html#stable) (including all members).*

    Structure used to describe a method of an extension type. This structure has
    four fields:

    const char \*ml\_name
    :   Name of the method.

    [PyCFunction](#c.PyCFunction "PyCFunction") ml\_meth
    :   Pointer to the C implementation.

    int ml\_flags
    :   Flags bits indicating how the call should be constructed.

    const char \*ml\_doc
    :   Points to the contents of the docstring.

The [`ml_meth`](#c.PyMethodDef.ml_meth "PyMethodDef.ml_meth") is a C function pointer.
The functions may be of different
types, but they always return [PyObject](#c.PyObject "PyObject")\*. If the function is not of
the [`PyCFunction`](#c.PyCFunction "PyCFunction"), the compiler will require a cast in the method table.
Even though [`PyCFunction`](#c.PyCFunction "PyCFunction") defines the first parameter as
[PyObject](#c.PyObject "PyObject")\*, it is common that the method implementation uses the
specific C type of the *self* object.

The [`ml_flags`](#c.PyMethodDef.ml_flags "PyMethodDef.ml_flags") field is a bitfield which can include
the following flags.
The individual flags indicate either a calling convention or a binding
convention.

There are these calling conventions:

METH\_VARARGS
:   This is the typical calling convention, where the methods have the type
    [`PyCFunction`](#c.PyCFunction "PyCFunction"). The function expects two [PyObject](#c.PyObject "PyObject")\* values.
    The first one is the *self* object for methods; for module functions, it is
    the module object. The second parameter (often called *args*) is a tuple
    object representing all arguments. This parameter is typically processed
    using [`PyArg_ParseTuple()`](arg.html#c.PyArg_ParseTuple "PyArg_ParseTuple") or [`PyArg_UnpackTuple()`](arg.html#c.PyArg_UnpackTuple "PyArg_UnpackTuple").

METH\_KEYWORDS
:   Can only be used in certain combinations with other flags:
    [METH\_VARARGS | METH\_KEYWORDS](#meth-varargs-meth-keywords),
    [METH\_FASTCALL | METH\_KEYWORDS](#meth-fastcall-meth-keywords) and
    [METH\_METHOD | METH\_FASTCALL | METH\_KEYWORDS](#meth-method-meth-fastcall-meth-keywords).

[METH\_VARARGS](#c.METH_VARARGS "METH_VARARGS") | [METH\_KEYWORDS](#c.METH_KEYWORDS "METH_KEYWORDS")
:   Methods with these flags must be of type [`PyCFunctionWithKeywords`](#c.PyCFunctionWithKeywords "PyCFunctionWithKeywords").
    The function expects three parameters: *self*, *args*, *kwargs* where
    *kwargs* is a dictionary of all the keyword arguments or possibly `NULL`
    if there are no keyword arguments. The parameters are typically processed
    using [`PyArg_ParseTupleAndKeywords()`](arg.html#c.PyArg_ParseTupleAndKeywords "PyArg_ParseTupleAndKeywords").

METH\_FASTCALL
:   Fast calling convention supporting only positional arguments.
    The methods have the type [`PyCFunctionFast`](#c.PyCFunctionFast "PyCFunctionFast").
    The first parameter is *self*, the second parameter is a C array
    of [PyObject](#c.PyObject "PyObject")\* values indicating the arguments and the third
    parameter is the number of arguments (the length of the array).

    Changed in version 3.10: `METH_FASTCALL` is now part of the [stable ABI](stable.html#stable-abi).

[METH\_FASTCALL](#c.METH_FASTCALL "METH_FASTCALL") | [METH\_KEYWORDS](#c.METH_KEYWORDS "METH_KEYWORDS")
:   Extension of [`METH_FASTCALL`](#c.METH_FASTCALL "METH_FASTCALL") supporting also keyword arguments,
    with methods of type [`PyCFunctionFastWithKeywords`](#c.PyCFunctionFastWithKeywords "PyCFunctionFastWithKeywords").
    Keyword arguments are passed the same way as in the
    [vectorcall protocol](call.html#vectorcall):
    there is an additional fourth [PyObject](#c.PyObject "PyObject")\* parameter
    which is a tuple representing the names of the keyword arguments
    (which are guaranteed to be strings)
    or possibly `NULL` if there are no keywords. The values of the keyword
    arguments are stored in the *args* array, after the positional arguments.

METH\_METHOD
:   Can only be used in the combination with other flags:
    [METH\_METHOD | METH\_FASTCALL | METH\_KEYWORDS](#meth-method-meth-fastcall-meth-keywords).

[METH\_METHOD](#c.METH_METHOD "METH_METHOD") | [METH\_FASTCALL](#c.METH_FASTCALL "METH_FASTCALL") | [METH\_KEYWORDS](#c.METH_KEYWORDS "METH_KEYWORDS")
:   Extension of [METH\_FASTCALL | METH\_KEYWORDS](#meth-fastcall-meth-keywords)
    supporting the *defining class*, that is,
    the class that contains the method in question.
    The defining class might be a superclass of `Py_TYPE(self)`.

    The method needs to be of type [`PyCMethod`](#c.PyCMethod "PyCMethod"), the same as for
    `METH_FASTCALL | METH_KEYWORDS` with `defining_class` argument added after
    `self`.

METH\_NOARGS
:   Methods without parameters don’t need to check whether arguments are given if
    they are listed with the [`METH_NOARGS`](#c.METH_NOARGS "METH_NOARGS") flag. They need to be of type
    [`PyCFunction`](#c.PyCFunction "PyCFunction"). The first parameter is typically named *self* and will
    hold a reference to the module or object instance. In all cases the second
    parameter will be `NULL`.

    The function must have 2 parameters. Since the second parameter is unused,
    [`Py_UNUSED`](intro.html#c.Py_UNUSED "Py_UNUSED") can be used to prevent a compiler warning.

METH\_O
:   Methods with a single object argument can be listed with the [`METH_O`](#c.METH_O "METH_O")
    flag, instead of invoking [`PyArg_ParseTuple()`](arg.html#c.PyArg_ParseTuple "PyArg_ParseTuple") with a `"O"` argument.
    They have the type [`PyCFunction`](#c.PyCFunction "PyCFunction"), with the *self* parameter, and a
    [PyObject](#c.PyObject "PyObject")\* parameter representing the single argument.

These two constants are not used to indicate the calling convention but the
binding when use with methods of classes. These may not be used for functions
defined for modules. At most one of these flags may be set for any given
method.

METH\_CLASS
:   The method will be passed the type object as the first parameter rather
    than an instance of the type. This is used to create *class methods*,
    similar to what is created when using the [`classmethod()`](../library/functions.html#classmethod "classmethod") built-in
    function.

METH\_STATIC
:   The method will be passed `NULL` as the first parameter rather than an
    instance of the type. This is used to create *static methods*, similar to
    what is created when using the [`staticmethod()`](../library/functions.html#staticmethod "staticmethod") built-in function.

One other constant controls whether a method is loaded in place of another
definition with the same method name.

METH\_COEXIST
:   The method will be loaded in place of existing definitions. Without
    *METH\_COEXIST*, the default is to skip repeated definitions. Since slot
    wrappers are loaded before the method table, the existence of a
    *sq\_contains* slot, for example, would generate a wrapped method named
    [`__contains__()`](../reference/datamodel.html#object.__contains__ "object.__contains__") and preclude the loading of a corresponding
    PyCFunction with the same name. With the flag defined, the PyCFunction
    will be loaded in place of the wrapper object and will co-exist with the
    slot. This is helpful because calls to PyCFunctions are optimized more
    than wrapper object calls.

[PyObject](#c.PyObject "PyObject") \*PyCMethod\_New([PyMethodDef](#c.PyMethodDef "PyMethodDef") \*ml, [PyObject](#c.PyObject "PyObject") \*self, [PyObject](#c.PyObject "PyObject") \*module, [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") \*cls)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.9.*

    Turn *ml* into a Python [callable](../glossary.html#term-callable) object.
    The caller must ensure that *ml* outlives the [callable](../glossary.html#term-callable).
    Typically, *ml* is defined as a static variable.

    The *self* parameter will be passed as the *self* argument
    to the C function in `ml->ml_meth` when invoked.
    *self* can be `NULL`.

    The [callable](../glossary.html#term-callable) object’s `__module__` attribute
    can be set from the given *module* argument.
    *module* should be a Python string,
    which will be used as name of the module the function is defined in.
    If unavailable, it can be set to [`None`](../library/constants.html#None "None") or `NULL`.

    The *cls* parameter will be passed as the *defining\_class*
    argument to the C function.
    Must be set if [`METH_METHOD`](#c.METH_METHOD "METH_METHOD") is set on `ml->ml_flags`.

[PyObject](#c.PyObject "PyObject") \*PyCFunction\_NewEx([PyMethodDef](#c.PyMethodDef "PyMethodDef") \*ml, [PyObject](#c.PyObject "PyObject") \*self, [PyObject](#c.PyObject "PyObject") \*module)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Equivalent to `PyCMethod_New(ml, self, module, NULL)`.

[PyObject](#c.PyObject "PyObject") \*PyCFunction\_New([PyMethodDef](#c.PyMethodDef "PyMethodDef") \*ml, [PyObject](#c.PyObject "PyObject") \*self)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.4.*

    Equivalent to `PyCMethod_New(ml, self, NULL, NULL)`.

Accessing attributes of extension types
---------------------------------------

type PyMemberDef
:   *Part of the [Stable ABI](stable.html#stable) (including all members).*

    Structure which describes an attribute of a type which corresponds to a C
    struct member.
    When defining a class, put a NULL-terminated array of these
    structures in the [`tp_members`](typeobj.html#c.PyTypeObject.tp_members "PyTypeObject.tp_members") slot.

    Its fields are, in order:

    const char \*name
    :   Name of the member.
        A NULL value marks the end of a `PyMemberDef[]` array.

        The string should be static, no copy is made of it.

    int type
    :   The type of the member in the C struct.
        See [Member types](#pymemberdef-types) for the possible values.

    [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") offset
    :   The offset in bytes that the member is located on the type’s object struct.

    int flags
    :   Zero or more of the [Member flags](#pymemberdef-flags), combined using bitwise OR.

    const char \*doc
    :   The docstring, or NULL.
        The string should be static, no copy is made of it.
        Typically, it is defined using [`PyDoc_STR`](intro.html#c.PyDoc_STR "PyDoc_STR").

    By default (when [`flags`](#c.PyMemberDef.flags "PyMemberDef.flags") is `0`), members allow
    both read and write access.
    Use the [`Py_READONLY`](#c.Py_READONLY "Py_READONLY") flag for read-only access.
    Certain types, like [`Py_T_STRING`](#c.Py_T_STRING "Py_T_STRING"), imply [`Py_READONLY`](#c.Py_READONLY "Py_READONLY").
    Only [`Py_T_OBJECT_EX`](#c.Py_T_OBJECT_EX "Py_T_OBJECT_EX") (and legacy [`T_OBJECT`](#c.T_OBJECT "T_OBJECT")) members can
    be deleted.

    For heap-allocated types (created using [`PyType_FromSpec()`](type.html#c.PyType_FromSpec "PyType_FromSpec") or similar),
    `PyMemberDef` may contain a definition for the special member
    `"__vectorcalloffset__"`, corresponding to
    [`tp_vectorcall_offset`](typeobj.html#c.PyTypeObject.tp_vectorcall_offset "PyTypeObject.tp_vectorcall_offset") in type objects.
    These must be defined with `Py_T_PYSSIZET` and `Py_READONLY`, for example:

    ```
    static PyMemberDef spam_type_members[] = {
        {"__vectorcalloffset__", Py_T_PYSSIZET,
         offsetof(Spam_object, vectorcall), Py_READONLY},
        {NULL}  /* Sentinel */
    };

    ```

    (You may need to `#include <stddef.h>` for `offsetof()`.)

    The legacy offsets [`tp_dictoffset`](typeobj.html#c.PyTypeObject.tp_dictoffset "PyTypeObject.tp_dictoffset") and
    [`tp_weaklistoffset`](typeobj.html#c.PyTypeObject.tp_weaklistoffset "PyTypeObject.tp_weaklistoffset") can be defined similarly using
    `"__dictoffset__"` and `"__weaklistoffset__"` members, but extensions
    are strongly encouraged to use [`Py_TPFLAGS_MANAGED_DICT`](typeobj.html#c.Py_TPFLAGS_MANAGED_DICT "Py_TPFLAGS_MANAGED_DICT") and
    [`Py_TPFLAGS_MANAGED_WEAKREF`](typeobj.html#c.Py_TPFLAGS_MANAGED_WEAKREF "Py_TPFLAGS_MANAGED_WEAKREF") instead.

    Changed in version 3.12: `PyMemberDef` is always available.
    Previously, it required including `"structmember.h"`.

[PyObject](#c.PyObject "PyObject") \*PyMember\_GetOne(const char \*obj\_addr, struct [PyMemberDef](#c.PyMemberDef "PyMemberDef") \*m)
:   *Part of the [Stable ABI](stable.html#stable).*

    Get an attribute belonging to the object at address *obj\_addr*. The
    attribute is described by `PyMemberDef` *m*. Returns `NULL`
    on error.

    Changed in version 3.12: `PyMember_GetOne` is always available.
    Previously, it required including `"structmember.h"`.

int PyMember\_SetOne(char \*obj\_addr, struct [PyMemberDef](#c.PyMemberDef "PyMemberDef") \*m, [PyObject](#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Set an attribute belonging to the object at address *obj\_addr* to object *o*.
    The attribute to set is described by `PyMemberDef` *m*. Returns `0`
    if successful and a negative value on failure.

    Changed in version 3.12: `PyMember_SetOne` is always available.
    Previously, it required including `"structmember.h"`.

### Member flags

The following flags can be used with [`PyMemberDef.flags`](#c.PyMemberDef.flags "PyMemberDef.flags"):

Py\_READONLY
:   Not writable.

Py\_AUDIT\_READ
:   Emit an `object.__getattr__` [audit event](../library/audit_events.html#audit-events)
    before reading.

Py\_RELATIVE\_OFFSET
:   Indicates that the [`offset`](#c.PyMemberDef.offset "PyMemberDef.offset") of this `PyMemberDef`
    entry indicates an offset from the subclass-specific data, rather than
    from `PyObject`.

    Can only be used as part of [`Py_tp_members`](typeobj.html#c.PyTypeObject.tp_members "PyTypeObject.tp_members")
    [`slot`](type.html#c.PyType_Slot "PyType_Slot") when creating a class using negative
    [`basicsize`](type.html#c.PyType_Spec.basicsize "PyType_Spec.basicsize").
    It is mandatory in that case.

    This flag is only used in [`PyType_Slot`](type.html#c.PyType_Slot "PyType_Slot").
    When setting [`tp_members`](typeobj.html#c.PyTypeObject.tp_members "PyTypeObject.tp_members") during
    class creation, Python clears it and sets
    [`PyMemberDef.offset`](#c.PyMemberDef.offset "PyMemberDef.offset") to the offset from the `PyObject` struct.

Changed in version 3.10: The `RESTRICTED`, `READ_RESTRICTED` and
`WRITE_RESTRICTED` macros available with
`#include "structmember.h"` are deprecated.
`READ_RESTRICTED` and `RESTRICTED` are equivalent to
[`Py_AUDIT_READ`](#c.Py_AUDIT_READ "Py_AUDIT_READ"); `WRITE_RESTRICTED` does nothing.

Changed in version 3.12: The `READONLY` macro was renamed to [`Py_READONLY`](#c.Py_READONLY "Py_READONLY").
The `PY_AUDIT_READ` macro was renamed with the `Py_` prefix.
The new names are now always available.
Previously, these required `#include "structmember.h"`.
The header is still available and it provides the old names.

### Member types

[`PyMemberDef.type`](#c.PyMemberDef.type "PyMemberDef.type") can be one of the following macros corresponding
to various C types.
When the member is accessed in Python, it will be converted to the
equivalent Python type.
When it is set from Python, it will be converted back to the C type.
If that is not possible, an exception such as [`TypeError`](../library/exceptions.html#TypeError "TypeError") or
[`ValueError`](../library/exceptions.html#ValueError "ValueError") is raised.

Unless marked (D), attributes defined this way cannot be deleted
using e.g. [`del`](../reference/simple_stmts.html#del) or [`delattr()`](../library/functions.html#delattr "delattr").

| Macro name | C type | Python type |
| --- | --- | --- |
| Py\_T\_BYTE | char | [`int`](../library/functions.html#int "int") |
| Py\_T\_SHORT | short | [`int`](../library/functions.html#int "int") |
| Py\_T\_INT | int | [`int`](../library/functions.html#int "int") |
| Py\_T\_LONG | long | [`int`](../library/functions.html#int "int") |
| Py\_T\_LONGLONG | long long | [`int`](../library/functions.html#int "int") |
| Py\_T\_UBYTE | unsigned char | [`int`](../library/functions.html#int "int") |
| Py\_T\_UINT | unsigned int | [`int`](../library/functions.html#int "int") |
| Py\_T\_USHORT | unsigned short | [`int`](../library/functions.html#int "int") |
| Py\_T\_ULONG | unsigned long | [`int`](../library/functions.html#int "int") |
| Py\_T\_ULONGLONG | unsigned long long | [`int`](../library/functions.html#int "int") |
| Py\_T\_PYSSIZET | [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") | [`int`](../library/functions.html#int "int") |
| Py\_T\_FLOAT | float | [`float`](../library/functions.html#float "float") |
| Py\_T\_DOUBLE | double | [`float`](../library/functions.html#float "float") |
| Py\_T\_BOOL | char (written as 0 or 1) | [`bool`](../library/functions.html#bool "bool") |
| Py\_T\_STRING | const char\* (\*) | [`str`](../library/stdtypes.html#str "str") (RO) |
| Py\_T\_STRING\_INPLACE | const char[] (\*) | [`str`](../library/stdtypes.html#str "str") (RO) |
| Py\_T\_CHAR | char (0-127) | [`str`](../library/stdtypes.html#str "str") (\*\*) |
| Py\_T\_OBJECT\_EX | [PyObject](#c.PyObject "PyObject")\* | [`object`](../library/functions.html#object "object") (D) |

> (\*): Zero-terminated, UTF8-encoded C string.
> With `Py_T_STRING` the C representation is a pointer;
> with `Py_T_STRING_INPLACE` the string is stored directly
> in the structure.
>
> (\*\*): String of length 1. Only ASCII is accepted.
>
> (RO): Implies [`Py_READONLY`](#c.Py_READONLY "Py_READONLY").
>
> (D): Can be deleted, in which case the pointer is set to `NULL`.
> Reading a `NULL` pointer raises [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError").

Added in version 3.12: In previous versions, the macros were only available with
`#include "structmember.h"` and were named without the `Py_` prefix
(e.g. as `T_INT`).
The header is still available and contains the old names, along with
the following deprecated types:

T\_OBJECT
:   Like `Py_T_OBJECT_EX`, but `NULL` is converted to `None`.
    This results in surprising behavior in Python: deleting the attribute
    effectively sets it to `None`.

T\_NONE
:   Always `None`. Must be used with [`Py_READONLY`](#c.Py_READONLY "Py_READONLY").

### Defining Getters and Setters

type PyGetSetDef
:   *Part of the [Stable ABI](stable.html#stable) (including all members).*

    Structure to define property-like access for a type. See also description of
    the [`PyTypeObject.tp_getset`](typeobj.html#c.PyTypeObject.tp_getset "PyTypeObject.tp_getset") slot.

    const char \*name
    :   attribute name

    [getter](#c.getter "getter") get
    :   C function to get the attribute.

    [setter](#c.setter "setter") set
    :   Optional C function to set or delete the attribute.
        If `NULL`, the attribute is read-only.

    const char \*doc
    :   optional docstring

    void \*closure
    :   Optional user data pointer, providing additional data for getter and setter.

typedef [PyObject](#c.PyObject "PyObject") \*(\*getter)([PyObject](#c.PyObject "PyObject")\*, void\*)
:   *Part of the [Stable ABI](stable.html#stable).*

    The `get` function takes one [PyObject](#c.PyObject "PyObject")\* parameter (the
    instance) and a user data pointer (the associated `closure`):

    It should return a new reference on success or `NULL` with a set exception
    on failure.

typedef int (\*setter)([PyObject](#c.PyObject "PyObject")\*, [PyObject](#c.PyObject "PyObject")\*, void\*)
:   *Part of the [Stable ABI](stable.html#stable).*

    `set` functions take two [PyObject](#c.PyObject "PyObject")\* parameters (the instance and
    the value to be set) and a user data pointer (the associated `closure`):

    In case the attribute should be deleted the second parameter is `NULL`.
    Should return `0` on success or `-1` with a set exception on failure.