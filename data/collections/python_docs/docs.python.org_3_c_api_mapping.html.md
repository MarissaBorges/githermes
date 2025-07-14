Mapping Protocol
================

See also [`PyObject_GetItem()`](object.html#c.PyObject_GetItem "PyObject_GetItem"), [`PyObject_SetItem()`](object.html#c.PyObject_SetItem "PyObject_SetItem") and
[`PyObject_DelItem()`](object.html#c.PyObject_DelItem "PyObject_DelItem").

int PyMapping\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return `1` if the object provides the mapping protocol or supports slicing,
    and `0` otherwise. Note that it returns `1` for Python classes with
    a [`__getitem__()`](../reference/datamodel.html#object.__getitem__ "object.__getitem__") method, since in general it is impossible to
    determine what type of keys the class supports. This function always succeeds.

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyMapping\_Size([PyObject](structures.html#c.PyObject "PyObject") \*o)

[Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") PyMapping\_Length([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable).*

    Returns the number of keys in object *o* on success, and `-1` on failure.
    This is equivalent to the Python expression `len(o)`.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMapping\_GetItemString([PyObject](structures.html#c.PyObject "PyObject") \*o, const char \*key)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    This is the same as [`PyObject_GetItem()`](object.html#c.PyObject_GetItem "PyObject_GetItem"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

int PyMapping\_GetOptionalItem([PyObject](structures.html#c.PyObject "PyObject") \*obj, [PyObject](structures.html#c.PyObject "PyObject") \*key, [PyObject](structures.html#c.PyObject "PyObject") \*\*result)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Variant of [`PyObject_GetItem()`](object.html#c.PyObject_GetItem "PyObject_GetItem") which doesn’t raise
    [`KeyError`](../library/exceptions.html#KeyError "KeyError") if the key is not found.

    If the key is found, return `1` and set *\*result* to a new
    [strong reference](../glossary.html#term-strong-reference) to the corresponding value.
    If the key is not found, return `0` and set *\*result* to `NULL`;
    the [`KeyError`](../library/exceptions.html#KeyError "KeyError") is silenced.
    If an error other than [`KeyError`](../library/exceptions.html#KeyError "KeyError") is raised, return `-1` and
    set *\*result* to `NULL`.

int PyMapping\_GetOptionalItemString([PyObject](structures.html#c.PyObject "PyObject") \*obj, const char \*key, [PyObject](structures.html#c.PyObject "PyObject") \*\*result)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    This is the same as [`PyMapping_GetOptionalItem()`](#c.PyMapping_GetOptionalItem "PyMapping_GetOptionalItem"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

int PyMapping\_SetItemString([PyObject](structures.html#c.PyObject "PyObject") \*o, const char \*key, [PyObject](structures.html#c.PyObject "PyObject") \*v)
:   *Part of the [Stable ABI](stable.html#stable).*

    This is the same as [`PyObject_SetItem()`](object.html#c.PyObject_SetItem "PyObject_SetItem"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

int PyMapping\_DelItem([PyObject](structures.html#c.PyObject "PyObject") \*o, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   This is an alias of [`PyObject_DelItem()`](object.html#c.PyObject_DelItem "PyObject_DelItem").

int PyMapping\_DelItemString([PyObject](structures.html#c.PyObject "PyObject") \*o, const char \*key)
:   This is the same as [`PyObject_DelItem()`](object.html#c.PyObject_DelItem "PyObject_DelItem"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

int PyMapping\_HasKeyWithError([PyObject](structures.html#c.PyObject "PyObject") \*o, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Return `1` if the mapping object has the key *key* and `0` otherwise.
    This is equivalent to the Python expression `key in o`.
    On failure, return `-1`.

int PyMapping\_HasKeyStringWithError([PyObject](structures.html#c.PyObject "PyObject") \*o, const char \*key)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    This is the same as [`PyMapping_HasKeyWithError()`](#c.PyMapping_HasKeyWithError "PyMapping_HasKeyWithError"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

int PyMapping\_HasKey([PyObject](structures.html#c.PyObject "PyObject") \*o, [PyObject](structures.html#c.PyObject "PyObject") \*key)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return `1` if the mapping object has the key *key* and `0` otherwise.
    This is equivalent to the Python expression `key in o`.
    This function always succeeds.

int PyMapping\_HasKeyString([PyObject](structures.html#c.PyObject "PyObject") \*o, const char \*key)
:   *Part of the [Stable ABI](stable.html#stable).*

    This is the same as [`PyMapping_HasKey()`](#c.PyMapping_HasKey "PyMapping_HasKey"), but *key* is
    specified as a const char\* UTF-8 encoded bytes string,
    rather than a [PyObject](structures.html#c.PyObject "PyObject")\*.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMapping\_Keys([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    On success, return a list of the keys in object *o*. On failure, return
    `NULL`.

    Changed in version 3.7: Previously, the function returned a list or a tuple.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMapping\_Values([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    On success, return a list of the values in object *o*. On failure, return
    `NULL`.

    Changed in version 3.7: Previously, the function returned a list or a tuple.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMapping\_Items([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    On success, return a list of the items in object *o*, where each item is a
    tuple containing a key-value pair. On failure, return `NULL`.

    Changed in version 3.7: Previously, the function returned a list or a tuple.