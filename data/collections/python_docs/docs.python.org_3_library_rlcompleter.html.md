`rlcompleter` — Completion function for GNU readline
====================================================

**Source code:** [Lib/rlcompleter.py](https://github.com/python/cpython/tree/3.13/Lib/rlcompleter.py)

---

The `rlcompleter` module defines a completion function suitable to be
passed to [`set_completer()`](readline.html#readline.set_completer "readline.set_completer") in the [`readline`](readline.html#module-readline "readline: GNU readline support for Python. (Unix)") module.

When this module is imported on a Unix platform with the [`readline`](readline.html#module-readline "readline: GNU readline support for Python. (Unix)") module
available, an instance of the [`Completer`](#rlcompleter.Completer "rlcompleter.Completer") class is automatically created
and its [`complete()`](#rlcompleter.Completer.complete "rlcompleter.Completer.complete") method is set as the
[readline completer](readline.html#readline-completion). The method provides
completion of valid Python [identifiers and keywords](../reference/lexical_analysis.html#identifiers).

Example:

Copy

```
>>> import rlcompleter
>>> import readline
>>> readline.parse_and_bind("tab: complete")
>>> readline. <TAB PRESSED>
readline.__doc__          readline.get_line_buffer(  readline.read_init_file(
readline.__file__         readline.insert_text(      readline.set_completer(
readline.__name__         readline.parse_and_bind(
>>> readline.

```

The `rlcompleter` module is designed for use with Python’s
[interactive mode](../tutorial/interpreter.html#tut-interactive). Unless Python is run with the
[`-S`](../using/cmdline.html#cmdoption-S) option, the module is automatically imported and configured
(see [Readline configuration](site.html#rlcompleter-config)).

On platforms without [`readline`](readline.html#module-readline "readline: GNU readline support for Python. (Unix)"), the [`Completer`](#rlcompleter.Completer "rlcompleter.Completer") class defined by
this module can still be used for custom purposes.

*class* rlcompleter.Completer
:   Completer objects have the following method:

    complete(*text*, *state*)
    :   Return the next possible completion for *text*.

        When called by the [`readline`](readline.html#module-readline "readline: GNU readline support for Python. (Unix)") module, this method is called
        successively with `state == 0, 1, 2, ...` until the method returns
        `None`.

        If called for *text* that doesn’t include a period character (`'.'`), it will
        complete from names currently defined in [`__main__`](__main__.html#module-__main__ "__main__: The environment where top-level code is run. Covers command-line interfaces, import-time behavior, and ``__name__ == '__main__'``."), [`builtins`](builtins.html#module-builtins "builtins: The module that provides the built-in namespace.") and
        keywords (as defined by the [`keyword`](keyword.html#module-keyword "keyword: Test whether a string is a keyword in Python.") module).

        If called for a dotted name, it will try to evaluate anything without obvious
        side-effects (functions will not be evaluated, but it can generate calls to
        [`__getattr__()`](../reference/datamodel.html#object.__getattr__ "object.__getattr__")) up to the last part, and find matches for the
        rest via the [`dir()`](functions.html#dir "dir") function. Any exception raised during the
        evaluation of the expression is caught, silenced and [`None`](constants.html#None "None") is
        returned.