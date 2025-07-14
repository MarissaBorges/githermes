:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Take a C `printf()`-style *format* string and a variable number of
    arguments, calculate the size of the resulting Python Unicode string and return
    a string with the values formatted into it. The variable arguments must be C
    types and must correspond exactly to the format characters in the *format*
    ASCII-encoded string.

    A conversion specifier contains two or more characters and has the following
    components, which must occur in this order:

    1. The `'%'` character, which marks the start of the specifier.
    2. Conversion flags (optional), which affect the result of some conversion
       types.
    3. Minimum field width (optional).
       If specified as an `'*'` (asterisk), the actual width is given in the
       next argument, which must be of type int, and the object to
       convert comes after the minimum field width and optional precision.
    4. Precision (optional), given as a `'.'` (dot) followed by the precision.
       If specified as `'*'` (an asterisk), the actual precision is given in
       the next argument, which must be of type int, and the value to
       convert comes after the precision.
    5. Length modifier (optional).
    6. Conversion type.

    The conversion flag characters are:

    | Flag | Meaning |
    | --- | --- |
    | `0` | The conversion will be zero padded for numeric values. |
    | `-` | The converted value is left adjusted (overrides the `0` flag if both are given). |

    The length modifiers for following integer conversions (`d`, `i`,
    `o`, `u`, `x`, or `X`) specify the type of the argument
    (int by default):

    | Modifier | Types |
    | --- | --- |
    | `l` | long or unsigned long |
    | `ll` | long long or unsigned long long |
    | `j` | `intmax_t` or `uintmax_t` |
    | `z` | `size_t` or `ssize_t` |
    | `t` | `ptrdiff_t` |

    The length modifier `l` for following conversions `s` or `V` specify
    that the type of the argument is const wchar\_t\*.

    The conversion specifiers are:

    | Conversion Specifier | Type | Comment |
    | --- | --- | --- |
    | `%` | *n/a* | The literal `%` character. |
    | `d`, `i` | Specified by the length modifier | The decimal representation of a signed C integer. |
    | `u` | Specified by the length modifier | The decimal representation of an unsigned C integer. |
    | `o` | Specified by the length modifier | The octal representation of an unsigned C integer. |
    | `x` | Specified by the length modifier | The hexadecimal representation of an unsigned C integer (lowercase). |
    | `X` | Specified by the length modifier | The hexadecimal representation of an unsigned C integer (uppercase). |
    | `c` | int | A single character. |
    | `s` | const char\* or const wchar\_t\* | A null-terminated C character array. |
    | `p` | const void\* | The hex representation of a C pointer. Mostly equivalent to `printf("%p")` except that it is guaranteed to start with the literal `0x` regardless of what the platform’s `printf` yields. |
    | `A` | [PyObject](structures.html#c.PyObject "PyObject")\* | The result of calling [`ascii()`](../library/functions.html#ascii "ascii"). |
    | `U` | [PyObject](structures.html#c.PyObject "PyObject")\* | A Unicode object. |
    | `V` | [PyObject](structures.html#c.PyObject "PyObject")\*, const char\* or const wchar\_t\* | A Unicode object (which may be `NULL`) and a null-terminated C character array as a second parameter (which will be used, if the first parameter is `NULL`). |
    | `S` | [PyObject](structures.html#c.PyObject "PyObject")\* | The result of calling [`PyObject_Str()`](object.html#c.PyObject_Str "PyObject_Str"). |
    | `R` | [PyObject](structures.html#c.PyObject "PyObject")\* | The result of calling [`PyObject_Repr()`](object.html#c.PyObject_Repr "PyObject_Repr"). |
    | `T` | [PyObject](structures.html#c.PyObject "PyObject")\* | Get the fully qualified name of an object type; call [`PyType_GetFullyQualifiedName()`](type.html#c.PyType_GetFullyQualifiedName "PyType_GetFullyQualifiedName"). |
    | `#T` | [PyObject](structures.html#c.PyObject "PyObject")\* | Similar to `T` format, but use a colon (`:`) as separator between the module name and the qualified name. |
    | `N` | [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject")\* | Get the fully qualified name of a type; call [`PyType_GetFullyQualifiedName()`](type.html#c.PyType_GetFullyQualifiedName "PyType_GetFullyQualifiedName"). |
    | `#N` | [PyTypeObject](type.html#c.PyTypeObject "PyTypeObject")\* | Similar to `N` format, but use a colon (`:`) as separator between the module name and the qualified name. |

    Note

    The width formatter unit is number of characters rather than bytes.
    The precision formatter unit is number of bytes or `wchar_t`
    items (if the length modifier `l` is used) for `"%s"` and
    `"%V"` (if the `PyObject*` argument is `NULL`), and a number of
    characters for `"%A"`, `"%U"`, `"%S"`, `"%R"` and `"%V"`
    (if the `PyObject*` argument is not `NULL`).

    Note

    Unlike to C `printf()` the `0` flag has effect even when
    a precision is given for integer conversions (`d`, `i`, `u`, `o`,
    `x`, or `X`).

    Changed in version 3.2: Support for `"%lld"` and `"%llu"` added.

    Changed in version 3.3: Support for `"%li"`, `"%lli"` and `"%zi"` added.

    Changed in version 3.4: Support width and precision formatter for `"%s"`, `"%A"`, `"%U"`,
    `"%V"`, `"%S"`, `"%R"` added.

    Changed in version 3.12: Support for conversion specifiers `o` and `X`.
    Support for length modifiers `j` and `t`.
    Length modifiers are now applied to all integer conversions.
    Length modifier `l` is now applied to conversion specifiers `s` and `V`.
    Support for variable width and precision `*`.
    Support for flag `-`.

    An unrecognized format character now sets a [`SystemError`](../library/exceptions.html#SystemError "SystemError").
    In previous versions it caused all the rest of the format string to be
    copied as-is to the result string, and any extra arguments discarded.

    Changed in version 3.13: Support for `%T`, `%#T`, `%N` and `%#N` formats added.