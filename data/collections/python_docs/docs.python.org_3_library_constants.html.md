Built-in Constants
==================

A small number of constants live in the built-in namespace. They are:

False
:   The false value of the [`bool`](functions.html#bool "bool") type. Assignments to `False`
    are illegal and raise a [`SyntaxError`](exceptions.html#SyntaxError "SyntaxError").

True
:   The true value of the [`bool`](functions.html#bool "bool") type. Assignments to `True`
    are illegal and raise a [`SyntaxError`](exceptions.html#SyntaxError "SyntaxError").

None
:   An object frequently used to represent the absence of a value, as when
    default arguments are not passed to a function. Assignments to `None`
    are illegal and raise a [`SyntaxError`](exceptions.html#SyntaxError "SyntaxError").
    `None` is the sole instance of the [`NoneType`](types.html#types.NoneType "types.NoneType") type.

NotImplemented
:   A special value which should be returned by the binary special methods
    (e.g. [`__eq__()`](../reference/datamodel.html#object.__eq__ "object.__eq__"), [`__lt__()`](../reference/datamodel.html#object.__lt__ "object.__lt__"), [`__add__()`](../reference/datamodel.html#object.__add__ "object.__add__"), [`__rsub__()`](../reference/datamodel.html#object.__rsub__ "object.__rsub__"),
    etc.) to indicate that the operation is not implemented with respect to
    the other type; may be returned by the in-place binary special methods
    (e.g. [`__imul__()`](../reference/datamodel.html#object.__imul__ "object.__imul__"), [`__iand__()`](../reference/datamodel.html#object.__iand__ "object.__iand__"), etc.) for the same purpose.
    It should not be evaluated in a boolean context.
    `NotImplemented` is the sole instance of the [`types.NotImplementedType`](types.html#types.NotImplementedType "types.NotImplementedType") type.

    Note

    When a binary (or in-place) method returns `NotImplemented` the
    interpreter will try the reflected operation on the other type (or some
    other fallback, depending on the operator). If all attempts return
    `NotImplemented`, the interpreter will raise an appropriate exception.
    Incorrectly returning `NotImplemented` will result in a misleading
    error message or the `NotImplemented` value being returned to Python code.

    See [Implementing the arithmetic operations](numbers.html#implementing-the-arithmetic-operations) for examples.

    Caution

    `NotImplemented` and `NotImplementedError` are not
    interchangeable. This constant should only be used as described
    above; see [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError") for details on correct usage
    of the exception.

    Changed in version 3.9: Evaluating `NotImplemented` in a boolean context is deprecated. While
    it currently evaluates as true, it will emit a [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning").
    It will raise a [`TypeError`](exceptions.html#TypeError "TypeError") in a future version of Python.

Ellipsis
:   The same as the ellipsis literal “`...`”. Special value used mostly in conjunction
    with extended slicing syntax for user-defined container data types.
    `Ellipsis` is the sole instance of the [`types.EllipsisType`](types.html#types.EllipsisType "types.EllipsisType") type.

\_\_debug\_\_
:   This constant is true if Python was not started with an [`-O`](../using/cmdline.html#cmdoption-O) option.
    See also the [`assert`](../reference/simple_stmts.html#assert) statement.

Note

The names [`None`](#None "None"), [`False`](#False "False"), [`True`](#True "True") and [`__debug__`](#debug__ "__debug__")
cannot be reassigned (assignments to them, even as an attribute name, raise
[`SyntaxError`](exceptions.html#SyntaxError "SyntaxError")), so they can be considered “true” constants.

Constants added by the [`site`](site.html#module-site "site: Module responsible for site-specific configuration.") module
-------------------------------------------------------------------------------------------------------------------------

The [`site`](site.html#module-site "site: Module responsible for site-specific configuration.") module (which is imported automatically during startup, except
if the [`-S`](../using/cmdline.html#cmdoption-S) command-line option is given) adds several constants to the
built-in namespace. They are useful for the interactive interpreter shell and
should not be used in programs.

quit(*code=None*)

exit(*code=None*)
:   Objects that when printed, print a message like “Use quit() or Ctrl-D
    (i.e. EOF) to exit”, and when called, raise [`SystemExit`](exceptions.html#SystemExit "SystemExit") with the
    specified exit code.

help
:   Object that when printed, prints the message “Type help() for interactive
    help, or help(object) for help about object.”, and when called,
    acts as described [`elsewhere`](functions.html#help "help").

copyright

credits
:   Objects that when printed or called, print the text of copyright or
    credits, respectively.

license
:   Object that when printed, prints the message “Type license() to see the
    full license text”, and when called, displays the full license text in a
    pager-like fashion (one screen at a time).