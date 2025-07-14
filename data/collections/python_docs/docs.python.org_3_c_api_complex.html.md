Complex Number Objects
======================

Python’s complex number objects are implemented as two distinct types when
viewed from the C API: one is the Python object exposed to Python programs, and
the other is a C structure which represents the actual complex number value.
The API provides functions for working with both.

Complex Numbers as C Structures
-------------------------------

Note that the functions which accept these structures as parameters and return
them as results do so *by value* rather than dereferencing them through
pointers. This is consistent throughout the API.

type Py\_complex
:   The C structure which corresponds to the value portion of a Python complex
    number object. Most of the functions for dealing with complex number objects
    use structures of this type as input or output values, as appropriate.

    double real

    double imag

    The structure is defined as:

    ```
    typedef struct {
        double real;
        double imag;
    } Py_complex;

    ```

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_sum([Py\_complex](#c.Py_complex "Py_complex") left, [Py\_complex](#c.Py_complex "Py_complex") right)
:   Return the sum of two complex numbers, using the C [`Py_complex`](#c.Py_complex "Py_complex")
    representation.

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_diff([Py\_complex](#c.Py_complex "Py_complex") left, [Py\_complex](#c.Py_complex "Py_complex") right)
:   Return the difference between two complex numbers, using the C
    [`Py_complex`](#c.Py_complex "Py_complex") representation.

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_neg([Py\_complex](#c.Py_complex "Py_complex") num)
:   Return the negation of the complex number *num*, using the C
    [`Py_complex`](#c.Py_complex "Py_complex") representation.

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_prod([Py\_complex](#c.Py_complex "Py_complex") left, [Py\_complex](#c.Py_complex "Py_complex") right)
:   Return the product of two complex numbers, using the C [`Py_complex`](#c.Py_complex "Py_complex")
    representation.

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_quot([Py\_complex](#c.Py_complex "Py_complex") dividend, [Py\_complex](#c.Py_complex "Py_complex") divisor)
:   Return the quotient of two complex numbers, using the C [`Py_complex`](#c.Py_complex "Py_complex")
    representation.

    If *divisor* is null, this method returns zero and sets
    `errno` to `EDOM`.

[Py\_complex](#c.Py_complex "Py_complex") \_Py\_c\_pow([Py\_complex](#c.Py_complex "Py_complex") num, [Py\_complex](#c.Py_complex "Py_complex") exp)
:   Return the exponentiation of *num* by *exp*, using the C [`Py_complex`](#c.Py_complex "Py_complex")
    representation.

    If *num* is null and *exp* is not a positive real number,
    this method returns zero and sets `errno` to `EDOM`.

Complex Numbers as Python Objects
---------------------------------

type PyComplexObject
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python complex number object.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyComplex\_Type
:   *Part of the [Stable ABI](stable.html#stable).*

    This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python complex number
    type. It is the same object as [`complex`](../library/functions.html#complex "complex") in the Python layer.

int PyComplex\_Check([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if its argument is a [`PyComplexObject`](#c.PyComplexObject "PyComplexObject") or a subtype of
    [`PyComplexObject`](#c.PyComplexObject "PyComplexObject"). This function always succeeds.

int PyComplex\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*p)
:   Return true if its argument is a [`PyComplexObject`](#c.PyComplexObject "PyComplexObject"), but not a subtype of
    [`PyComplexObject`](#c.PyComplexObject "PyComplexObject"). This function always succeeds.

[PyObject](structures.html#c.PyObject "PyObject") \*PyComplex\_FromCComplex([Py\_complex](#c.Py_complex "Py_complex") v)
:   *Return value: New reference.*

    Create a new Python complex number object from a C [`Py_complex`](#c.Py_complex "Py_complex") value.
    Return `NULL` with an exception set on error.

[PyObject](structures.html#c.PyObject "PyObject") \*PyComplex\_FromDoubles(double real, double imag)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return a new [`PyComplexObject`](#c.PyComplexObject "PyComplexObject") object from *real* and *imag*.
    Return `NULL` with an exception set on error.

double PyComplex\_RealAsDouble([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the real part of *op* as a C double.

    If *op* is not a Python complex number object but has a
    [`__complex__()`](../reference/datamodel.html#object.__complex__ "object.__complex__") method, this method will first be called to
    convert *op* to a Python complex number object. If `__complex__()` is
    not defined then it falls back to call [`PyFloat_AsDouble()`](float.html#c.PyFloat_AsDouble "PyFloat_AsDouble") and
    returns its result.

    Upon failure, this method returns `-1.0` with an exception set, so one
    should call [`PyErr_Occurred()`](exceptions.html#c.PyErr_Occurred "PyErr_Occurred") to check for errors.

double PyComplex\_ImagAsDouble([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the imaginary part of *op* as a C double.

    If *op* is not a Python complex number object but has a
    [`__complex__()`](../reference/datamodel.html#object.__complex__ "object.__complex__") method, this method will first be called to
    convert *op* to a Python complex number object. If `__complex__()` is
    not defined then it falls back to call [`PyFloat_AsDouble()`](float.html#c.PyFloat_AsDouble "PyFloat_AsDouble") and
    returns `0.0` on success.

    Upon failure, this method returns `-1.0` with an exception set, so one
    should call [`PyErr_Occurred()`](exceptions.html#c.PyErr_Occurred "PyErr_Occurred") to check for errors.

[Py\_complex](#c.Py_complex "Py_complex") PyComplex\_AsCComplex([PyObject](structures.html#c.PyObject "PyObject") \*op)
:   Return the [`Py_complex`](#c.Py_complex "Py_complex") value of the complex number *op*.

    If *op* is not a Python complex number object but has a [`__complex__()`](../reference/datamodel.html#object.__complex__ "object.__complex__")
    method, this method will first be called to convert *op* to a Python complex
    number object. If `__complex__()` is not defined then it falls back to
    [`__float__()`](../reference/datamodel.html#object.__float__ "object.__float__"). If `__float__()` is not defined then it falls back
    to [`__index__()`](../reference/datamodel.html#object.__index__ "object.__index__").

    Upon failure, this method returns [`Py_complex`](#c.Py_complex "Py_complex")
    with [`real`](#c.Py_complex.real "Py_complex.real") set to `-1.0` and with an exception set, so one
    should call [`PyErr_Occurred()`](exceptions.html#c.PyErr_Occurred "PyErr_Occurred") to check for errors.