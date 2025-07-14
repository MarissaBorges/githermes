### Multi-phase initialization

An alternate way to specify extensions is to request “multi-phase initialization”.
Extension modules created this way behave more like Python modules: the
initialization is split between the *creation phase*, when the module object
is created, and the *execution phase*, when it is populated.
The distinction is similar to the [`__new__()`](../reference/datamodel.html#object.__new__ "object.__new__") and
[`__init__()`](../reference/datamodel.html#object.__init__ "object.__init__") methods of classes.

Unlike modules created using single-phase initialization, these modules are not
singletons.
For example, if the [`sys.modules`](../library/sys.html#sys.modules "sys.modules") entry is removed and the module
is re-imported, a new module object is created, and typically populated with
fresh method and type objects.
The old module is subject to normal garbage collection.
This mirrors the behavior of pure-Python modules.

Additional module instances may be created in
[sub-interpreters](init.html#sub-interpreter-support)
or after after Python runtime reinitialization
([`Py_Finalize()`](init.html#c.Py_Finalize "Py_Finalize") and [`Py_Initialize()`](init.html#c.Py_Initialize "Py_Initialize")).
In these cases, sharing Python objects between module instances would likely
cause crashes or undefined behavior.

To avoid such issues, each instance of an extension module should
be *isolated*: changes to one instance should not implicitly affect the others,
and all state, including references to Python objects, should be specific to
a particular module instance.
See [Isolating Extension Modules](../howto/isolating-extensions.html#isolating-extensions-howto) for more details and a practical guide.

A simpler way to avoid these issues is
[raising an error on repeated initialization](../howto/isolating-extensions.html#isolating-extensions-optout).

All modules created using multi-phase initialization are expected to support
[sub-interpreters](init.html#sub-interpreter-support), or otherwise explicitly
signal a lack of support.
This is usually achieved by isolation or blocking repeated initialization,
as above.
A module may also be limited to the main interpreter using
the [`Py_mod_multiple_interpreters`](#c.Py_mod_multiple_interpreters "Py_mod_multiple_interpreters") slot.

To request multi-phase initialization, the initialization function
(PyInit\_modulename) returns a [`PyModuleDef`](#c.PyModuleDef "PyModuleDef") instance with non-empty
[`m_slots`](#c.PyModuleDef.m_slots "PyModuleDef.m_slots"). Before it is returned, the `PyModuleDef`
instance must be initialized with the following function:

[PyObject](structures.html#c.PyObject "PyObject") \*PyModuleDef\_Init([PyModuleDef](#c.PyModuleDef "PyModuleDef") \*def)
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.5.*

    Ensures a module definition is a properly initialized Python object that
    correctly reports its type and reference count.

    Returns *def* cast to `PyObject*`, or `NULL` if an error occurred.

The *m\_slots* member of the module definition must point to an array of
`PyModuleDef_Slot` structures:

type PyModuleDef\_Slot
:   int slot
    :   A slot ID, chosen from the available values explained below.

    void \*value
    :   Value of the slot, whose meaning depends on the slot ID.

The *m\_slots* array must be terminated by a slot with id 0.

The available slot types are:

Py\_mod\_create
:   Specifies a function that is called to create the module object itself.
    The *value* pointer of this slot must point to a function of the signature:

    [PyObject](structures.html#c.PyObject "PyObject") \*create\_module([PyObject](structures.html#c.PyObject "PyObject") \*spec, [PyModuleDef](#c.PyModuleDef "PyModuleDef") \*def)

    The function receives a [`ModuleSpec`](../library/importlib.html#importlib.machinery.ModuleSpec "importlib.machinery.ModuleSpec")
    instance, as defined in [**PEP 451**](https://peps.python.org/pep-0451/), and the module definition.
    It should return a new module object, or set an error
    and return `NULL`.

    This function should be kept minimal. In particular, it should not
    call arbitrary Python code, as trying to import the same module again may
    result in an infinite loop.

    Multiple `Py_mod_create` slots may not be specified in one module
    definition.

    If `Py_mod_create` is not specified, the import machinery will create
    a normal module object using [`PyModule_New()`](#c.PyModule_New "PyModule_New"). The name is taken from
    *spec*, not the definition, to allow extension modules to dynamically adjust
    to their place in the module hierarchy and be imported under different
    names through symlinks, all while sharing a single module definition.

    There is no requirement for the returned object to be an instance of
    [`PyModule_Type`](#c.PyModule_Type "PyModule_Type"). Any type can be used, as long as it supports
    setting and getting import-related attributes.
    However, only `PyModule_Type` instances may be returned if the
    `PyModuleDef` has non-`NULL` `m_traverse`, `m_clear`,
    `m_free`; non-zero `m_size`; or slots other than `Py_mod_create`.

Py\_mod\_exec
:   Specifies a function that is called to *execute* the module.
    This is equivalent to executing the code of a Python module: typically,
    this function adds classes and constants to the module.
    The signature of the function is:

    int exec\_module([PyObject](structures.html#c.PyObject "PyObject") \*module)

    If multiple `Py_mod_exec` slots are specified, they are processed in the
    order they appear in the *m\_slots* array.

Py\_mod\_multiple\_interpreters
:   Specifies one of the following values:

    Py\_MOD\_MULTIPLE\_INTERPRETERS\_NOT\_SUPPORTED
    :   The module does not support being imported in subinterpreters.

    Py\_MOD\_MULTIPLE\_INTERPRETERS\_SUPPORTED
    :   The module supports being imported in subinterpreters,
        but only when they share the main interpreter’s GIL.
        (See [Isolating Extension Modules](../howto/isolating-extensions.html#isolating-extensions-howto).)

    Py\_MOD\_PER\_INTERPRETER\_GIL\_SUPPORTED
    :   The module supports being imported in subinterpreters,
        even when they have their own GIL.
        (See [Isolating Extension Modules](../howto/isolating-extensions.html#isolating-extensions-howto).)

    This slot determines whether or not importing this module
    in a subinterpreter will fail.

    Multiple `Py_mod_multiple_interpreters` slots may not be specified
    in one module definition.

    If `Py_mod_multiple_interpreters` is not specified, the import
    machinery defaults to `Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED`.

Py\_mod\_gil
:   Specifies one of the following values:

    Py\_MOD\_GIL\_USED
    :   The module depends on the presence of the global interpreter lock (GIL),
        and may access global state without synchronization.

    Py\_MOD\_GIL\_NOT\_USED
    :   The module is safe to run without an active GIL.

    This slot is ignored by Python builds not configured with
    [`--disable-gil`](../using/configure.html#cmdoption-disable-gil). Otherwise, it determines whether or not importing
    this module will cause the GIL to be automatically enabled. See
    [Free-threaded CPython](../whatsnew/3.13.html#whatsnew313-free-threaded-cpython) for more detail.

    Multiple `Py_mod_gil` slots may not be specified in one module definition.

    If `Py_mod_gil` is not specified, the import machinery defaults to
    `Py_MOD_GIL_USED`.

See [**PEP 489**](https://peps.python.org/pep-0489/) for more details on multi-phase initialization.