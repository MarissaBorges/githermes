Context Variables Objects
=========================

Changed in version 3.7.1:

Note

In Python 3.7.1 the signatures of all context variables
C APIs were **changed** to use [`PyObject`](structures.html#c.PyObject "PyObject") pointers instead
of [`PyContext`](#c.PyContext "PyContext"), [`PyContextVar`](#c.PyContextVar "PyContextVar"), and
[`PyContextToken`](#c.PyContextToken "PyContextToken"), e.g.:

```
// in 3.7.0:
PyContext *PyContext_New(void);

// in 3.7.1+:
PyObject *PyContext_New(void);

```

See [bpo-34762](https://bugs.python.org/issue?@action=redirect&bpo=34762) for more details.

This section details the public C API for the [`contextvars`](../library/contextvars.html#module-contextvars "contextvars: Context Variables") module.

type PyContext
:   The C structure used to represent a [`contextvars.Context`](../library/contextvars.html#contextvars.Context "contextvars.Context")
    object.

type PyContextVar
:   The C structure used to represent a [`contextvars.ContextVar`](../library/contextvars.html#contextvars.ContextVar "contextvars.ContextVar")
    object.

type PyContextToken
:   The C structure used to represent a [`contextvars.Token`](../library/contextvars.html#contextvars.Token "contextvars.Token") object.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyContext\_Type
:   The type object representing the *context* type.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyContextVar\_Type
:   The type object representing the *context variable* type.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyContextToken\_Type
:   The type object representing the *context variable token* type.

Type-check macros:

int PyContext\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is of type [`PyContext_Type`](#c.PyContext_Type "PyContext_Type"). *o* must not be
    `NULL`. This function always succeeds.

int PyContextVar\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is of type [`PyContextVar_Type`](#c.PyContextVar_Type "PyContextVar_Type"). *o* must not be
    `NULL`. This function always succeeds.

int PyContextToken\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*o)
:   Return true if *o* is of type [`PyContextToken_Type`](#c.PyContextToken_Type "PyContextToken_Type").
    *o* must not be `NULL`. This function always succeeds.

Context object management functions:

[PyObject](structures.html#c.PyObject "PyObject") \*PyContext\_New(void)
:   *Return value: New reference.*

    Create a new empty context object. Returns `NULL` if an error
    has occurred.

[PyObject](structures.html#c.PyObject "PyObject") \*PyContext\_Copy([PyObject](structures.html#c.PyObject "PyObject") \*ctx)
:   *Return value: New reference.*

    Create a shallow copy of the passed *ctx* context object.
    Returns `NULL` if an error has occurred.

[PyObject](structures.html#c.PyObject "PyObject") \*PyContext\_CopyCurrent(void)
:   *Return value: New reference.*

    Create a shallow copy of the current thread context.
    Returns `NULL` if an error has occurred.

int PyContext\_Enter([PyObject](structures.html#c.PyObject "PyObject") \*ctx)
:   Set *ctx* as the current context for the current thread.
    Returns `0` on success, and `-1` on error.

int PyContext\_Exit([PyObject](structures.html#c.PyObject "PyObject") \*ctx)
:   Deactivate the *ctx* context and restore the previous context as the
    current context for the current thread. Returns `0` on success,
    and `-1` on error.

Context variable functions:

[PyObject](structures.html#c.PyObject "PyObject") \*PyContextVar\_New(const char \*name, [PyObject](structures.html#c.PyObject "PyObject") \*def)
:   *Return value: New reference.*

    Create a new `ContextVar` object. The *name* parameter is used
    for introspection and debug purposes. The *def* parameter specifies
    a default value for the context variable, or `NULL` for no default.
    If an error has occurred, this function returns `NULL`.

int PyContextVar\_Get([PyObject](structures.html#c.PyObject "PyObject") \*var, [PyObject](structures.html#c.PyObject "PyObject") \*default\_value, [PyObject](structures.html#c.PyObject "PyObject") \*\*value)
:   Get the value of a context variable. Returns `-1` if an error has
    occurred during lookup, and `0` if no error occurred, whether or not
    a value was found.

    If the context variable was found, *value* will be a pointer to it.
    If the context variable was *not* found, *value* will point to:

    * *default\_value*, if not `NULL`;
    * the default value of *var*, if not `NULL`;
    * `NULL`

    Except for `NULL`, the function returns a new reference.

[PyObject](structures.html#c.PyObject "PyObject") \*PyContextVar\_Set([PyObject](structures.html#c.PyObject "PyObject") \*var, [PyObject](structures.html#c.PyObject "PyObject") \*value)
:   *Return value: New reference.*

    Set the value of *var* to *value* in the current context. Returns
    a new token object for this change, or `NULL` if an error has occurred.

int PyContextVar\_Reset([PyObject](structures.html#c.PyObject "PyObject") \*var, [PyObject](structures.html#c.PyObject "PyObject") \*token)
:   Reset the state of the *var* context variable to that it was in before
    [`PyContextVar_Set()`](#c.PyContextVar_Set "PyContextVar_Set") that returned the *token* was called.
    This function returns `0` on success and `-1` on error.