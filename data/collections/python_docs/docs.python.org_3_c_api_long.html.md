:   Copy the Python integer value *pylong* to a native *buffer* of size
    *n\_bytes*. The *flags* can be set to `-1` to behave similarly to a C cast,
    or to values documented below to control the behavior.

    Returns `-1` with an exception raised on error. This may happen if
    *pylong* cannot be interpreted as an integer, or if *pylong* was negative
    and the `Py_ASNATIVEBYTES_REJECT_NEGATIVE` flag was set.

    Otherwise, returns the number of bytes required to store the value.
    If this is equal to or less than *n\_bytes*, the entire value was copied.
    All *n\_bytes* of the buffer are written: large buffers are padded with
    zeroes.

    If the returned value is greater than *n\_bytes*, the value was
    truncated: as many of the lowest bits of the value as could fit are written,
    and the higher bits are ignored. This matches the typical behavior
    of a C-style downcast.

    Note

    Overflow is not considered an error. If the returned value
    is larger than *n\_bytes*, most significant bits were discarded.

    `0` will never be returned.

    Values are always copied as two’s-complement.

    Usage example:

    ```
    int32_t value;
    Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, &value, sizeof(value), -1);
    if (bytes < 0) {
        // Failed. A Python exception was set with the reason.
        return NULL;
    }
    else if (bytes <= (Py_ssize_t)sizeof(value)) {
        // Success!
    }
    else {
        // Overflow occurred, but 'value' contains the truncated
        // lowest bits of pylong.
    }

    ```

    Passing zero to *n\_bytes* will return the size of a buffer that would
    be large enough to hold the value. This may be larger than technically
    necessary, but not unreasonably so. If *n\_bytes=0*, *buffer* may be
    `NULL`.

    Note

    Passing *n\_bytes=0* to this function is not an accurate way to determine
    the bit length of the value.

    To get at the entire Python value of an unknown size, the function can be
    called twice: first to determine the buffer size, then to fill it:

    ```
    // Ask how much space we need.
    Py_ssize_t expected = PyLong_AsNativeBytes(pylong, NULL, 0, -1);
    if (expected < 0) {
        // Failed. A Python exception was set with the reason.
        return NULL;
    }
    assert(expected != 0);  // Impossible per the API definition.
    uint8_t *bignum = malloc(expected);
    if (!bignum) {
        PyErr_SetString(PyExc_MemoryError, "bignum malloc failed.");
        return NULL;
    }
    // Safely get the entire value.
    Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, bignum, expected, -1);
    if (bytes < 0) {  // Exception has been set.
        free(bignum);
        return NULL;
    }
    else if (bytes > expected) {  // This should not be possible.
        PyErr_SetString(PyExc_RuntimeError,
            "Unexpected bignum truncation after a size check.");
        free(bignum);
        return NULL;
    }
    // The expected success given the above pre-check.
    // ... use bignum ...
    free(bignum);

    ```

    *flags* is either `-1` (`Py_ASNATIVEBYTES_DEFAULTS`) to select defaults
    that behave most like a C cast, or a combination of the other flags in
    the table below.
    Note that `-1` cannot be combined with other flags.

    Currently, `-1` corresponds to
    `Py_ASNATIVEBYTES_NATIVE_ENDIAN | Py_ASNATIVEBYTES_UNSIGNED_BUFFER`.

    | Flag | Value |
    | --- | --- |
    | Py\_ASNATIVEBYTES\_DEFAULTS | `-1` |
    | Py\_ASNATIVEBYTES\_BIG\_ENDIAN | `0` |
    | Py\_ASNATIVEBYTES\_LITTLE\_ENDIAN | `1` |
    | Py\_ASNATIVEBYTES\_NATIVE\_ENDIAN | `3` |
    | Py\_ASNATIVEBYTES\_UNSIGNED\_BUFFER | `4` |
    | Py\_ASNATIVEBYTES\_REJECT\_NEGATIVE | `8` |
    | Py\_ASNATIVEBYTES\_ALLOW\_INDEX | `16` |

    Specifying `Py_ASNATIVEBYTES_NATIVE_ENDIAN` will override any other endian
    flags. Passing `2` is reserved.

    By default, sufficient buffer will be requested to include a sign bit.
    For example, when converting 128 with *n\_bytes=1*, the function will return
    2 (or more) in order to store a zero sign bit.

    If `Py_ASNATIVEBYTES_UNSIGNED_BUFFER` is specified, a zero sign bit
    will be omitted from size calculations. This allows, for example, 128 to fit
    in a single-byte buffer. If the destination buffer is later treated as
    signed, a positive input value may become negative.
    Note that the flag does not affect handling of negative values: for those,
    space for a sign bit is always requested.

    Specifying `Py_ASNATIVEBYTES_REJECT_NEGATIVE` causes an exception to be set
    if *pylong* is negative. Without this flag, negative values will be copied
    provided there is enough space for at least one sign bit, regardless of
    whether `Py_ASNATIVEBYTES_UNSIGNED_BUFFER` was specified.

    If `Py_ASNATIVEBYTES_ALLOW_INDEX` is specified and a non-integer value is
    passed, its [`__index__()`](../reference/datamodel.html#object.__index__ "object.__index__") method will be called first. This may
    result in Python code executing and other threads being allowed to run, which
    could cause changes to other objects or values in use. When *flags* is
    `-1`, this option is not set, and non-integer values will raise
    [`TypeError`](../library/exceptions.html#TypeError "TypeError").

    Note

    With the default *flags* (`-1`, or *UNSIGNED\_BUFFER* without
    *REJECT\_NEGATIVE*), multiple Python integers can map to a single value
    without overflow. For example, both `255` and `-1` fit a single-byte
    buffer and set all its bits.
    This matches typical C cast behavior.