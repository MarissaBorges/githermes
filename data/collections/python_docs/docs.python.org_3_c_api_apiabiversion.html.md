API and ABI Versioning
======================

CPython exposes its version number in the following macros.
Note that these correspond to the version code is **built** with,
not necessarily the version used at **run time**.

See [C API Stability](stable.html#stable) for a discussion of API and ABI stability across versions.

PY\_MAJOR\_VERSION
:   The `3` in `3.4.1a2`.

PY\_MINOR\_VERSION
:   The `4` in `3.4.1a2`.

PY\_MICRO\_VERSION
:   The `1` in `3.4.1a2`.

PY\_RELEASE\_LEVEL
:   The `a` in `3.4.1a2`.
    This can be `0xA` for alpha, `0xB` for beta, `0xC` for release
    candidate or `0xF` for final.

PY\_RELEASE\_SERIAL
:   The `2` in `3.4.1a2`. Zero for final releases.

PY\_VERSION\_HEX
:   The Python version number encoded in a single integer.

    The underlying version information can be found by treating it as a 32 bit
    number in the following manner:

    | Bytes | Bits (big endian order) | Meaning | Value for `3.4.1a2` |
    | --- | --- | --- | --- |
    | 1 | 1-8 | `PY_MAJOR_VERSION` | `0x03` |
    | 2 | 9-16 | `PY_MINOR_VERSION` | `0x04` |
    | 3 | 17-24 | `PY_MICRO_VERSION` | `0x01` |
    | 4 | 25-28 | `PY_RELEASE_LEVEL` | `0xA` |
    | 29-32 | `PY_RELEASE_SERIAL` | `0x2` |

    Thus `3.4.1a2` is hexversion `0x030401a2` and `3.10.0` is
    hexversion `0x030a00f0`.

    Use this for numeric comparisons, e.g. `#if PY_VERSION_HEX >= ...`.

    This version is also available via the symbol [`Py_Version`](#c.Py_Version "Py_Version").

const unsigned long Py\_Version
:   *Part of the [Stable ABI](stable.html#stable) since version 3.11.*

    The Python runtime version number encoded in a single constant integer, with
    the same format as the [`PY_VERSION_HEX`](#c.PY_VERSION_HEX "PY_VERSION_HEX") macro.
    This contains the Python version used at run time.

All the given macros are defined in [Include/patchlevel.h](https://github.com/python/cpython/tree/3.13/Include/patchlevel.h).