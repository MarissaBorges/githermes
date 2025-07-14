`zipimport` — Import modules from Zip archives
==============================================

**Source code:** [Lib/zipimport.py](https://github.com/python/cpython/tree/3.13/Lib/zipimport.py)

---

This module adds the ability to import Python modules (`*.py`,
`*.pyc`) and packages from ZIP-format archives. It is usually not
needed to use the [`zipimport`](#module-zipimport "zipimport: Support for importing Python modules from ZIP archives.") module explicitly; it is automatically used
by the built-in [`import`](../reference/simple_stmts.html#import) mechanism for [`sys.path`](sys.html#sys.path "sys.path") items that are paths
to ZIP archives.

Typically, [`sys.path`](sys.html#sys.path "sys.path") is a list of directory names as strings. This module
also allows an item of [`sys.path`](sys.html#sys.path "sys.path") to be a string naming a ZIP file archive.
The ZIP archive can contain a subdirectory structure to support package imports,
and a path within the archive can be specified to only import from a
subdirectory. For example, the path `example.zip/lib/` would only
import from the `lib/` subdirectory within the archive.

Any files may be present in the ZIP archive, but importers are only invoked for
`.py` and `.pyc` files. ZIP import of dynamic modules
(`.pyd`, `.so`) is disallowed. Note that if an archive only contains
`.py` files, Python will not attempt to modify the archive by adding the
corresponding `.pyc` file, meaning that if a ZIP archive
doesn’t contain `.pyc` files, importing may be rather slow.

Changed in version 3.13: ZIP64 is supported

Changed in version 3.8: Previously, ZIP archives with an archive comment were not supported.

See also

[PKZIP Application Note](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
:   Documentation on the ZIP file format by Phil Katz, the creator of the format and
    algorithms used.

[**PEP 273**](https://peps.python.org/pep-0273/) - Import Modules from Zip Archives
:   Written by James C. Ahlstrom, who also provided an implementation. Python 2.3
    follows the specification in [**PEP 273**](https://peps.python.org/pep-0273/), but uses an implementation written by Just
    van Rossum that uses the import hooks described in [**PEP 302**](https://peps.python.org/pep-0302/).

[`importlib`](importlib.html#module-importlib "importlib: The implementation of the import machinery.") - The implementation of the import machinery
:   Package providing the relevant protocols for all importers to
    implement.

This module defines an exception:

*exception* zipimport.ZipImportError
:   Exception raised by zipimporter objects. It’s a subclass of [`ImportError`](exceptions.html#ImportError "ImportError"),
    so it can be caught as [`ImportError`](exceptions.html#ImportError "ImportError"), too.

zipimporter Objects
-------------------

[`zipimporter`](#zipimport.zipimporter "zipimport.zipimporter") is the class for importing ZIP files.

*class* zipimport.zipimporter(*archivepath*)
:   Create a new zipimporter instance. *archivepath* must be a path to a ZIP
    file, or to a specific path within a ZIP file. For example, an *archivepath*
    of `foo/bar.zip/lib` will look for modules in the `lib` directory
    inside the ZIP file `foo/bar.zip` (provided that it exists).

    [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") is raised if *archivepath* doesn’t point to a valid ZIP
    archive.

    Changed in version 3.12: Methods `find_loader()` and `find_module()`, deprecated in 3.10 are
    now removed. Use [`find_spec()`](#zipimport.zipimporter.find_spec "zipimport.zipimporter.find_spec") instead.

    create\_module(*spec*)
    :   Implementation of [`importlib.abc.Loader.create_module()`](importlib.html#importlib.abc.Loader.create_module "importlib.abc.Loader.create_module") that returns
        [`None`](constants.html#None "None") to explicitly request the default semantics.

    exec\_module(*module*)
    :   Implementation of [`importlib.abc.Loader.exec_module()`](importlib.html#importlib.abc.Loader.exec_module "importlib.abc.Loader.exec_module").

    find\_spec(*fullname*, *target=None*)
    :   An implementation of [`importlib.abc.PathEntryFinder.find_spec()`](importlib.html#importlib.abc.PathEntryFinder.find_spec "importlib.abc.PathEntryFinder.find_spec").

    get\_code(*fullname*)
    :   Return the code object for the specified module. Raise
        [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") if the module couldn’t be imported.

    get\_data(*pathname*)
    :   Return the data associated with *pathname*. Raise [`OSError`](exceptions.html#OSError "OSError") if the
        file wasn’t found.

        Changed in version 3.3: [`IOError`](exceptions.html#IOError "IOError") used to be raised, it is now an alias of [`OSError`](exceptions.html#OSError "OSError").

    get\_filename(*fullname*)
    :   Return the value `__file__` would be set to if the specified module
        was imported. Raise [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") if the module couldn’t be
        imported.

    get\_source(*fullname*)
    :   Return the source code for the specified module. Raise
        [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") if the module couldn’t be found, return
        [`None`](constants.html#None "None") if the archive does contain the module, but has no source
        for it.

    is\_package(*fullname*)
    :   Return `True` if the module specified by *fullname* is a package. Raise
        [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") if the module couldn’t be found.

    load\_module(*fullname*)
    :   Load the module specified by *fullname*. *fullname* must be the fully
        qualified (dotted) module name. Returns the imported module on success,
        raises [`ZipImportError`](#zipimport.ZipImportError "zipimport.ZipImportError") on failure.

    invalidate\_caches()
    :   Clear out the internal cache of information about files found within
        the ZIP archive.

    archive
    :   The file name of the importer’s associated ZIP file, without a possible
        subpath.

    prefix
    :   The subpath within the ZIP file where modules are searched. This is the
        empty string for zipimporter objects which point to the root of the ZIP
        file.

    The [`archive`](#zipimport.zipimporter.archive "zipimport.zipimporter.archive") and [`prefix`](#zipimport.zipimporter.prefix "zipimport.zipimporter.prefix") attributes, when combined with a
    slash, equal the original *archivepath* argument given to the
    [`zipimporter`](#zipimport.zipimporter "zipimport.zipimporter") constructor.

Examples
--------

Here is an example that imports a module from a ZIP archive - note that the
[`zipimport`](#module-zipimport "zipimport: Support for importing Python modules from ZIP archives.") module is not explicitly used.

```
$ unzip -l example.zip
Archive:  example.zip
  Length     Date   Time    Name
 --------    ----   ----    ----
     8467  11-26-02 22:30   jwzthreading.py
 --------                   -------
     8467                   1 file
$ ./python
Python 2.3 (#1, Aug 1 2003, 19:54:32)
>>> import sys
>>> sys.path.insert(0, 'example.zip')  # Add .zip file to front of path
>>> import jwzthreading
>>> jwzthreading.__file__
'example.zip/jwzthreading.py'

```