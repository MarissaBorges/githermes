Pack and Unpack functions
-------------------------

The pack and unpack functions provide an efficient platform-independent way to
store floating-point values as byte strings. The Pack routines produce a bytes
string from a C double, and the Unpack routines produce a C
double from such a bytes string. The suffix (2, 4 or 8) specifies the
number of bytes in the bytes string.

On platforms that appear to use IEEE 754 formats these functions work by
copying bits. On other platforms, the 2-byte format is identical to the IEEE
754 binary16 half-precision format, the 4-byte format (32-bit) is identical to
the IEEE 754 binary32 single precision format, and the 8-byte format to the
IEEE 754 binary64 double precision format, although the packing of INFs and
NaNs (if such things exist on the platform) isn’t handled correctly, and
attempting to unpack a bytes string containing an IEEE INF or NaN will raise an
exception.

On non-IEEE platforms with more precision, or larger dynamic range, than IEEE
754 supports, not all values can be packed; on non-IEEE platforms with less
precision, or smaller dynamic range, not all values can be unpacked. What
happens in such cases is partly accidental (alas).

### Pack functions

The pack routines write 2, 4 or 8 bytes, starting at *p*. *le* is an
int argument, non-zero if you want the bytes string in little-endian
format (exponent last, at `p+1`, `p+3`, or `p+6` `p+7`), zero if you
want big-endian format (exponent first, at *p*). The `PY_BIG_ENDIAN`
constant can be used to use the native endian: it is equal to `1` on big
endian processor, or `0` on little endian processor.

Return value: `0` if all is OK, `-1` if error (and an exception is set,
most likely [`OverflowError`](../library/exceptions.html#OverflowError "OverflowError")).

There are two problems on non-IEEE platforms:

int PyFloat\_Pack2(double x, unsigned char \*p, int le)
:   Pack a C double as the IEEE 754 binary16 half-precision format.

int PyFloat\_Pack4(double x, unsigned char \*p, int le)
:   Pack a C double as the IEEE 754 binary32 single precision format.

int PyFloat\_Pack8(double x, unsigned char \*p, int le)
:   Pack a C double as the IEEE 754 binary64 double precision format.

### Unpack functions

The unpack routines read 2, 4 or 8 bytes, starting at *p*. *le* is an
int argument, non-zero if the bytes string is in little-endian format
(exponent last, at `p+1`, `p+3` or `p+6` and `p+7`), zero if big-endian
(exponent first, at *p*). The `PY_BIG_ENDIAN` constant can be used to
use the native endian: it is equal to `1` on big endian processor, or `0`
on little endian processor.

Return value: The unpacked double. On error, this is `-1.0` and
[`PyErr_Occurred()`](exceptions.html#c.PyErr_Occurred "PyErr_Occurred") is true (and an exception is set, most likely
[`OverflowError`](../library/exceptions.html#OverflowError "OverflowError")).

Note that on a non-IEEE platform this will refuse to unpack a bytes string that
represents a NaN or infinity.

double PyFloat\_Unpack2(const unsigned char \*p, int le)
:   Unpack the IEEE 754 binary16 half-precision format as a C double.

double PyFloat\_Unpack4(const unsigned char \*p, int le)
:   Unpack the IEEE 754 binary32 single precision format as a C double.

double PyFloat\_Unpack8(const unsigned char \*p, int le)
:   Unpack the IEEE 754 binary64 double precision format as a C double.