:   *Part of the [Stable ABI](stable.html#stable).*

    Usable replacement for [`PySlice_GetIndices()`](#c.PySlice_GetIndices "PySlice_GetIndices"). Retrieve the start,
    stop, and step indices from the slice object *slice* assuming a sequence of
    length *length*, and store the length of the slice in *slicelength*. Out
    of bounds indices are clipped in a manner consistent with the handling of
    normal slices.

    Return `0` on success and `-1` on error with an exception set.

    Note

    This function is considered not safe for resizable sequences.
    Its invocation should be replaced by a combination of
    [`PySlice_Unpack()`](#c.PySlice_Unpack "PySlice_Unpack") and [`PySlice_AdjustIndices()`](#c.PySlice_AdjustIndices "PySlice_AdjustIndices") where

    ```
    if (PySlice_GetIndicesEx(slice, length, &start, &stop, &step, &slicelength) < 0) {
        // return error
    }

    ```

    is replaced by

    ```
    if (PySlice_Unpack(slice, &start, &stop, &step) < 0) {
        // return error
    }
    slicelength = PySlice_AdjustIndices(length, &start, &stop, step);

    ```

    Changed in version 3.2: The parameter type for the *slice* parameter was `PySliceObject*`
    before.

    Changed in version 3.6.1: If `Py_LIMITED_API` is not set or set to the value between `0x03050400`
    and `0x03060000` (not including) or `0x03060100` or higher
    `PySlice_GetIndicesEx()` is implemented as a macro using
    `PySlice_Unpack()` and `PySlice_AdjustIndices()`.
    Arguments *start*, *stop* and *step* are evaluated more than once.

    Deprecated since version 3.6.1: If `Py_LIMITED_API` is set to the value less than `0x03050400` or
    between `0x03060000` and `0x03060100` (not including)
    `PySlice_GetIndicesEx()` is a deprecated function.