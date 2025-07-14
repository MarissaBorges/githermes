Set Objects
===========

This section details the public API for [`set`](../library/stdtypes.html#set "set") and [`frozenset`](../library/stdtypes.html#frozenset "frozenset")
objects. Any functionality not listed below is best accessed using either
the abstract object protocol (including [`PyObject_CallMethod()`](call.html#c.PyObject_CallMethod "PyObject_CallMethod"),
[`PyObject_RichCompareBool()`](object.html#c.PyObject_RichCompareBool "PyObject_RichCompareBool"), [`PyObject_Hash()`](object.html#c.PyObject_Hash "PyObject_Hash"),
[`PyObject_Repr()`](object.html#c.PyObject_Repr "PyObject_Repr"), [`PyObject_IsTrue()`](object.html#c.PyObject_IsTrue "PyObject_IsTrue"), [`PyObject_Print()`](object.html#c.PyObject_Print "PyObject_Print"), and
[`PyObject_GetIter()`](object.html#c.PyObject_GetIter "PyObject_GetIter")) or the abstract number protocol (including
[`PyNumber_And()`](number.html#c.PyNumber_And "PyNumber_And"), [`PyNumber_Subtract()`](number.html#c.PyNumber_Subtract "PyNumber_Subtract"), [`PyNumber_Or()`](number.html#c.PyNumber_Or "PyNumber_Or"),
[`PyNumber_Xor()`](number.html#c.PyNumber_Xor "PyNumber_Xor"), [`PyNumber_InPlaceAnd()`](number.html#c.PyNumber_InPlaceAnd "PyNumber_InPlaceAnd"),
[`PyNumber_InPlaceSubtract()`](number.html#c.PyNumber_InPlaceSubtract "PyNumber_InPlaceSubtract"), [`PyNumber_InPlaceOr()`](number.html#c.PyNumber_InPlaceOr "PyNumber_InPlaceOr"), and
[`PyNumber_InPlaceXor()`](number.html#c.PyNumber_InPlaceXor "PyNumber_InPlaceXor")).

type PySetObject
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") is used to hold the internal data for both
    [`set`](../library/stdtypes.html#set "set") and [`frozenset`](../library/stdtypes.html#frozenset "frozenset") objects. It is like a [`PyDictObject`](dict.html#c.PyDictObject "PyDictObject")
    in that it is a fixed size for small sets (much like tuple storage) and will
    point to a separate, variable sized block of memory for medium and large sized
    sets (much like list storage). None of the fields of this structure should be
    considered public and all are subject to change. All access should be done through
    the documented API rather than by manipulating the values in the structure.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PySet\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This is an instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") representing the Python
    [`set`](../library/stdtypes.html#set "set") type.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyFrozenSet\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This is an instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") representing the Python
    [`frozenset`](../library/stdtypes.html#frozenset "frozenset") type.

The following type check macros work on pointers to any Python object. Likewise,
the constructor functions work with any iterable Python object.

int PySet\_Check([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`set`](../library/stdtypes.html#set "set") object or an instance of a subtype.
    This function always succeeds.

int PyFrozenSet\_Check([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`frozenset`](../library/stdtypes.html#frozenset "frozenset") object or an instance of a
    subtype. This function always succeeds.

int PyAnySet\_Check([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`set`](../library/stdtypes.html#set "set") object, a [`frozenset`](../library/stdtypes.html#frozenset "frozenset") object, or an
    instance of a subtype. This function always succeeds.

int PySet\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`set`](../library/stdtypes.html#set "set") object but not an instance of a
    subtype. This function always succeeds.

int PyAnySet\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`set`](../library/stdtypes.html#set "set") object or a [`frozenset`](../library/stdtypes.html#frozenset "frozenset") object but
    not an instance of a subtype. This function always succeeds.

int PyFrozenSet\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if *p* is a [`frozenset`](../library/stdtypes.html#frozenset "frozenset") object but not an instance of a
    subtype. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PySet\_New([PyObject](structures.html#c.PyObject "PyObject") \*iterable)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new [`set`](../library/stdtypes.html#set "set") containing objects returned by the *iterable*. The
    *iterable* may be `NULL` to create a new empty set. Return the new set on
    success or `NULL` on failure. Raise [`TypeError`](../library/exceptions.html#TypeError "TypeError") if *iterable* is not
    actually iterable. The constructor is also useful for copying a set
    (`c=set(s)`).

[PyObject](structures.html#c.PyObject "PyObject") \*PyFrozenSet\_New([PyObject](structures.html#c.PyObject "PyObject") \*iterable)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new [`frozenset`](../library/stdtypes.html#frozenset "frozenset") containing objects returned by the *iterable*.
    The *iterable* may be `NULL` to create a new empty frozenset. Return the new
    set on success or `NULL` on failure. Raise [`TypeError`](../library/exceptions.html#TypeError "TypeError") if *iterable* is
    not actually iterable.

The following functions and macros are available for instances of [`set`](../library/stdtypes.html#set "set")
or [`frozenset`](../library/stdtypes.html#frozenset "frozenset") or instances of their subtypes.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PySet\_Size([PyObject](structures.html#c.PyObject "PyObject") \*anyset)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the length of a [`set`](../library/stdtypes.html#set "set") or [`frozenset`](../library/stdtypes.html#frozenset "frozenset") object. Equivalent to
    `len(anyset)`. Raises a [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *anyset* is not a
    [`set`](../library/stdtypes.html#set "set"), [`frozenset`](../library/stdtypes.html#frozenset "frozenset"), or an instance of a subtype.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PySet\_GET\_SIZE([PyObject](structures.html#c.PyObject "PyObject") \*anyset)
:   Macro form of [`PySet_Size()`](#c.PySet_Size "PySet_Size") without error checking.

int PySet\_Contains([PyObject](structures.html#c.PyObject "PyObject") \*anyset, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return `1` if found, `0` if not found, and `-1` if an error is encountered. Unlike
    the Python [`__contains__()`](../reference/datamodel.html#object.__contains__ "object.__contains__") method, this function does not automatically
    convert unhashable sets into temporary frozensets. Raise a [`TypeError`](../library/exceptions.html#TypeError "TypeError") if
    the *key* is unhashable. Raise [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *anyset* is not a
    [`set`](../library/stdtypes.html#set "set"), [`frozenset`](../library/stdtypes.html#frozenset "frozenset"), or an instance of a subtype.

int PySet\_Add([PyObject](structures.html#c.PyObject "PyObject") \*set, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   *Part of the [Stable ABI](stable.html#stable).*

    Add *key* to a [`set`](../library/stdtypes.html#set "set") instance. Also works with [`frozenset`](../library/stdtypes.html#frozenset "frozenset")
    instances (like [`PyTuple_SetItem()`](tuple.html#c.PyTuple_SetItem "PyTuple_SetItem") it can be used to fill in the values
    of brand new frozensets before they are exposed to other code). Return `0` on
    success or `-1` on failure. Raise a [`TypeError`](../library/exceptions.html#TypeError "TypeError") if the *key* is
    unhashable. Raise a [`MemoryError`](../library/exceptions.html#MemoryError "MemoryError") if there is no room to grow. Raise a
    [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *set* is not an instance of [`set`](../library/stdtypes.html#set "set") or its
    subtype.

The following functions are available for instances of [`set`](../library/stdtypes.html#set "set") or its
subtypes but not for instances of [`frozenset`](../library/stdtypes.html#frozenset "frozenset") or its subtypes.

int PySet\_Discard([PyObject](structures.html#c.PyObject "PyObject") \*set, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return `1` if found and removed, `0` if not found (no action taken), and `-1` if an
    error is encountered. Does not raise [`KeyError`](../library/exceptions.html#KeyError "KeyError") for missing keys. Raise a
    [`TypeError`](../library/exceptions.html#TypeError "TypeError") if the *key* is unhashable. Unlike the Python [`discard()`](../library/stdtypes.html#frozenset.discard "frozenset.discard")
    method, this function does not automatically convert unhashable sets into
    temporary frozensets. Raise [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *set* is not an
    instance of [`set`](../library/stdtypes.html#set "set") or its subtype.

[PyObject](structures.html#c.PyObject "PyObject") \*PySet\_Pop([PyObject](structures.html#c.PyObject "PyObject") \*set)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new reference to an arbitrary object in the *set*, and removes the
    object from the *set*. Return `NULL` on failure. Raise [`KeyError`](../library/exceptions.html#KeyError "KeyError") if the
    set is empty. Raise a [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *set* is not an instance of
    [`set`](../library/stdtypes.html#set "set") or its subtype.

int PySet\_Clear([PyObject](structures.html#c.PyObject "PyObject") \*set)
:   *Part of the [Stable ABI](stable.html#stable).*

    Empty an existing set of all elements. Return `0` on
    success. Return `-1` and raise [`SystemError`](../library/exceptions.html#SystemError "SystemError") if *set* is not an instance of
    [`set`](../library/stdtypes.html#set "set") or its subtype.