:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Returns the integer *n* converted to base *base* as a string. The *base*
    argument must be one of 2, 8, 10, or 16. For base 2, 8, or 16, the
    returned string is prefixed with a base marker of `'0b'`, `'0o'`, or
    `'0x'`, respectively. If *n* is not a Python int, it is converted with
    [`PyNumber_Index()`](#c.PyNumber_Index "PyNumber_Index") first.