Examples and Recipes
--------------------

This section describes some examples and recipes for making effective use of
the tools provided by [`contextlib`](#module-contextlib "contextlib: Utilities for with-statement contexts.").

### Supporting a variable number of context managers

The primary use case for [`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") is the one given in the class
documentation: supporting a variable number of context managers and other
cleanup operations in a single [`with`](../reference/compound_stmts.html#with) statement. The variability
may come from the number of context managers needed being driven by user
input (such as opening a user specified collection of files), or from
some of the context managers being optional:

Copy

```
with ExitStack() as stack:
    for resource in resources:
        stack.enter_context(resource)
    if need_special_resource():
        special = acquire_special_resource()
        stack.callback(release_special_resource, special)
    # Perform operations that use the acquired resources

```

As shown, [`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") also makes it quite easy to use [`with`](../reference/compound_stmts.html#with)
statements to manage arbitrary resources that don’t natively support the
context management protocol.

### Catching exceptions from `__enter__` methods

It is occasionally desirable to catch exceptions from an `__enter__`
method implementation, *without* inadvertently catching exceptions from
the [`with`](../reference/compound_stmts.html#with) statement body or the context manager’s `__exit__`
method. By using [`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") the steps in the context management
protocol can be separated slightly in order to allow this:

Copy

```
stack = ExitStack()
try:
    x = stack.enter_context(cm)
except Exception:
    # handle __enter__ exception
else:
    with stack:
        # Handle normal case

```

Actually needing to do this is likely to indicate that the underlying API
should be providing a direct resource management interface for use with
[`try`](../reference/compound_stmts.html#try)/[`except`](../reference/compound_stmts.html#except)/[`finally`](../reference/compound_stmts.html#finally) statements, but not
all APIs are well designed in that regard. When a context manager is the
only resource management API provided, then [`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") can make it
easier to handle various situations that can’t be handled directly in a
[`with`](../reference/compound_stmts.html#with) statement.

### Cleaning up in an `__enter__` implementation

As noted in the documentation of [`ExitStack.push()`](#contextlib.ExitStack.push "contextlib.ExitStack.push"), this
method can be useful in cleaning up an already allocated resource if later
steps in the [`__enter__()`](../reference/datamodel.html#object.__enter__ "object.__enter__") implementation fail.

Here’s an example of doing this for a context manager that accepts resource
acquisition and release functions, along with an optional validation function,
and maps them to the context management protocol:

Copy

```
from contextlib import contextmanager, AbstractContextManager, ExitStack

class ResourceManager(AbstractContextManager):

    def __init__(self, acquire_resource, release_resource, check_resource_ok=None):
        self.acquire_resource = acquire_resource
        self.release_resource = release_resource
        if check_resource_ok is None:
            def check_resource_ok(resource):
                return True
        self.check_resource_ok = check_resource_ok

    @contextmanager
    def _cleanup_on_error(self):
        with ExitStack() as stack:
            stack.push(self)
            yield
            # The validation check passed and didn't raise an exception
            # Accordingly, we want to keep the resource, and pass it
            # back to our caller
            stack.pop_all()

    def __enter__(self):
        resource = self.acquire_resource()
        with self._cleanup_on_error():
            if not self.check_resource_ok(resource):
                msg = "Failed validation for {!r}"
                raise RuntimeError(msg.format(resource))
        return resource

    def __exit__(self, *exc_details):
        # We don't need to duplicate any of our resource release logic
        self.release_resource()

```

### Replacing any use of `try-finally` and flag variables

A pattern you will sometimes see is a `try-finally` statement with a flag
variable to indicate whether or not the body of the `finally` clause should
be executed. In its simplest form (that can’t already be handled just by
using an `except` clause instead), it looks something like this:

Copy

```
cleanup_needed = True
try:
    result = perform_operation()
    if result:
        cleanup_needed = False
finally:
    if cleanup_needed:
        cleanup_resources()

```

As with any `try` statement based code, this can cause problems for
development and review, because the setup code and the cleanup code can end
up being separated by arbitrarily long sections of code.

[`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") makes it possible to instead register a callback for
execution at the end of a `with` statement, and then later decide to skip
executing that callback:

Copy

```
from contextlib import ExitStack

with ExitStack() as stack:
    stack.callback(cleanup_resources)
    result = perform_operation()
    if result:
        stack.pop_all()

```

This allows the intended cleanup behaviour to be made explicit up front,
rather than requiring a separate flag variable.

If a particular application uses this pattern a lot, it can be simplified
even further by means of a small helper class:

Copy

```
from contextlib import ExitStack

class Callback(ExitStack):
    def __init__(self, callback, /, *args, **kwds):
        super().__init__()
        self.callback(callback, *args, **kwds)

    def cancel(self):
        self.pop_all()

with Callback(cleanup_resources) as cb:
    result = perform_operation()
    if result:
        cb.cancel()

```

If the resource cleanup isn’t already neatly bundled into a standalone
function, then it is still possible to use the decorator form of
[`ExitStack.callback()`](#contextlib.ExitStack.callback "contextlib.ExitStack.callback") to declare the resource cleanup in
advance:

Copy

```
from contextlib import ExitStack

with ExitStack() as stack:
    @stack.callback
    def cleanup_resources():
        ...
    result = perform_operation()
    if result:
        stack.pop_all()

```

Due to the way the decorator protocol works, a callback function
declared this way cannot take any parameters. Instead, any resources to
be released must be accessed as closure variables.

### Using a context manager as a function decorator

[`ContextDecorator`](#contextlib.ContextDecorator "contextlib.ContextDecorator") makes it possible to use a context manager in
both an ordinary `with` statement and also as a function decorator.

For example, it is sometimes useful to wrap functions or groups of statements
with a logger that can track the time of entry and time of exit. Rather than
writing both a function decorator and a context manager for the task,
inheriting from [`ContextDecorator`](#contextlib.ContextDecorator "contextlib.ContextDecorator") provides both capabilities in a
single definition:

Copy

```
from contextlib import ContextDecorator
import logging

logging.basicConfig(level=logging.INFO)

class track_entry_and_exit(ContextDecorator):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        logging.info('Entering: %s', self.name)

    def __exit__(self, exc_type, exc, exc_tb):
        logging.info('Exiting: %s', self.name)

```

Instances of this class can be used as both a context manager:

Copy

```
with track_entry_and_exit('widget loader'):
    print('Some time consuming activity goes here')
    load_widget()

```

And also as a function decorator:

Copy

```
@track_entry_and_exit('widget loader')
def activity():
    print('Some time consuming activity goes here')
    load_widget()

```

Note that there is one additional limitation when using context managers
as function decorators: there’s no way to access the return value of
[`__enter__()`](../reference/datamodel.html#object.__enter__ "object.__enter__"). If that value is needed, then it is still necessary to use
an explicit `with` statement.

See also

[**PEP 343**](https://peps.python.org/pep-0343/) - The “with” statement
:   The specification, background, and examples for the Python [`with`](../reference/compound_stmts.html#with)
    statement.

Single use, reusable and reentrant context managers
---------------------------------------------------

Most context managers are written in a way that means they can only be
used effectively in a [`with`](../reference/compound_stmts.html#with) statement once. These single use
context managers must be created afresh each time they’re used -
attempting to use them a second time will trigger an exception or
otherwise not work correctly.

This common limitation means that it is generally advisable to create
context managers directly in the header of the [`with`](../reference/compound_stmts.html#with) statement
where they are used (as shown in all of the usage examples above).

Files are an example of effectively single use context managers, since
the first [`with`](../reference/compound_stmts.html#with) statement will close the file, preventing any
further IO operations using that file object.

Context managers created using [`contextmanager()`](#contextlib.contextmanager "contextlib.contextmanager") are also single use
context managers, and will complain about the underlying generator failing
to yield if an attempt is made to use them a second time:

Copy

```
>>> from contextlib import contextmanager
>>> @contextmanager
... def singleuse():
...     print("Before")
...     yield
...     print("After")
...
>>> cm = singleuse()
>>> with cm:
...     pass
...
Before
After
>>> with cm:
...     pass
...
Traceback (most recent call last):
    ...
RuntimeError: generator didn't yield

```

### Reentrant context managers

More sophisticated context managers may be “reentrant”. These context
managers can not only be used in multiple [`with`](../reference/compound_stmts.html#with) statements,
but may also be used *inside* a `with` statement that is already
using the same context manager.

[`threading.RLock`](threading.html#threading.RLock "threading.RLock") is an example of a reentrant context manager, as are
[`suppress()`](#contextlib.suppress "contextlib.suppress"), [`redirect_stdout()`](#contextlib.redirect_stdout "contextlib.redirect_stdout"), and [`chdir()`](#contextlib.chdir "contextlib.chdir"). Here’s a very
simple example of reentrant use:

Copy

```
>>> from contextlib import redirect_stdout
>>> from io import StringIO
>>> stream = StringIO()
>>> write_to_stream = redirect_stdout(stream)
>>> with write_to_stream:
...     print("This is written to the stream rather than stdout")
...     with write_to_stream:
...         print("This is also written to the stream")
...
>>> print("This is written directly to stdout")
This is written directly to stdout
>>> print(stream.getvalue())
This is written to the stream rather than stdout
This is also written to the stream

```

Real world examples of reentrancy are more likely to involve multiple
functions calling each other and hence be far more complicated than this
example.

Note also that being reentrant is *not* the same thing as being thread safe.
[`redirect_stdout()`](#contextlib.redirect_stdout "contextlib.redirect_stdout"), for example, is definitely not thread safe, as it
makes a global modification to the system state by binding [`sys.stdout`](sys.html#sys.stdout "sys.stdout")
to a different stream.

### Reusable context managers

Distinct from both single use and reentrant context managers are “reusable”
context managers (or, to be completely explicit, “reusable, but not
reentrant” context managers, since reentrant context managers are also
reusable). These context managers support being used multiple times, but
will fail (or otherwise not work correctly) if the specific context manager
instance has already been used in a containing with statement.

[`threading.Lock`](threading.html#threading.Lock "threading.Lock") is an example of a reusable, but not reentrant,
context manager (for a reentrant lock, it is necessary to use
[`threading.RLock`](threading.html#threading.RLock "threading.RLock") instead).

Another example of a reusable, but not reentrant, context manager is
[`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack"), as it invokes *all* currently registered callbacks
when leaving any with statement, regardless of where those callbacks
were added:

Copy

```
>>> from contextlib import ExitStack
>>> stack = ExitStack()
>>> with stack:
...     stack.callback(print, "Callback: from first context")
...     print("Leaving first context")
...
Leaving first context
Callback: from first context
>>> with stack:
...     stack.callback(print, "Callback: from second context")
...     print("Leaving second context")
...
Leaving second context
Callback: from second context
>>> with stack:
...     stack.callback(print, "Callback: from outer context")
...     with stack:
...         stack.callback(print, "Callback: from inner context")
...         print("Leaving inner context")
...     print("Leaving outer context")
...
Leaving inner context
Callback: from inner context
Callback: from outer context
Leaving outer context

```

As the output from the example shows, reusing a single stack object across
multiple with statements works correctly, but attempting to nest them
will cause the stack to be cleared at the end of the innermost with
statement, which is unlikely to be desirable behaviour.

Using separate [`ExitStack`](#contextlib.ExitStack "contextlib.ExitStack") instances instead of reusing a single
instance avoids that problem:

Copy

```
>>> from contextlib import ExitStack
>>> with ExitStack() as outer_stack:
...     outer_stack.callback(print, "Callback: from outer context")
...     with ExitStack() as inner_stack:
...         inner_stack.callback(print, "Callback: from inner context")
...         print("Leaving inner context")
...     print("Leaving outer context")
...
Leaving inner context
Callback: from inner context
Leaving outer context
Callback: from outer context

```