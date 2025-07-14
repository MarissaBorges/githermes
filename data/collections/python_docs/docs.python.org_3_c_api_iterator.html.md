Iterator Objects
================

Python provides two general-purpose iterator objects. The first, a sequence
iterator, works with an arbitrary sequence supporting the [`__getitem__()`](../reference/datamodel.html#object.__getitem__ "object.__getitem__")
method. The second works with a callable object and a sentinel value, calling
the callable for each item in the sequence, and ending the iteration when the
sentinel value is returned.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PySeqIter\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    Type object for iterator objects returned by [`PySeqIter_New()`](#c.PySeqIter_New "PySeqIter_New") and the
    one-argument form of the [`iter()`](../library/functions.html#iter "iter") built-in function for built-in sequence
    types.

int PySeqIter\_Check([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   Return true if the type of *op* is [`PySeqIter_Type`](#c.PySeqIter_Type "PySeqIter_Type"). This function
    always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PySeqIter\_New([PyObject](structures.html#c.PyObject "PyObject") \*seq)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return an iterator that works with a general sequence object, *seq*. The
    iteration ends when the sequence raises [`IndexError`](../library/exceptions.html#IndexError "IndexError") for the subscripting
    operation.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyCallIter\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    Type object for iterator objects returned by [`PyCallIter_New()`](#c.PyCallIter_New "PyCallIter_New") and the
    two-argument form of the [`iter()`](../library/functions.html#iter "iter") built-in function.

int PyCallIter\_Check([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   Return true if the type of *op* is [`PyCallIter_Type`](#c.PyCallIter_Type "PyCallIter_Type"). This
    function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyCallIter\_New([PyObject](structures.html#c.PyObject "PyObject") \*callable, [PyObject](structures.html#c.PyObject "PyObject") \*sentinel)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new iterator. The first parameter, *callable*, can be any Python
    callable object that can be called with no parameters; each call to it should
    return the next item in the iteration. When *callable* returns a value equal to
    *sentinel*, the iteration will be terminated.