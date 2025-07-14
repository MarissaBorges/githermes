:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the sequence or iterable *o* as an object usable by the other
    `PySequence_Fast*` family of functions. If the object is not a sequence or
    iterable, raises [`TypeError`](../library/exceptions.html#TypeError "TypeError") with *m* as the message text. Returns
    `NULL` on failure.

    The `PySequence_Fast*` functions are thus named because they assume
    *o* is a [`PyTupleObject`](tuple.html#c.PyTupleObject "PyTupleObject") or a [`PyListObject`](list.html#c.PyListObject "PyListObject") and access
    the data fields of *o* directly.

    As a CPython implementation detail, if *o* is already a sequence or list, it
    will be returned.