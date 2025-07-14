`glob` — Unix style pathname pattern expansion
==============================================

**Source code:** [Lib/glob.py](https://github.com/python/cpython/tree/3.13/Lib/glob.py)

---

The [`glob`](#module-glob "glob: Unix shell style pathname pattern expansion.") module finds all the pathnames matching a specified pattern
according to the rules used by the Unix shell, although results are returned in
arbitrary order. No tilde expansion is done, but `*`, `?`, and character
ranges expressed with `[]` will be correctly matched. This is done by using
the [`os.scandir()`](os.html#os.scandir "os.scandir") and [`fnmatch.fnmatch()`](fnmatch.html#fnmatch.fnmatch "fnmatch.fnmatch") functions in concert, and
not by actually invoking a subshell.

Note that files beginning with a dot (`.`) can only be matched by
patterns that also start with a dot,
unlike [`fnmatch.fnmatch()`](fnmatch.html#fnmatch.fnmatch "fnmatch.fnmatch") or [`pathlib.Path.glob()`](pathlib.html#pathlib.Path.glob "pathlib.Path.glob").
(For tilde and shell variable expansion, use [`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser") and
[`os.path.expandvars()`](os.path.html#os.path.expandvars "os.path.expandvars").)

For a literal match, wrap the meta-characters in brackets.
For example, `'[?]'` matches the character `'?'`.

The [`glob`](#module-glob "glob: Unix shell style pathname pattern expansion.") module defines the following functions:

glob.glob(*pathname*, *\**, *root\_dir=None*, *dir\_fd=None*, *recursive=False*, *include\_hidden=False*)
:   Return a possibly empty list of path names that match *pathname*, which must be
    a string containing a path specification. *pathname* can be either absolute
    (like `/usr/src/Python-1.5/Makefile`) or relative (like
    `../../Tools/*/*.gif`), and can contain shell-style wildcards. Broken
    symlinks are included in the results (as in the shell). Whether or not the
    results are sorted depends on the file system. If a file that satisfies
    conditions is removed or added during the call of this function, whether
    a path name for that file will be included is unspecified.

    If *root\_dir* is not `None`, it should be a [path-like object](../glossary.html#term-path-like-object)
    specifying the root directory for searching. It has the same effect on
    [`glob()`](#module-glob "glob: Unix shell style pathname pattern expansion.") as changing the current directory before calling it. If
    *pathname* is relative, the result will contain paths relative to
    *root\_dir*.

    This function can support [paths relative to directory descriptors](os.html#dir-fd) with the *dir\_fd* parameter.

    If *recursive* is true, the pattern “`**`” will match any files and zero or
    more directories, subdirectories and symbolic links to directories. If the
    pattern is followed by an [`os.sep`](os.html#os.sep "os.sep") or [`os.altsep`](os.html#os.altsep "os.altsep") then files will not
    match.

    If *include\_hidden* is true, “`**`” pattern will match hidden directories.

    Raises an [auditing event](sys.html#auditing) `glob.glob` with arguments `pathname`, `recursive`.

    Raises an [auditing event](sys.html#auditing) `glob.glob/2` with arguments `pathname`, `recursive`, `root_dir`, `dir_fd`.

    Note

    Using the “`**`” pattern in large directory trees may consume
    an inordinate amount of time.

    Note

    This function may return duplicate path names if *pathname*
    contains multiple “`**`” patterns and *recursive* is true.

    Changed in version 3.5: Support for recursive globs using “`**`”.

    Changed in version 3.10: Added the *root\_dir* and *dir\_fd* parameters.

    Changed in version 3.11: Added the *include\_hidden* parameter.

glob.iglob(*pathname*, *\**, *root\_dir=None*, *dir\_fd=None*, *recursive=False*, *include\_hidden=False*)
:   Return an [iterator](../glossary.html#term-iterator) which yields the same values as [`glob()`](#module-glob "glob: Unix shell style pathname pattern expansion.")
    without actually storing them all simultaneously.

    Raises an [auditing event](sys.html#auditing) `glob.glob` with arguments `pathname`, `recursive`.

    Raises an [auditing event](sys.html#auditing) `glob.glob/2` with arguments `pathname`, `recursive`, `root_dir`, `dir_fd`.

    Note

    This function may return duplicate path names if *pathname*
    contains multiple “`**`” patterns and *recursive* is true.

    Changed in version 3.5: Support for recursive globs using “`**`”.

    Changed in version 3.10: Added the *root\_dir* and *dir\_fd* parameters.

    Changed in version 3.11: Added the *include\_hidden* parameter.

glob.escape(*pathname*)
:   Escape all special characters (`'?'`, `'*'` and `'['`).
    This is useful if you want to match an arbitrary literal string that may
    have special characters in it. Special characters in drive/UNC
    sharepoints are not escaped, e.g. on Windows
    `escape('//?/c:/Quo vadis?.txt')` returns `'//?/c:/Quo vadis[?].txt'`.

glob.translate(*pathname*, *\**, *recursive=False*, *include\_hidden=False*, *seps=None*)
:   Convert the given path specification to a regular expression for use with
    [`re.match()`](re.html#re.match "re.match"). The path specification can contain shell-style wildcards.

    For example:

    Copy

    ```
    >>> import glob, re
    >>>
    >>> regex = glob.translate('**/*.txt', recursive=True, include_hidden=True)
    >>> regex
    '(?s:(?:.+/)?[^/]*\\.txt)\\Z'
    >>> reobj = re.compile(regex)
    >>> reobj.match('foo/bar/baz.txt')
    <re.Match object; span=(0, 15), match='foo/bar/baz.txt'>

    ```

    Path separators and segments are meaningful to this function, unlike
    [`fnmatch.translate()`](fnmatch.html#fnmatch.translate "fnmatch.translate"). By default wildcards do not match path
    separators, and `*` pattern segments match precisely one path segment.

    If *recursive* is true, the pattern segment “`**`” will match any number
    of path segments.

    If *include\_hidden* is true, wildcards can match path segments that start
    with a dot (`.`).

    A sequence of path separators may be supplied to the *seps* argument. If
    not given, [`os.sep`](os.html#os.sep "os.sep") and [`altsep`](os.html#os.altsep "os.altsep") (if available) are used.

Examples
--------

Consider a directory containing the following files:
`1.gif`, `2.txt`, `card.gif` and a subdirectory `sub`
which contains only the file `3.txt`. [`glob()`](#module-glob "glob: Unix shell style pathname pattern expansion.") will produce
the following results. Notice how any leading components of the path are
preserved.

Copy

```
>>> import glob
>>> glob.glob('./[0-9].*')
['./1.gif', './2.txt']
>>> glob.glob('*.gif')
['1.gif', 'card.gif']
>>> glob.glob('?.gif')
['1.gif']
>>> glob.glob('**/*.txt', recursive=True)
['2.txt', 'sub/3.txt']
>>> glob.glob('./**/', recursive=True)
['./', './sub/']

```

If the directory contains files starting with `.` they won’t be matched by
default. For example, consider a directory containing `card.gif` and
`.card.gif`:

Copy

```
>>> import glob
>>> glob.glob('*.gif')
['card.gif']
>>> glob.glob('.c*')
['.card.gif']

```

See also

The [`fnmatch`](fnmatch.html#module-fnmatch "fnmatch: Unix shell style filename pattern matching.") module offers shell-style filename (not path) expansion.

See also

The [`pathlib`](pathlib.html#module-pathlib "pathlib: Object-oriented filesystem paths") module offers high-level path objects.