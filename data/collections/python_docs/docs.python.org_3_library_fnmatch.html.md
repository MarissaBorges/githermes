`fnmatch` — Unix filename pattern matching
==========================================

**Source code:** [Lib/fnmatch.py](https://github.com/python/cpython/tree/3.13/Lib/fnmatch.py)

---

This module provides support for Unix shell-style wildcards, which are *not* the
same as regular expressions (which are documented in the [`re`](re.html#module-re "re: Regular expression operations.") module). The
special characters used in shell-style wildcards are:

| Pattern | Meaning |
| --- | --- |
| `*` | matches everything |
| `?` | matches any single character |
| `[seq]` | matches any character in *seq* |
| `[!seq]` | matches any character not in *seq* |

For a literal match, wrap the meta-characters in brackets.
For example, `'[?]'` matches the character `'?'`.

Note that the filename separator (`'/'` on Unix) is *not* special to this
module. See module [`glob`](glob.html#module-glob "glob: Unix shell style pathname pattern expansion.") for pathname expansion ([`glob`](glob.html#module-glob "glob: Unix shell style pathname pattern expansion.") uses
[`filter()`](#fnmatch.filter "fnmatch.filter") to match pathname segments). Similarly, filenames starting with
a period are not special for this module, and are matched by the `*` and `?`
patterns.

Unless stated otherwise, “filename string” and “pattern string” either refer to
[`str`](stdtypes.html#str "str") or `ISO-8859-1` encoded [`bytes`](stdtypes.html#bytes "bytes") objects. Note that the
functions documented below do not allow to mix a `bytes` pattern with
a `str` filename, and vice-versa.

Finally, note that [`functools.lru_cache()`](functools.html#functools.lru_cache "functools.lru_cache") with a *maxsize* of 32768
is used to cache the (typed) compiled regex patterns in the following
functions: [`fnmatch()`](#module-fnmatch "fnmatch: Unix shell style filename pattern matching."), [`fnmatchcase()`](#fnmatch.fnmatchcase "fnmatch.fnmatchcase"), [`filter()`](#fnmatch.filter "fnmatch.filter").

fnmatch.fnmatch(*name*, *pat*)
:   Test whether the filename string *name* matches the pattern string *pat*,
    returning `True` or `False`. Both parameters are case-normalized
    using [`os.path.normcase()`](os.path.html#os.path.normcase "os.path.normcase"). [`fnmatchcase()`](#fnmatch.fnmatchcase "fnmatch.fnmatchcase") can be used to perform a
    case-sensitive comparison, regardless of whether that’s standard for the
    operating system.

    This example will print all file names in the current directory with the
    extension `.txt`:

    Copy

    ```
    import fnmatch
    import os

    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.txt'):
            print(file)

    ```

fnmatch.fnmatchcase(*name*, *pat*)
:   Test whether the filename string *name* matches the pattern string *pat*,
    returning `True` or `False`;
    the comparison is case-sensitive and does not apply [`os.path.normcase()`](os.path.html#os.path.normcase "os.path.normcase").

fnmatch.filter(*names*, *pat*)
:   Construct a list from those elements of the [iterable](../glossary.html#term-iterable) of filename
    strings *names* that match the pattern string *pat*.
    It is the same as `[n for n in names if fnmatch(n, pat)]`,
    but implemented more efficiently.

fnmatch.translate(*pat*)
:   Return the shell-style pattern *pat* converted to a regular expression for
    using with [`re.match()`](re.html#re.match "re.match"). The pattern is expected to be a [`str`](stdtypes.html#str "str").

    Example:

    Copy

    ```
    >>> import fnmatch, re
    >>>
    >>> regex = fnmatch.translate('*.txt')
    >>> regex
    '(?s:.*\\.txt)\\Z'
    >>> reobj = re.compile(regex)
    >>> reobj.match('foobar.txt')
    <re.Match object; span=(0, 10), match='foobar.txt'>

    ```

See also

Module [`glob`](glob.html#module-glob "glob: Unix shell style pathname pattern expansion.")
:   Unix shell-style path expansion.