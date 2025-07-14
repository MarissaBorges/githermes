:   The first version requires that *numerator* and *denominator* are instances
    of [`numbers.Rational`](numbers.html#numbers.Rational "numbers.Rational") and returns a new [`Fraction`](#fractions.Fraction "fractions.Fraction") instance
    with value `numerator/denominator`. If *denominator* is `0`, it
    raises a [`ZeroDivisionError`](exceptions.html#ZeroDivisionError "ZeroDivisionError"). The second version requires that
    *other\_fraction* is an instance of [`numbers.Rational`](numbers.html#numbers.Rational "numbers.Rational") and returns a
    [`Fraction`](#fractions.Fraction "fractions.Fraction") instance with the same value. The next two versions accept
    either a [`float`](functions.html#float "float") or a [`decimal.Decimal`](decimal.html#decimal.Decimal "decimal.Decimal") instance, and return a
    [`Fraction`](#fractions.Fraction "fractions.Fraction") instance with exactly the same value. Note that due to the
    usual issues with binary floating point (see [Floating-Point Arithmetic: Issues and Limitations](../tutorial/floatingpoint.html#tut-fp-issues)), the
    argument to `Fraction(1.1)` is not exactly equal to 11/10, and so
    `Fraction(1.1)` does *not* return `Fraction(11, 10)` as one might expect.
    (But see the documentation for the [`limit_denominator()`](#fractions.Fraction.limit_denominator "fractions.Fraction.limit_denominator") method below.)
    The last version of the constructor expects a string or unicode instance.
    The usual form for this instance is:

    Copy

    ```
    [sign] numerator ['/' denominator]

    ```

    where the optional `sign` may be either ‘+’ or ‘-’ and
    `numerator` and `denominator` (if present) are strings of
    decimal digits (underscores may be used to delimit digits as with
    integral literals in code). In addition, any string that represents a finite
    value and is accepted by the [`float`](functions.html#float "float") constructor is also
    accepted by the [`Fraction`](#fractions.Fraction "fractions.Fraction") constructor. In either form the
    input string may also have leading and/or trailing whitespace.
    Here are some examples:

    Copy

    ```
    >>> from fractions import Fraction
    >>> Fraction(16, -10)
    Fraction(-8, 5)
    >>> Fraction(123)
    Fraction(123, 1)
    >>> Fraction()
    Fraction(0, 1)
    >>> Fraction('3/7')
    Fraction(3, 7)
    >>> Fraction(' -3/7 ')
    Fraction(-3, 7)
    >>> Fraction('1.414213 \t\n')
    Fraction(1414213, 1000000)
    >>> Fraction('-.125')
    Fraction(-1, 8)
    >>> Fraction('7e-6')
    Fraction(7, 1000000)
    >>> Fraction(2.25)
    Fraction(9, 4)
    >>> Fraction(1.1)
    Fraction(2476979795053773, 2251799813685248)
    >>> from decimal import Decimal
    >>> Fraction(Decimal('1.1'))
    Fraction(11, 10)

    ```

    The [`Fraction`](#fractions.Fraction "fractions.Fraction") class inherits from the abstract base class
    [`numbers.Rational`](numbers.html#numbers.Rational "numbers.Rational"), and implements all of the methods and
    operations from that class. [`Fraction`](#fractions.Fraction "fractions.Fraction") instances are [hashable](../glossary.html#term-hashable),
    and should be treated as immutable. In addition,
    [`Fraction`](#fractions.Fraction "fractions.Fraction") has the following properties and methods:

    Changed in version 3.9: The [`math.gcd()`](math.html#math.gcd "math.gcd") function is now used to normalize the *numerator*
    and *denominator*. [`math.gcd()`](math.html#math.gcd "math.gcd") always returns an [`int`](functions.html#int "int") type.
    Previously, the GCD type depended on *numerator* and *denominator*.

    Changed in version 3.11: Underscores are now permitted when creating a [`Fraction`](#fractions.Fraction "fractions.Fraction") instance
    from a string, following [**PEP 515**](https://peps.python.org/pep-0515/) rules.

    Changed in version 3.11: [`Fraction`](#fractions.Fraction "fractions.Fraction") implements `__int__` now to satisfy
    `typing.SupportsInt` instance checks.

    Changed in version 3.12: Space is allowed around the slash for string inputs: `Fraction('2 / 3')`.

    Changed in version 3.12: [`Fraction`](#fractions.Fraction "fractions.Fraction") instances now support float-style formatting, with
    presentation types `"e"`, `"E"`, `"f"`, `"F"`, `"g"`, `"G"`
    and `"%""`.

    Changed in version 3.13: Formatting of [`Fraction`](#fractions.Fraction "fractions.Fraction") instances without a presentation type
    now supports fill, alignment, sign handling, minimum width and grouping.

    numerator
    :   Numerator of the Fraction in lowest term.

    denominator
    :   Denominator of the Fraction in lowest term.

    as\_integer\_ratio()
    :   Return a tuple of two integers, whose ratio is equal
        to the original Fraction. The ratio is in lowest terms
        and has a positive denominator.

    is\_integer()
    :   Return `True` if the Fraction is an integer.

    *classmethod* from\_float(*f*)
    :   Alternative constructor which only accepts instances of
        [`float`](functions.html#float "float") or [`numbers.Integral`](numbers.html#numbers.Integral "numbers.Integral"). Beware that
        `Fraction.from_float(0.3)` is not the same value as `Fraction(3, 10)`.

        Note

        From Python 3.2 onwards, you can also construct a
        [`Fraction`](#fractions.Fraction "fractions.Fraction") instance directly from a [`float`](functions.html#float "float").

    *classmethod* from\_decimal(*dec*)
    :   Alternative constructor which only accepts instances of
        [`decimal.Decimal`](decimal.html#decimal.Decimal "decimal.Decimal") or [`numbers.Integral`](numbers.html#numbers.Integral "numbers.Integral").

    limit\_denominator(*max\_denominator=1000000*)
    :   Finds and returns the closest [`Fraction`](#fractions.Fraction "fractions.Fraction") to `self` that has
        denominator at most max\_denominator. This method is useful for finding
        rational approximations to a given floating-point number:

        Copy

        ```
        >>> from fractions import Fraction
        >>> Fraction('3.1415926535897932').limit_denominator(1000)
        Fraction(355, 113)

        ```

        or for recovering a rational number that’s represented as a float:

        Copy

        ```
        >>> from math import pi, cos
        >>> Fraction(cos(pi/3))
        Fraction(4503599627370497, 9007199254740992)
        >>> Fraction(cos(pi/3)).limit_denominator()
        Fraction(1, 2)
        >>> Fraction(1.1).limit_denominator()
        Fraction(11, 10)

        ```

    \_\_floor\_\_()
    :   Returns the greatest [`int`](functions.html#int "int") `<= self`. This method can
        also be accessed through the [`math.floor()`](math.html#math.floor "math.floor") function:

        Copy

        ```
        >>> from math import floor
        >>> floor(Fraction(355, 113))
        3

        ```

    \_\_ceil\_\_()
    :   Returns the least [`int`](functions.html#int "int") `>= self`. This method can
        also be accessed through the [`math.ceil()`](math.html#math.ceil "math.ceil") function.

    \_\_round\_\_()

    \_\_round\_\_(*ndigits*)
    :   The first version returns the nearest [`int`](functions.html#int "int") to `self`,
        rounding half to even. The second version rounds `self` to the
        nearest multiple of `Fraction(1, 10**ndigits)` (logically, if
        `ndigits` is negative), again rounding half toward even. This
        method can also be accessed through the [`round()`](functions.html#round "round") function.

    \_\_format\_\_(*format\_spec*, */*)
    :   Provides support for formatting of [`Fraction`](#fractions.Fraction "fractions.Fraction") instances via the
        [`str.format()`](stdtypes.html#str.format "str.format") method, the [`format()`](functions.html#format "format") built-in function, or
        [Formatted string literals](../reference/lexical_analysis.html#f-strings).

        If the `format_spec` format specification string does not end with one
        of the presentation types `'e'`, `'E'`, `'f'`, `'F'`, `'g'`,
        `'G'` or `'%'` then formatting follows the general rules for fill,
        alignment, sign handling, minimum width, and grouping as described in the
        [format specification mini-language](string.html#formatspec). The “alternate
        form” flag `'#'` is supported: if present, it forces the output string
        to always include an explicit denominator, even when the value being
        formatted is an exact integer. The zero-fill flag `'0'` is not
        supported.

        If the `format_spec` format specification string ends with one of
        the presentation types `'e'`, `'E'`, `'f'`, `'F'`, `'g'`,
        `'G'` or `'%'` then formatting follows the rules outlined for the
        [`float`](functions.html#float "float") type in the [Format Specification Mini-Language](string.html#formatspec) section.

        Here are some examples:

        Copy

        ```
        >>> from fractions import Fraction
        >>> format(Fraction(103993, 33102), '_')
        '103_993/33_102'
        >>> format(Fraction(1, 7), '.^+10')
        '...+1/7...'
        >>> format(Fraction(3, 1), '')
        '3'
        >>> format(Fraction(3, 1), '#')
        '3/1'
        >>> format(Fraction(1, 7), '.40g')
        '0.1428571428571428571428571428571428571429'
        >>> format(Fraction('1234567.855'), '_.2f')
        '1_234_567.86'
        >>> f"{Fraction(355, 113):*>20.6e}"
        '********3.141593e+00'
        >>> old_price, new_price = 499, 672
        >>> "{:.2%} price increase".format(Fraction(new_price, old_price) - 1)
        '34.67% price increase'

        ```