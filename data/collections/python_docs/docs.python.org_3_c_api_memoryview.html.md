MemoryView objects
==================

A [`memoryview`](../library/stdtypes.html#memoryview "memoryview") object exposes the C level [buffer interface](buffer.html#bufferobjects) as a Python object which can then be passed around like
any other object.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMemoryView\_FromObject([PyObject](structures.html#c.PyObject "PyObject") \*obj)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Create a memoryview object from an object that provides the buffer interface.
    If *obj* supports writable buffer exports, the memoryview object will be
    read/write, otherwise it may be either read-only or read/write at the
    discretion of the exporter.

PyBUF\_READ
:   Flag to request a readonly buffer.

PyBUF\_WRITE
:   Flag to request a writable buffer.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMemoryView\_FromMemory(char \*mem, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") size, int flags)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.7.*

    Create a memoryview object using *mem* as the underlying buffer.
    *flags* can be one of [`PyBUF_READ`](#c.PyBUF_READ "PyBUF_READ") or [`PyBUF_WRITE`](#c.PyBUF_WRITE "PyBUF_WRITE").

[PyObject](structures.html#c.PyObject "PyObject") \*PyMemoryView\_FromBuffer(const [Py\_buffer](buffer.html#c.Py_buffer "Py_buffer") \*view)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.11.*

    Create a memoryview object wrapping the given buffer structure *view*.
    For simple byte buffers, [`PyMemoryView_FromMemory()`](#c.PyMemoryView_FromMemory "PyMemoryView_FromMemory") is the preferred
    function.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMemoryView\_GetContiguous([PyObject](structures.html#c.PyObject "PyObject") \*obj, int buffertype, char order)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Create a memoryview object to a [contiguous](../glossary.html#term-contiguous) chunk of memory (in either
    ‘C’ or ‘F’ortran *order*) from an object that defines the buffer
    interface. If memory is contiguous, the memoryview object points to the
    original memory. Otherwise, a copy is made and the memoryview points to a
    new bytes object.

    *buffertype* can be one of [`PyBUF_READ`](#c.PyBUF_READ "PyBUF_READ") or [`PyBUF_WRITE`](#c.PyBUF_WRITE "PyBUF_WRITE").

int PyMemoryView\_Check([PyObject](structures.html#c.PyObject "PyObject") \*obj)
:   Return true if the object *obj* is a memoryview object. It is not
    currently allowed to create subclasses of [`memoryview`](../library/stdtypes.html#memoryview "memoryview"). This
    function always succeeds.

[Py\_buffer](buffer.html#c.Py_buffer "Py_buffer") \*PyMemoryView\_GET\_BUFFER([PyObject](structures.html#c.PyObject "PyObject") \*mview)
:   Return a pointer to the memoryview’s private copy of the exporter’s buffer.
    *mview* **must** be a memoryview instance; this macro doesn’t check its type,
    you must do it yourself or you will risk crashes.

[PyObject](structures.html#c.PyObject "PyObject") \*PyMemoryView\_GET\_BASE([PyObject](structures.html#c.PyObject "PyObject") \*mview)
:   Return either a pointer to the exporting object that the memoryview is based
    on or `NULL` if the memoryview has been created by one of the functions
    [`PyMemoryView_FromMemory()`](#c.PyMemoryView_FromMemory "PyMemoryView_FromMemory") or [`PyMemoryView_FromBuffer()`](#c.PyMemoryView_FromBuffer "PyMemoryView_FromBuffer").
    *mview* **must** be a memoryview instance.