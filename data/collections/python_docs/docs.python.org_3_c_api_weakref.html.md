Weak Reference Objects
======================

Python supports *weak references* as first-class objects. There are two
specific object types which directly implement weak references. The first is a
simple reference object, and the second acts as a proxy for the original object
as much as it can.

int PyWeakref\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return non-zero if *ob* is either a reference or proxy object. This function
    always succeeds.

int PyWeakref\_CheckRef([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return non-zero if *ob* is a reference object. This function always succeeds.

int PyWeakref\_CheckProxy([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return non-zero if *ob* is a proxy object. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyWeakref\_NewRef([PyObject](structures.html#c.PyObject "PyObject") \*ob, [PyObject](structures.html#c.PyObject "PyObject") \*callback)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a weak reference object for the object *ob*. This will always return
    a new reference, but is not guaranteed to create a new object; an existing
    reference object may be returned. The second parameter, *callback*, can be a
    callable object that receives notification when *ob* is garbage collected; it
    should accept a single parameter, which will be the weak reference object
    itself. *callback* may also be `None` or `NULL`. If *ob* is not a
    weakly referenceable object, or if *callback* is not callable, `None`, or
    `NULL`, this will return `NULL` and raise [`TypeError`](../library/exceptions.html#TypeError "TypeError").

[PyObject](structures.html#c.PyObject "PyObject") \*PyWeakref\_NewProxy([PyObject](structures.html#c.PyObject "PyObject") \*ob, [PyObject](structures.html#c.PyObject "PyObject") \*callback)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a weak reference proxy object for the object *ob*. This will always
    return a new reference, but is not guaranteed to create a new object; an
    existing proxy object may be returned. The second parameter, *callback*, can
    be a callable object that receives notification when *ob* is garbage
    collected; it should accept a single parameter, which will be the weak
    reference object itself. *callback* may also be `None` or `NULL`. If *ob*
    is not a weakly referenceable object, or if *callback* is not callable,
    `None`, or `NULL`, this will return `NULL` and raise [`TypeError`](../library/exceptions.html#TypeError "TypeError").

int PyWeakref\_GetRef([PyObject](structures.html#c.PyObject "PyObject") \*ref, [PyObject](structures.html#c.PyObject "PyObject") \*\*pobj)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Get a [strong reference](../glossary.html#term-strong-reference) to the referenced object from a weak
    reference, *ref*, into *\*pobj*.

    * On success, set *\*pobj* to a new [strong reference](../glossary.html#term-strong-reference) to the
      referenced object and return 1.
    * If the reference is dead, set *\*pobj* to `NULL` and return 0.
    * On error, raise an exception and return -1.

[PyObject](structures.html#c.PyObject "PyObject") \*PyWeakref\_GetObject([PyObject](structures.html#c.PyObject "PyObject") \*ref)
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a [borrowed reference](../glossary.html#term-borrowed-reference) to the referenced object from a weak
    reference, *ref*. If the referent is no longer live, returns `Py_None`.

    Note

    This function returns a [borrowed reference](../glossary.html#term-borrowed-reference) to the referenced object.
    This means that you should always call [`Py_INCREF()`](refcounting.html#c.Py_INCREF "Py_INCREF") on the object
    except when it cannot be destroyed before the last usage of the borrowed
    reference.

    Deprecated since version 3.13, will be removed in version 3.15: Use [`PyWeakref_GetRef()`](#c.PyWeakref_GetRef "PyWeakref_GetRef") instead.

[PyObject](structures.html#c.PyObject "PyObject") \*PyWeakref\_GET\_OBJECT([PyObject](structures.html#c.PyObject "PyObject") \*ref)
:   *Return value: Borrowed reference.*

    Similar to [`PyWeakref_GetObject()`](#c.PyWeakref_GetObject "PyWeakref_GetObject"), but does no error checking.

    Deprecated since version 3.13, will be removed in version 3.15: Use [`PyWeakref_GetRef()`](#c.PyWeakref_GetRef "PyWeakref_GetRef") instead.

void PyObject\_ClearWeakRefs([PyObject](structures.html#c.PyObject "PyObject") \*object)
:   *Part of the [Stable ABI](stable.html#stable).*

    This function is called by the [`tp_dealloc`](typeobj.html#c.PyTypeObject.tp_dealloc "PyTypeObject.tp_dealloc") handler
    to clear weak references.

    This iterates through the weak references for *object* and calls callbacks
    for those references which have one. It returns when all callbacks have
    been attempted.

void PyUnstable\_Object\_ClearWeakRefsNoCallbacks([PyObject](structures.html#c.PyObject "PyObject") \*object)
:   *This is [Unstable API](stable.html#unstable-c-api). It may change without warning in minor releases.*

    Clears the weakrefs for *object* without calling the callbacks.

    This function is called by the [`tp_dealloc`](typeobj.html#c.PyTypeObject.tp_dealloc "PyTypeObject.tp_dealloc") handler
    for types with finalizers (i.e., [`__del__()`](../reference/datamodel.html#object.__del__ "object.__del__")). The handler for
    those objects first calls [`PyObject_ClearWeakRefs()`](#c.PyObject_ClearWeakRefs "PyObject_ClearWeakRefs") to clear weakrefs
    and call their callbacks, then the finalizer, and finally this function to
    clear any weakrefs that may have been created by the finalizer.

    In most circumstances, it’s more appropriate to use
    [`PyObject_ClearWeakRefs()`](#c.PyObject_ClearWeakRefs "PyObject_ClearWeakRefs") to clear weakrefs instead of this function.