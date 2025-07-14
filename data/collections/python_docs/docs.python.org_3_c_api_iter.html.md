Iterator Protocol
=================

There are two functions specifically for working with iterators.

int PyIter\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.8.*

    Return non-zero if the object *o* can be safely passed to
    [`PyIter_Next()`](#c.PyIter_Next "PyIter_Next"), and `0` otherwise. This function always succeeds.

int PyAIter\_Check([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Return non-zero if the object *o* provides the `AsyncIterator`
    protocol, and `0` otherwise. This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyIter\_Next([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the next value from the iterator *o*. The object must be an iterator
    according to [`PyIter_Check()`](#c.PyIter_Check "PyIter_Check") (it is up to the caller to check this).
    If there are no remaining values, returns `NULL` with no exception set.
    If an error occurs while retrieving the item, returns `NULL` and passes
    along the exception.

To write a loop which iterates over an iterator, the C code should look
something like this:

```
PyObject *iterator = PyObject_GetIter(obj);
PyObject *item;

if (iterator == NULL) {
    /* propagate error */
}

while ((item = PyIter_Next(iterator))) {
    /* do something with item */
    ...
    /* release reference when done */
    Py_DECREF(item);
}

Py_DECREF(iterator);

if (PyErr_Occurred()) {
    /* propagate error */
}
else {
    /* continue doing useful work */
}

```

type PySendResult
:   The enum value used to represent different results of [`PyIter_Send()`](#c.PyIter_Send "PyIter_Send").

[PySendResult](#c.PySendResult "PySendResult") PyIter\_Send([PyObject](structures.html#c.PyObject "PyObject") \*iter, [PyObject](structures.html#c.PyObject "PyObject") \*arg, [PyObject](structures.html#c.PyObject "PyObject") \*\*presult)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.10.*

    Sends the *arg* value into the iterator *iter*. Returns:

    * `PYGEN_RETURN` if iterator returns. Return value is returned via *presult*.
    * `PYGEN_NEXT` if iterator yields. Yielded value is returned via *presult*.
    * `PYGEN_ERROR` if iterator has raised and exception. *presult* is set to `NULL`.