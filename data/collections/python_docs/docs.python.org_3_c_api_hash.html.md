PyHash API
==========

See also the [`PyTypeObject.tp_hash`](typeobj.html#c.PyTypeObject.tp_hash "PyTypeObject.tp_hash") member and [Hashing of numeric types](../library/stdtypes.html#numeric-hash).

type Py\_hash\_t
:   Hash value type: signed integer.

type Py\_uhash\_t
:   Hash value type: unsigned integer.

PyHASH\_MODULUS
:   The [Mersenne prime](https://en.wikipedia.org/wiki/Mersenne_prime) `P = 2**n -1`, used for numeric hash scheme.

PyHASH\_BITS
:   The exponent `n` of `P` in [`PyHASH_MODULUS`](#c.PyHASH_MODULUS "PyHASH_MODULUS").

PyHASH\_MULTIPLIER
:   Prime multiplier used in string and various other hashes.

PyHASH\_INF
:   The hash value returned for a positive infinity.

PyHASH\_IMAG
:   The multiplier used for the imaginary part of a complex number.

type PyHash\_FuncDef
:   Hash function definition used by [`PyHash_GetFuncDef()`](#c.PyHash_GetFuncDef "PyHash_GetFuncDef").

    const char \*name
    :   Hash function name (UTF-8 encoded string).

    const int hash\_bits
    :   Internal size of the hash value in bits.

    const int seed\_bits
    :   Size of seed input in bits.

[PyHash\_FuncDef](#c.PyHash_FuncDef "PyHash_FuncDef") \*PyHash\_GetFuncDef(void)
:   Get the hash function definition.

    See also

    [**PEP 456**](https://peps.python.org/pep-0456/) “Secure and interchangeable hash algorithm”.

[Py\_hash\_t](#c.Py_hash_t "Py_hash_t") Py\_HashPointer(const void \*ptr)
:   Hash a pointer value: process the pointer value as an integer (cast it to
    `uintptr_t` internally). The pointer is not dereferenced.

    The function cannot fail: it cannot return `-1`.

[Py\_hash\_t](#c.Py_hash_t "Py_hash_t") PyObject\_GenericHash([PyObject](structures.html#c.PyObject "PyObject") \*obj)
:   Generic hashing function that is meant to be put into a type
    object’s `tp_hash` slot.
    Its result only depends on the object’s identity.

    **CPython implementation detail:** In CPython, it is equivalent to [`Py_HashPointer()`](#c.Py_HashPointer "Py_HashPointer").