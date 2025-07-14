### 3.4.3. Main Makefile targets

#### 3.4.3.1. make

For the most part, when rebuilding after editing some code or
refreshing your checkout from upstream, all you need to do is execute
`make`, which (per Make’s semantics) builds the default target, the
first one defined in the Makefile. By tradition (including in the
CPython project) this is usually the `all` target. The
`configure` script expands an `autoconf` variable,
`@DEF_MAKE_ALL_RULE@` to describe precisely which targets `make
all` will build. The three choices are:

* `profile-opt` (configured with `--enable-optimizations`)
* `build_wasm` (configured with `--with-emscripten-target`)
* `build_all` (configured without explicitly using either of the others)

Depending on the most recent source file changes, Make will rebuild
any targets (object files and executables) deemed out-of-date,
including running `configure` again if necessary. Source/target
dependencies are many and maintained manually however, so Make
sometimes doesn’t have all the information necessary to correctly
detect all targets which need to be rebuilt. Depending on which
targets aren’t rebuilt, you might experience a number of problems. If
you have build or test problems which you can’t otherwise explain,
`make clean && make` should work around most dependency problems, at
the expense of longer build times.

#### 3.4.3.2. make platform

Build the `python` program, but don’t build the standard library
extension modules. This generates a file named `platform` which
contains a single line describing the details of the build platform,
e.g., `macosx-14.3-arm64-3.12` or `linux-x86_64-3.13`.

#### 3.4.3.3. make profile-opt

Build Python using profile-guided optimization (PGO). You can use the
configure [`--enable-optimizations`](#cmdoption-enable-optimizations) option to make this the
default target of the `make` command (`make all` or just
`make`).

#### 3.4.3.4. make clean

Remove built files.

#### 3.4.3.5. make distclean

In addition to the work done by `make clean`, remove files
created by the configure script. `configure` will have to be run
before building again.

#### 3.4.3.6. make install

Build the `all` target and install Python.

#### 3.4.3.7. make test

Build the `all` target and run the Python test suite with the
`--fast-ci` option. Variables:

* `TESTOPTS`: additional regrtest command-line options.
* `TESTPYTHONOPTS`: additional Python command-line options.
* `TESTTIMEOUT`: timeout in seconds (default: 10 minutes).

#### 3.4.3.8. make buildbottest

This is similar to `make test`, but uses the `--slow-ci`
option and default timeout of 20 minutes, instead of `--fast-ci` option.

#### 3.4.3.9. make regen-all

Regenerate (almost) all generated files. These include (but are not
limited to) bytecode cases, and parser generator file.
`make regen-stdlib-module-names` and `autoconf` must be run
separately for the remaining [generated files](#generated-files).

### 3.4.4. C extensions

Some C extensions are built as built-in modules, like the `sys` module.
They are built with the `Py_BUILD_CORE_BUILTIN` macro defined.
Built-in modules have no `__file__` attribute:

Copy

```
>>> import sys
>>> sys
<module 'sys' (built-in)>
>>> sys.__file__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'sys' has no attribute '__file__'

```

Other C extensions are built as dynamic libraries, like the `_asyncio` module.
They are built with the `Py_BUILD_CORE_MODULE` macro defined.
Example on Linux x86-64:

Copy

```
>>> import _asyncio
>>> _asyncio
<module '_asyncio' from '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'>
>>> _asyncio.__file__
'/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'

```

`Modules/Setup` is used to generate Makefile targets to build C extensions.
At the beginning of the files, C extensions are built as built-in modules.
Extensions defined after the `*shared*` marker are built as dynamic libraries.

The `PyAPI_FUNC()`, `PyAPI_DATA()` and
[`PyMODINIT_FUNC`](../c-api/intro.html#c.PyMODINIT_FUNC "PyMODINIT_FUNC") macros of `Include/exports.h` are defined
differently depending if the `Py_BUILD_CORE_MODULE` macro is defined:

If the `Py_BUILD_CORE_BUILTIN` macro is used by mistake on a C extension
built as a shared library, its `PyInit_xxx()` function is not exported,
causing an [`ImportError`](../library/exceptions.html#ImportError "ImportError") on import.