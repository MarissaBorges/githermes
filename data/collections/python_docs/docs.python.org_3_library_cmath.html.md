`cmath` — Mathematical functions for complex numbers
====================================================

---

This module provides access to mathematical functions for complex numbers. The
functions in this module accept integers, floating-point numbers or complex
numbers as arguments. They will also accept any Python object that has either a
[`__complex__()`](../reference/datamodel.html#object.__complex__ "object.__complex__") or a [`__float__()`](../reference/datamodel.html#object.__float__ "object.__float__") method: these methods are used to
convert the object to a complex or floating-point number, respectively, and
the function is then applied to the result of the conversion.

Note

For functions involving branch cuts, we have the problem of deciding how to
define those functions on the cut itself. Following Kahan’s “Branch cuts for
complex elementary functions” paper, as well as Annex G of C99 and later C
standards, we use the sign of zero to distinguish one side of the branch cut
from the other: for a branch cut along (a portion of) the real axis we look
at the sign of the imaginary part, while for a branch cut along the
imaginary axis we look at the sign of the real part.

For example, the [`cmath.sqrt()`](#cmath.sqrt "cmath.sqrt") function has a branch cut along the
negative real axis. An argument of `complex(-2.0, -0.0)` is treated as
though it lies *below* the branch cut, and so gives a result on the negative
imaginary axis:

Copy

```
>>> cmath.sqrt(complex(-2.0, -0.0))
-1.4142135623730951j

```

But an argument of `complex(-2.0, 0.0)` is treated as though it lies above
the branch cut:

Copy

```
>>> cmath.sqrt(complex(-2.0, 0.0))
1.4142135623730951j

```

|  |  |
| --- | --- |
| **Conversions to and from polar coordinates** | |
| [`phase(z)`](#cmath.phase "cmath.phase") | Return the phase of *z* |
| [`polar(z)`](#cmath.polar "cmath.polar") | Return the representation of *z* in polar coordinates |
| [`rect(r, phi)`](#cmath.rect "cmath.rect") | Return the complex number *z* with polar coordinates *r* and *phi* |
| **Power and logarithmic functions** | |
| [`exp(z)`](#cmath.exp "cmath.exp") | Return *e* raised to the power *z* |
| [`log(z[, base])`](#cmath.log "cmath.log") | Return the logarithm of *z* to the given *base* (*e* by default) |
| [`log10(z)`](#cmath.log10 "cmath.log10") | Return the base-10 logarithm of *z* |
| [`sqrt(z)`](#cmath.sqrt "cmath.sqrt") | Return the square root of *z* |
| **Trigonometric functions** | |
| [`acos(z)`](#cmath.acos "cmath.acos") | Return the arc cosine of *z* |
| [`asin(z)`](#cmath.asin "cmath.asin") | Return the arc sine of *z* |
| [`atan(z)`](#cmath.atan "cmath.atan") | Return the arc tangent of *z* |
| [`cos(z)`](#cmath.cos "cmath.cos") | Return the cosine of *z* |
| [`sin(z)`](#cmath.sin "cmath.sin") | Return the sine of *z* |
| [`tan(z)`](#cmath.tan "cmath.tan") | Return the tangent of *z* |
| **Hyperbolic functions** | |
| [`acosh(z)`](#cmath.acosh "cmath.acosh") | Return the inverse hyperbolic cosine of *z* |
| [`asinh(z)`](#cmath.asinh "cmath.asinh") | Return the inverse hyperbolic sine of *z* |
| [`atanh(z)`](#cmath.atanh "cmath.atanh") | Return the inverse hyperbolic tangent of *z* |
| [`cosh(z)`](#cmath.cosh "cmath.cosh") | Return the hyperbolic cosine of *z* |
| [`sinh(z)`](#cmath.sinh "cmath.sinh") | Return the hyperbolic sine of *z* |
| [`tanh(z)`](#cmath.tanh "cmath.tanh") | Return the hyperbolic tangent of *z* |
| **Classification functions** | |
| [`isfinite(z)`](#cmath.isfinite "cmath.isfinite") | Check if all components of *z* are finite |
| [`isinf(z)`](#cmath.isinf "cmath.isinf") | Check if any component of *z* is infinite |
| [`isnan(z)`](#cmath.isnan "cmath.isnan") | Check if any component of *z* is a NaN |
| [`isclose(a, b, *, rel_tol, abs_tol)`](#cmath.isclose "cmath.isclose") | Check if the values *a* and *b* are close to each other |
| **Constants** | |
| [`pi`](#cmath.pi "cmath.pi") | *π* = 3.141592… |
| [`e`](#cmath.e "cmath.e") | *e* = 2.718281… |
| [`tau`](#cmath.tau "cmath.tau") | *τ* = 2*π* = 6.283185… |
| [`inf`](#cmath.inf "cmath.inf") | Positive infinity |
| [`infj`](#cmath.infj "cmath.infj") | Pure imaginary infinity |
| [`nan`](#cmath.nan "cmath.nan") | “Not a number” (NaN) |
| [`nanj`](#cmath.nanj "cmath.nanj") | Pure imaginary NaN |

Conversions to and from polar coordinates
-----------------------------------------

A Python complex number `z` is stored internally using *rectangular*
or *Cartesian* coordinates. It is completely determined by its *real
part* `z.real` and its *imaginary part* `z.imag`.

*Polar coordinates* give an alternative way to represent a complex
number. In polar coordinates, a complex number *z* is defined by the
modulus *r* and the phase angle *phi*. The modulus *r* is the distance
from *z* to the origin, while the phase *phi* is the counterclockwise
angle, measured in radians, from the positive x-axis to the line
segment that joins the origin to *z*.

The following functions can be used to convert from the native
rectangular coordinates to polar coordinates and back.

cmath.phase(*z*)
:   Return the phase of *z* (also known as the *argument* of *z*), as a float.
    `phase(z)` is equivalent to `math.atan2(z.imag, z.real)`. The result
    lies in the range [-*π*, *π*], and the branch cut for this operation lies
    along the negative real axis. The sign of the result is the same as the
    sign of `z.imag`, even when `z.imag` is zero:

    Copy

    ```
    >>> phase(complex(-1.0, 0.0))
    3.141592653589793
    >>> phase(complex(-1.0, -0.0))
    -3.141592653589793

    ```

Note

The modulus (absolute value) of a complex number *z* can be
computed using the built-in [`abs()`](functions.html#abs "abs") function. There is no
separate [`cmath`](#module-cmath "cmath: Mathematical functions for complex numbers.") module function for this operation.

cmath.polar(*z*)
:   Return the representation of *z* in polar coordinates. Returns a
    pair `(r, phi)` where *r* is the modulus of *z* and *phi* is the
    phase of *z*. `polar(z)` is equivalent to `(abs(z),
    phase(z))`.

cmath.rect(*r*, *phi*)
:   Return the complex number *z* with polar coordinates *r* and *phi*.
    Equivalent to `complex(r * math.cos(phi), r * math.sin(phi))`.

Power and logarithmic functions
-------------------------------

cmath.exp(*z*)
:   Return *e* raised to the power *z*, where *e* is the base of natural
    logarithms.

cmath.log(*z*[, *base*])
:   Return the logarithm of *z* to the given *base*. If the *base* is not
    specified, returns the natural logarithm of *z*. There is one branch cut,
    from 0 along the negative real axis to -∞.

cmath.log10(*z*)
:   Return the base-10 logarithm of *z*. This has the same branch cut as
    [`log()`](#cmath.log "cmath.log").

cmath.sqrt(*z*)
:   Return the square root of *z*. This has the same branch cut as [`log()`](#cmath.log "cmath.log").

Trigonometric functions
-----------------------

cmath.acos(*z*)
:   Return the arc cosine of *z*. There are two branch cuts: One extends right
    from 1 along the real axis to ∞. The other extends left from -1 along the
    real axis to -∞.

cmath.asin(*z*)
:   Return the arc sine of *z*. This has the same branch cuts as [`acos()`](#cmath.acos "cmath.acos").

cmath.atan(*z*)
:   Return the arc tangent of *z*. There are two branch cuts: One extends from
    `1j` along the imaginary axis to `∞j`. The other extends from `-1j`
    along the imaginary axis to `-∞j`.

cmath.cos(*z*)
:   Return the cosine of *z*.

cmath.sin(*z*)
:   Return the sine of *z*.

cmath.tan(*z*)
:   Return the tangent of *z*.

Hyperbolic functions
--------------------

cmath.acosh(*z*)
:   Return the inverse hyperbolic cosine of *z*. There is one branch cut,
    extending left from 1 along the real axis to -∞.

cmath.asinh(*z*)
:   Return the inverse hyperbolic sine of *z*. There are two branch cuts:
    One extends from `1j` along the imaginary axis to `∞j`. The other
    extends from `-1j` along the imaginary axis to `-∞j`.

cmath.atanh(*z*)
:   Return the inverse hyperbolic tangent of *z*. There are two branch cuts: One
    extends from `1` along the real axis to `∞`. The other extends from
    `-1` along the real axis to `-∞`.

cmath.cosh(*z*)
:   Return the hyperbolic cosine of *z*.

cmath.sinh(*z*)
:   Return the hyperbolic sine of *z*.

cmath.tanh(*z*)
:   Return the hyperbolic tangent of *z*.

Classification functions
------------------------

cmath.isfinite(*z*)
:   Return `True` if both the real and imaginary parts of *z* are finite, and
    `False` otherwise.

cmath.isinf(*z*)
:   Return `True` if either the real or the imaginary part of *z* is an
    infinity, and `False` otherwise.

cmath.isnan(*z*)
:   Return `True` if either the real or the imaginary part of *z* is a NaN,
    and `False` otherwise.

cmath.isclose(*a*, *b*, *\**, *rel\_tol=1e-09*, *abs\_tol=0.0*)
:   Return `True` if the values *a* and *b* are close to each other and
    `False` otherwise.

    Whether or not two values are considered close is determined according to
    given absolute and relative tolerances. If no errors occur, the result will
    be: `abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`.

    *rel\_tol* is the relative tolerance – it is the maximum allowed difference
    between *a* and *b*, relative to the larger absolute value of *a* or *b*.
    For example, to set a tolerance of 5%, pass `rel_tol=0.05`. The default
    tolerance is `1e-09`, which assures that the two values are the same
    within about 9 decimal digits. *rel\_tol* must be nonnegative and less
    than `1.0`.

    *abs\_tol* is the absolute tolerance; it defaults to `0.0` and it must be
    nonnegative. When comparing `x` to `0.0`, `isclose(x, 0)` is computed
    as `abs(x) <= rel_tol  * abs(x)`, which is `False` for any `x` and
    rel\_tol less than `1.0`. So add an appropriate positive abs\_tol argument
    to the call.

    The IEEE 754 special values of `NaN`, `inf`, and `-inf` will be
    handled according to IEEE rules. Specifically, `NaN` is not considered
    close to any other value, including `NaN`. `inf` and `-inf` are only
    considered close to themselves.

    See also

    [**PEP 485**](https://peps.python.org/pep-0485/) – A function for testing approximate equality

Constants
---------

cmath.pi
:   The mathematical constant *π*, as a float.

cmath.e
:   The mathematical constant *e*, as a float.

cmath.tau
:   The mathematical constant *τ*, as a float.

cmath.inf
:   Floating-point positive infinity. Equivalent to `float('inf')`.

cmath.infj
:   Complex number with zero real part and positive infinity imaginary
    part. Equivalent to `complex(0.0, float('inf'))`.

cmath.nan
:   A floating-point “not a number” (NaN) value. Equivalent to
    `float('nan')`.

cmath.nanj
:   Complex number with zero real part and NaN imaginary part. Equivalent to
    `complex(0.0, float('nan'))`.

Note that the selection of functions is similar, but not identical, to that in
module [`math`](math.html#module-math "math: Mathematical functions (sin() etc.)."). The reason for having two modules is that some users aren’t
interested in complex numbers, and perhaps don’t even know what they are. They
would rather have `math.sqrt(-1)` raise an exception than return a complex
number. Also note that the functions defined in [`cmath`](#module-cmath "cmath: Mathematical functions for complex numbers.") always return a
complex number, even if the answer can be expressed as a real number (in which
case the complex number has an imaginary part of zero).

A note on branch cuts: They are curves along which the given function fails to
be continuous. They are a necessary feature of many complex functions. It is
assumed that if you need to compute with complex functions, you will understand
about branch cuts. Consult almost any (not too elementary) book on complex
variables for enlightenment. For information of the proper choice of branch
cuts for numerical purposes, a good reference should be the following:

See also

Kahan, W: Branch cuts for complex elementary functions; or, Much ado about
nothing’s sign bit. In Iserles, A., and Powell, M. (eds.), The state of the art
in numerical analysis. Clarendon Press (1987) pp165–211.