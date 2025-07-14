6. Using Python on Android
==========================

Python on Android is unlike Python on desktop platforms. On a desktop platform,
Python is generally installed as a system resource that can be used by any user
of that computer. Users then interact with Python by running a **python**
executable and entering commands at an interactive prompt, or by running a
Python script.

On Android, there is no concept of installing as a system resource. The only unit
of software distribution is an “app”. There is also no console where you could
run a **python** executable, or interact with a Python REPL.

As a result, the only way you can use Python on Android is in embedded mode – that
is, by writing a native Android application, embedding a Python interpreter
using `libpython`, and invoking Python code using the [Python embedding
API](../extending/embedding.html#embedding). The full Python interpreter, the standard library, and all
your Python code is then packaged into your app for its own private use.

The Python standard library has some notable omissions and restrictions on
Android. See the [API availability guide](../library/intro.html#mobile-availability) for
details.

6.1. Adding Python to an Android app
------------------------------------

Most app developers should use one of the following tools, which will provide a
much easier experience:

If you’re sure you want to do all of this manually, read on. You can use the
[testbed app](https://github.com/python/cpython/tree/3.13/Android/testbed) as a guide; each step below contains a
link to the relevant file.

6.2. Building a Python package for Android
------------------------------------------

Python packages can be built for Android as wheels and released on PyPI. The
recommended tool for doing this is [cibuildwheel](https://cibuildwheel.pypa.io/en/stable/platforms/#android), which automates
all the details of setting up a cross-compilation environment, building the
wheel, and testing it on an emulator.