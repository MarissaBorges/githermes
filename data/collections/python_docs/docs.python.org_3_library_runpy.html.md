:   Execute the code at the named filesystem location and return the resulting
    module’s globals dictionary. As with a script name supplied to the CPython
    command line, *file\_path* may refer to a Python source file, a
    compiled bytecode file or a valid [`sys.path`](sys.html#sys.path "sys.path") entry containing a
    [`__main__`](__main__.html#module-__main__ "__main__: The environment where top-level code is run. Covers command-line interfaces, import-time behavior, and ``__name__ == '__main__'``.") module
    (e.g. a zipfile containing a top-level `__main__.py` file).

    For a simple script, the specified code is simply executed in a fresh
    module namespace. For a valid [`sys.path`](sys.html#sys.path "sys.path") entry (typically a zipfile or
    directory), the entry is first added to the beginning of `sys.path`. The
    function then looks for and executes a [`__main__`](__main__.html#module-__main__ "__main__: The environment where top-level code is run. Covers command-line interfaces, import-time behavior, and ``__name__ == '__main__'``.") module using the
    updated path. Note that there is no special protection against invoking
    an existing `__main__` entry located elsewhere on `sys.path` if
    there is no such module at the specified location.

    The optional dictionary argument *init\_globals* may be used to pre-populate
    the module’s globals dictionary before the code is executed.
    *init\_globals* will not be modified. If any of the special global variables
    below are defined in *init\_globals*, those definitions are
    overridden by [`run_path()`](#runpy.run_path "runpy.run_path").

    The special global variables `__name__`, `__spec__`, `__file__`,
    `__cached__`, `__loader__` and `__package__` are set in the globals
    dictionary before the module code is executed. (Note that this is a
    minimal set of variables - other variables may be set implicitly as an
    interpreter implementation detail.)

    `__name__` is set to *run\_name* if this optional argument is not
    [`None`](constants.html#None "None") and to `'<run_path>'` otherwise.

    If *file\_path* directly references a script file (whether as source
    or as precompiled byte code), then `__file__` will be set to
    *file\_path*, and `__spec__`, `__cached__`, `__loader__` and
    `__package__` will all be set to [`None`](constants.html#None "None").

    If *file\_path* is a reference to a valid [`sys.path`](sys.html#sys.path "sys.path") entry, then
    `__spec__` will be set appropriately for the imported [`__main__`](__main__.html#module-__main__ "__main__: The environment where top-level code is run. Covers command-line interfaces, import-time behavior, and ``__name__ == '__main__'``.")
    module (that is, `__spec__.name` will always be `__main__`).
    `__file__`, `__cached__`, `__loader__` and `__package__` will be
    [set as normal](../reference/datamodel.html#import-mod-attrs) based on the module spec.

    A number of alterations are also made to the [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.") module. Firstly,
    [`sys.path`](sys.html#sys.path "sys.path") may be altered as described above. `sys.argv[0]` is updated
    with the value of *file\_path* and `sys.modules[__name__]` is updated
    with a temporary module object for the module being executed. All
    modifications to items in [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.") are reverted before the function
    returns.

    Note that, unlike [`run_module()`](#runpy.run_module "runpy.run_module"), the alterations made to [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.")
    are not optional in this function as these adjustments are essential to
    allowing the execution of [`sys.path`](sys.html#sys.path "sys.path") entries. As the thread-safety
    limitations still apply, use of this function in threaded code should be
    either serialised with the import lock or delegated to a separate process.

    See also

    [Interface options](../using/cmdline.html#using-on-interface-options) for equivalent functionality on the
    command line (`python path/to/script`).

    Changed in version 3.4: Updated to take advantage of the module spec feature added by
    [**PEP 451**](https://peps.python.org/pep-0451/). This allows `__cached__` to be set correctly in the
    case where `__main__` is imported from a valid [`sys.path`](sys.html#sys.path "sys.path") entry rather
    than being executed directly.

    Changed in version 3.12: The setting of `__cached__`, `__loader__`, and
    `__package__` are deprecated.