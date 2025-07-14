`importlib.resources` – Package resource reading, opening and access
====================================================================

**Source code:** [Lib/importlib/resources/\_\_init\_\_.py](https://github.com/python/cpython/tree/3.13/Lib/importlib/resources/__init__.py)

---

This module leverages Python’s import system to provide access to *resources*
within *packages*.

“Resources” are file-like resources associated with a module or package in
Python. The resources may be contained directly in a package, within a
subdirectory contained in that package, or adjacent to modules outside a
package. Resources may be text or binary. As a result, Python module sources
(.py) of a package and compilation artifacts (pycache) are technically
de-facto resources of that package. In practice, however, resources are
primarily those non-Python artifacts exposed specifically by the package
author.

Resources can be opened or read in either binary or text mode.

Resources are roughly akin to files inside directories, though it’s important
to keep in mind that this is just a metaphor. Resources and packages **do
not** have to exist as physical files and directories on the file system:
for example, a package and its resources can be imported from a zip file using
[`zipimport`](zipimport.html#module-zipimport "zipimport: Support for importing Python modules from ZIP archives.").

[`Loaders`](importlib.html#importlib.abc.Loader "importlib.abc.Loader") that wish to support resource reading should implement a
`get_resource_reader(fullname)` method as specified by
[`importlib.resources.abc.ResourceReader`](importlib.resources.abc.html#importlib.resources.abc.ResourceReader "importlib.resources.abc.ResourceReader").

*class* importlib.resources.Anchor
:   Represents an anchor for resources, either a [`module object`](types.html#types.ModuleType "types.ModuleType") or a module name as a string. Defined as
    `Union[str, ModuleType]`.

importlib.resources.files(*anchor: [Anchor](#importlib.resources.Anchor "importlib.resources.Anchor") | [None](constants.html#None "None") = None*)
:   Returns a [`Traversable`](importlib.resources.abc.html#importlib.resources.abc.Traversable "importlib.resources.abc.Traversable") object
    representing the resource container (think directory) and its resources
    (think files). A Traversable may contain other containers (think
    subdirectories).

    *anchor* is an optional [`Anchor`](#importlib.resources.Anchor "importlib.resources.Anchor"). If the anchor is a
    package, resources are resolved from that package. If a module,
    resources are resolved adjacent to that module (in the same package
    or the package root). If the anchor is omitted, the caller’s module
    is used.

    Changed in version 3.12: *package* parameter was renamed to *anchor*. *anchor* can now
    be a non-package module and if omitted will default to the caller’s
    module. *package* is still accepted for compatibility but will raise
    a [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning"). Consider passing the anchor positionally or
    using `importlib_resources >= 5.10` for a compatible interface
    on older Pythons.

importlib.resources.as\_file(*traversable*)
:   Given a [`Traversable`](importlib.resources.abc.html#importlib.resources.abc.Traversable "importlib.resources.abc.Traversable") object representing
    a file or directory, typically from [`importlib.resources.files()`](#importlib.resources.files "importlib.resources.files"),
    return a context manager for use in a [`with`](../reference/compound_stmts.html#with) statement.
    The context manager provides a [`pathlib.Path`](pathlib.html#pathlib.Path "pathlib.Path") object.

    Exiting the context manager cleans up any temporary file or directory
    created when the resource was extracted from e.g. a zip file.

    Use `as_file` when the Traversable methods
    (`read_text`, etc) are insufficient and an actual file or directory on
    the file system is required.

    Changed in version 3.12: Added support for *traversable* representing a directory.

Functional API
--------------

A set of simplified, backwards-compatible helpers is available.
These allow common operations in a single function call.

For all the following functions:

* *anchor* is an [`Anchor`](#importlib.resources.Anchor "importlib.resources.Anchor"),
  as in [`files()`](#importlib.resources.files "importlib.resources.files").
  Unlike in `files`, it may not be omitted.
* *path\_names* are components of a resource’s path name, relative to
  the anchor.
  For example, to get the text of resource named `info.txt`, use:

  Copy

  ```
  importlib.resources.read_text(my_module, "info.txt")

  ```

  Like [`Traversable.joinpath`](importlib.resources.abc.html#importlib.resources.abc.Traversable "importlib.resources.abc.Traversable"),
  The individual components should use forward slashes (`/`)
  as path separators.
  For example, the following are equivalent:

  Copy

  ```
  importlib.resources.read_binary(my_module, "pics/painting.png")
  importlib.resources.read_binary(my_module, "pics", "painting.png")

  ```

  For backward compatibility reasons, functions that read text require
  an explicit *encoding* argument if multiple *path\_names* are given.
  For example, to get the text of `info/chapter1.txt`, use:

  Copy

  ```
  importlib.resources.read_text(my_module, "info", "chapter1.txt",
                                encoding='utf-8')

  ```

importlib.resources.open\_binary(*anchor*, *\*path\_names*)
:   Open the named resource for binary reading.

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.

    This function returns a [`BinaryIO`](typing.html#typing.BinaryIO "typing.BinaryIO") object,
    that is, a binary stream open for reading.

    This function is roughly equivalent to:

    Copy

    ```
    files(anchor).joinpath(*path_names).open('rb')

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.

importlib.resources.open\_text(*anchor*, *\*path\_names*, *encoding='utf-8'*, *errors='strict'*)
:   Open the named resource for text reading.
    By default, the contents are read as strict UTF-8.

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.
    *encoding* and *errors* have the same meaning as in built-in [`open()`](functions.html#open "open").

    For backward compatibility reasons, the *encoding* argument must be given
    explicitly if there are multiple *path\_names*.
    This limitation is scheduled to be removed in Python 3.15.

    This function returns a [`TextIO`](typing.html#typing.TextIO "typing.TextIO") object,
    that is, a text stream open for reading.

    This function is roughly equivalent to:

    Copy

    ```
    files(anchor).joinpath(*path_names).open('r', encoding=encoding)

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.
    *encoding* and *errors* must be given as keyword arguments.

importlib.resources.read\_binary(*anchor*, *\*path\_names*)
:   Read and return the contents of the named resource as [`bytes`](stdtypes.html#bytes "bytes").

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.

    This function is roughly equivalent to:

    Copy

    ```
    files(anchor).joinpath(*path_names).read_bytes()

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.

importlib.resources.read\_text(*anchor*, *\*path\_names*, *encoding='utf-8'*, *errors='strict'*)
:   Read and return the contents of the named resource as [`str`](stdtypes.html#str "str").
    By default, the contents are read as strict UTF-8.

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.
    *encoding* and *errors* have the same meaning as in built-in [`open()`](functions.html#open "open").

    For backward compatibility reasons, the *encoding* argument must be given
    explicitly if there are multiple *path\_names*.
    This limitation is scheduled to be removed in Python 3.15.

    This function is roughly equivalent to:

    Copy

    ```
    files(anchor).joinpath(*path_names).read_text(encoding=encoding)

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.
    *encoding* and *errors* must be given as keyword arguments.

importlib.resources.path(*anchor*, *\*path\_names*)
:   Provides the path to the *resource* as an actual file system path. This
    function returns a context manager for use in a [`with`](../reference/compound_stmts.html#with) statement.
    The context manager provides a [`pathlib.Path`](pathlib.html#pathlib.Path "pathlib.Path") object.

    Exiting the context manager cleans up any temporary files created, e.g.
    when the resource needs to be extracted from a zip file.

    For example, the [`stat()`](pathlib.html#pathlib.Path.stat "pathlib.Path.stat") method requires
    an actual file system path; it can be used like this:

    Copy

    ```
    with importlib.resources.path(anchor, "resource.txt") as fspath:
        result = fspath.stat()

    ```

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.

    This function is roughly equivalent to:

    Copy

    ```
    as_file(files(anchor).joinpath(*path_names))

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.
    *encoding* and *errors* must be given as keyword arguments.

importlib.resources.is\_resource(*anchor*, *\*path\_names*)
:   Return `True` if the named resource exists, otherwise `False`.
    This function does not consider directories to be resources.

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.

    This function is roughly equivalent to:

    Copy

    ```
    files(anchor).joinpath(*path_names).is_file()

    ```

    Changed in version 3.13: Multiple *path\_names* are accepted.

importlib.resources.contents(*anchor*, *\*path\_names*)
:   Return an iterable over the named items within the package or path.
    The iterable returns names of resources (e.g. files) and non-resources
    (e.g. directories) as [`str`](stdtypes.html#str "str").
    The iterable does not recurse into subdirectories.

    See [the introduction](#importlib-resources-functional) for
    details on *anchor* and *path\_names*.

    This function is roughly equivalent to:

    Copy

    ```
    for resource in files(anchor).joinpath(*path_names).iterdir():
        yield resource.name

    ```

    Deprecated since version 3.11: Prefer `iterdir()` as above, which offers more control over the
    results and richer functionality.