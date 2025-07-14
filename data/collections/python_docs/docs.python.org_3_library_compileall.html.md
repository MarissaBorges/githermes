:   Recursively descend the directory tree named by *dir*, compiling all `.py`
    files along the way. Return a true value if all the files compiled successfully,
    and a false value otherwise.

    The *maxlevels* parameter is used to limit the depth of the recursion; it
    defaults to `sys.getrecursionlimit()`.

    If *ddir* is given, it is prepended to the path to each file being compiled
    for use in compilation time tracebacks, and is also compiled in to the
    byte-code file, where it will be used in tracebacks and other messages in
    cases where the source file does not exist at the time the byte-code file is
    executed.

    If *force* is true, modules are re-compiled even if the timestamps are up to
    date.

    If *rx* is given, its `search` method is called on the complete path to each
    file considered for compilation, and if it returns a true value, the file
    is skipped. This can be used to exclude files matching a regular expression,
    given as a [re.Pattern](re.html#re-objects) object.

    If *quiet* is `False` or `0` (the default), the filenames and other
    information are printed to standard out. Set to `1`, only errors are
    printed. Set to `2`, all output is suppressed.

    If *legacy* is true, byte-code files are written to their legacy locations
    and names, which may overwrite byte-code files created by another version of
    Python. The default is to write files to their [**PEP 3147**](https://peps.python.org/pep-3147/) locations and
    names, which allows byte-code files from multiple versions of Python to
    coexist.

    *optimize* specifies the optimization level for the compiler. It is passed to
    the built-in [`compile()`](functions.html#compile "compile") function. Accepts also a sequence of optimization
    levels which lead to multiple compilations of one `.py` file in one call.

    The argument *workers* specifies how many workers are used to
    compile files in parallel. The default is to not use multiple workers.
    If the platform can’t use multiple workers and *workers* argument is given,
    then sequential compilation will be used as a fallback. If *workers*
    is 0, the number of cores in the system is used. If *workers* is
    lower than `0`, a [`ValueError`](exceptions.html#ValueError "ValueError") will be raised.

    *invalidation\_mode* should be a member of the
    [`py_compile.PycInvalidationMode`](py_compile.html#py_compile.PycInvalidationMode "py_compile.PycInvalidationMode") enum and controls how the generated
    pycs are invalidated at runtime.

    The *stripdir*, *prependdir* and *limit\_sl\_dest* arguments correspond to
    the `-s`, `-p` and `-e` options described above.
    They may be specified as `str` or [`os.PathLike`](os.html#os.PathLike "os.PathLike").

    If *hardlink\_dupes* is true and two `.pyc` files with different optimization
    level have the same content, use hard links to consolidate duplicate files.

    Changed in version 3.2: Added the *legacy* and *optimize* parameter.

    Changed in version 3.5: Added the *workers* parameter.

    Changed in version 3.5: *quiet* parameter was changed to a multilevel value.

    Changed in version 3.5: The *legacy* parameter only writes out `.pyc` files, not `.pyo` files
    no matter what the value of *optimize* is.

    Changed in version 3.7: The *invalidation\_mode* parameter was added.

    Changed in version 3.7.2: The *invalidation\_mode* parameter’s default value is updated to `None`.

    Changed in version 3.8: Setting *workers* to 0 now chooses the optimal number of cores.

    Changed in version 3.9: Added *stripdir*, *prependdir*, *limit\_sl\_dest* and *hardlink\_dupes* arguments.
    Default value of *maxlevels* was changed from `10` to `sys.getrecursionlimit()`