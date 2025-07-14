Note

On Python 3.12 and older, the macro `PY_SSIZE_T_CLEAN` must be
defined before including `Python.h` to use all `#` variants of
formats (`s#`, `y#`, etc.) explained below.
This is not necessary on Python 3.13 and later.

These formats allow accessing an object as a contiguous chunk of memory.
You don’t have to provide raw storage for the returned unicode or bytes
area.

Unless otherwise stated, buffers are not NUL-terminated.

* Formats such as `y*` and `s*` fill a [`Py_buffer`](buffer.html#c.Py_buffer "Py_buffer") structure.
  This locks the underlying buffer so that the caller can subsequently use
  the buffer even inside a [`Py_BEGIN_ALLOW_THREADS`](init.html#c.Py_BEGIN_ALLOW_THREADS "Py_BEGIN_ALLOW_THREADS")
  block without the risk of mutable data being resized or destroyed.
  As a result, **you have to call** [`PyBuffer_Release()`](buffer.html#c.PyBuffer_Release "PyBuffer_Release") after you have
  finished processing the data (or in any early abort case).
* The `es`, `es#`, `et` and `et#` formats allocate the result buffer.
  **You have to call** [`PyMem_Free()`](memory.html#c.PyMem_Free "PyMem_Free") after you have finished
  processing the data (or in any early abort case).
* Other formats take a [`str`](../library/stdtypes.html#str "str") or a read-only [bytes-like object](../glossary.html#term-bytes-like-object),
  such as [`bytes`](../library/stdtypes.html#bytes "bytes"), and provide a `const char *` pointer to
  its buffer.
  In this case the buffer is “borrowed”: it is managed by the corresponding
  Python object, and shares the lifetime of this object.
  You won’t have to release any memory yourself.

  To ensure that the underlying buffer may be safely borrowed, the object’s
  [`PyBufferProcs.bf_releasebuffer`](typeobj.html#c.PyBufferProcs.bf_releasebuffer "PyBufferProcs.bf_releasebuffer") field must be `NULL`.
  This disallows common mutable objects such as [`bytearray`](../library/stdtypes.html#bytearray "bytearray"),
  but also some read-only objects such as [`memoryview`](../library/stdtypes.html#memoryview "memoryview") of
  [`bytes`](../library/stdtypes.html#bytes "bytes").

  Besides this `bf_releasebuffer` requirement, there is no check to verify
  whether the input object is immutable (e.g. whether it would honor a request
  for a writable buffer, or whether another thread can mutate the data).

`s` ([`str`](../library/stdtypes.html#str "str")) [const char \*]
:   Convert a Unicode object to a C pointer to a character string.
    A pointer to an existing string is stored in the character pointer
    variable whose address you pass. The C string is NUL-terminated.
    The Python string must not contain embedded null code points; if it does,
    a [`ValueError`](../library/exceptions.html#ValueError "ValueError") exception is raised. Unicode objects are converted
    to C strings using `'utf-8'` encoding. If this conversion fails, a
    [`UnicodeError`](../library/exceptions.html#UnicodeError "UnicodeError") is raised.

    Note

    This format does not accept [bytes-like objects](../glossary.html#term-bytes-like-object). If you want to accept
    filesystem paths and convert them to C character strings, it is
    preferable to use the `O&` format with [`PyUnicode_FSConverter()`](unicode.html#c.PyUnicode_FSConverter "PyUnicode_FSConverter")
    as *converter*.

    Changed in version 3.5: Previously, [`TypeError`](../library/exceptions.html#TypeError "TypeError") was raised when embedded null code points
    were encountered in the Python string.

`s*` ([`str`](../library/stdtypes.html#str "str") or [bytes-like object](../glossary.html#term-bytes-like-object)) [Py\_buffer]
:   This format accepts Unicode objects as well as bytes-like objects.
    It fills a [`Py_buffer`](buffer.html#c.Py_buffer "Py_buffer") structure provided by the caller.
    In this case the resulting C string may contain embedded NUL bytes.
    Unicode objects are converted to C strings using `'utf-8'` encoding.

`s#` ([`str`](../library/stdtypes.html#str "str"), read-only [bytes-like object](../glossary.html#term-bytes-like-object)) [const char \*, [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t")]
:   Like `s*`, except that it provides a [borrowed buffer](#c-arg-borrowed-buffer).
    The result is stored into two C variables,
    the first one a pointer to a C string, the second one its length.
    The string may contain embedded null bytes. Unicode objects are converted
    to C strings using `'utf-8'` encoding.

`z` ([`str`](../library/stdtypes.html#str "str") or `None`) [const char \*]
:   Like `s`, but the Python object may also be `None`, in which case the C
    pointer is set to `NULL`.

`z*` ([`str`](../library/stdtypes.html#str "str"), [bytes-like object](../glossary.html#term-bytes-like-object) or `None`) [Py\_buffer]
:   Like `s*`, but the Python object may also be `None`, in which case the
    `buf` member of the [`Py_buffer`](buffer.html#c.Py_buffer "Py_buffer") structure is set to `NULL`.

`z#` ([`str`](../library/stdtypes.html#str "str"), read-only [bytes-like object](../glossary.html#term-bytes-like-object) or `None`) [const char \*, [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t")]
:   Like `s#`, but the Python object may also be `None`, in which case the C
    pointer is set to `NULL`.

`y` (read-only [bytes-like object](../glossary.html#term-bytes-like-object)) [const char \*]
:   This format converts a bytes-like object to a C pointer to a
    [borrowed](#c-arg-borrowed-buffer) character string;
    it does not accept Unicode objects. The bytes buffer must not
    contain embedded null bytes; if it does, a [`ValueError`](../library/exceptions.html#ValueError "ValueError")
    exception is raised.

    Changed in version 3.5: Previously, [`TypeError`](../library/exceptions.html#TypeError "TypeError") was raised when embedded null bytes were
    encountered in the bytes buffer.

`y*` ([bytes-like object](../glossary.html#term-bytes-like-object)) [Py\_buffer]
:   This variant on `s*` doesn’t accept Unicode objects, only
    bytes-like objects. **This is the recommended way to accept
    binary data.**

`y#` (read-only [bytes-like object](../glossary.html#term-bytes-like-object)) [const char \*, [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t")]
:   This variant on `s#` doesn’t accept Unicode objects, only bytes-like
    objects.

`S` ([`bytes`](../library/stdtypes.html#bytes "bytes")) [PyBytesObject \*]
:   Requires that the Python object is a [`bytes`](../library/stdtypes.html#bytes "bytes") object, without
    attempting any conversion. Raises [`TypeError`](../library/exceptions.html#TypeError "TypeError") if the object is not
    a bytes object. The C variable may also be declared as [PyObject](structures.html#c.PyObject "PyObject")\*.

`Y` ([`bytearray`](../library/stdtypes.html#bytearray "bytearray")) [PyByteArrayObject \*]
:   Requires that the Python object is a [`bytearray`](../library/stdtypes.html#bytearray "bytearray") object, without
    attempting any conversion. Raises [`TypeError`](../library/exceptions.html#TypeError "TypeError") if the object is not
    a [`bytearray`](../library/stdtypes.html#bytearray "bytearray") object. The C variable may also be declared as [PyObject](structures.html#c.PyObject "PyObject")\*.

`U` ([`str`](../library/stdtypes.html#str "str")) [PyObject \*]
:   Requires that the Python object is a Unicode object, without attempting
    any conversion. Raises [`TypeError`](../library/exceptions.html#TypeError "TypeError") if the object is not a Unicode
    object. The C variable may also be declared as [PyObject](structures.html#c.PyObject "PyObject")\*.

`w*` (read-write [bytes-like object](../glossary.html#term-bytes-like-object)) [Py\_buffer]
:   This format accepts any object which implements the read-write buffer
    interface. It fills a [`Py_buffer`](buffer.html#c.Py_buffer "Py_buffer") structure provided by the caller.
    The buffer may contain embedded null bytes. The caller have to call
    [`PyBuffer_Release()`](buffer.html#c.PyBuffer_Release "PyBuffer_Release") when it is done with the buffer.

`es` ([`str`](../library/stdtypes.html#str "str")) [const char \*encoding, char \*\*buffer]
:   This variant on `s` is used for encoding Unicode into a character buffer.
    It only works for encoded data without embedded NUL bytes.

    This format requires two arguments. The first is only used as input, and
    must be a const char\* which points to the name of an encoding as a
    NUL-terminated string, or `NULL`, in which case `'utf-8'` encoding is used.
    An exception is raised if the named encoding is not known to Python. The
    second argument must be a char\*\*; the value of the pointer it
    references will be set to a buffer with the contents of the argument text.
    The text will be encoded in the encoding specified by the first argument.

    [`PyArg_ParseTuple()`](#c.PyArg_ParseTuple "PyArg_ParseTuple") will allocate a buffer of the needed size, copy the
    encoded data into this buffer and adjust *\*buffer* to reference the newly
    allocated storage. The caller is responsible for calling [`PyMem_Free()`](memory.html#c.PyMem_Free "PyMem_Free") to
    free the allocated buffer after use.

`et` ([`str`](../library/stdtypes.html#str "str"), [`bytes`](../library/stdtypes.html#bytes "bytes") or [`bytearray`](../library/stdtypes.html#bytearray "bytearray")) [const char \*encoding, char \*\*buffer]
:   Same as `es` except that byte string objects are passed through without
    recoding them. Instead, the implementation assumes that the byte string object uses
    the encoding passed in as parameter.

`es#` ([`str`](../library/stdtypes.html#str "str")) [const char \*encoding, char \*\*buffer, [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t") \*buffer\_length]
:   This variant on `s#` is used for encoding Unicode into a character buffer.
    Unlike the `es` format, this variant allows input data which contains NUL
    characters.

    It requires three arguments. The first is only used as input, and must be a
    const char\* which points to the name of an encoding as a
    NUL-terminated string, or `NULL`, in which case `'utf-8'` encoding is used.
    An exception is raised if the named encoding is not known to Python. The
    second argument must be a char\*\*; the value of the pointer it
    references will be set to a buffer with the contents of the argument text.
    The text will be encoded in the encoding specified by the first argument.
    The third argument must be a pointer to an integer; the referenced integer
    will be set to the number of bytes in the output buffer.

    There are two modes of operation:

    If *\*buffer* points a `NULL` pointer, the function will allocate a buffer of
    the needed size, copy the encoded data into this buffer and set *\*buffer* to
    reference the newly allocated storage. The caller is responsible for calling
    [`PyMem_Free()`](memory.html#c.PyMem_Free "PyMem_Free") to free the allocated buffer after usage.

    If *\*buffer* points to a non-`NULL` pointer (an already allocated buffer),
    [`PyArg_ParseTuple()`](#c.PyArg_ParseTuple "PyArg_ParseTuple") will use this location as the buffer and interpret the
    initial value of *\*buffer\_length* as the buffer size. It will then copy the
    encoded data into the buffer and NUL-terminate it. If the buffer is not large
    enough, a [`ValueError`](../library/exceptions.html#ValueError "ValueError") will be set.

    In both cases, *\*buffer\_length* is set to the length of the encoded data
    without the trailing NUL byte.

`et#` ([`str`](../library/stdtypes.html#str "str"), [`bytes`](../library/stdtypes.html#bytes "bytes") or [`bytearray`](../library/stdtypes.html#bytearray "bytearray")) [const char \*encoding, char \*\*buffer, [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t") \*buffer\_length]
:   Same as `es#` except that byte string objects are passed through without recoding
    them. Instead, the implementation assumes that the byte string object uses the
    encoding passed in as parameter.

Changed in version 3.12: `u`, `u#`, `Z`, and `Z#` are removed because they used a legacy
`Py_UNICODE*` representation.