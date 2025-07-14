:   *Part of the [Stable ABI](stable.html#stable) since version 3.12.*

    Create and return a [heap type](typeobj.html#heap-types) from the *spec*
    (see [`Py_TPFLAGS_HEAPTYPE`](typeobj.html#c.Py_TPFLAGS_HEAPTYPE "Py_TPFLAGS_HEAPTYPE")).

    The metaclass *metaclass* is used to construct the resulting type object.
    When *metaclass* is `NULL`, the metaclass is derived from *bases*
    (or *Py\_tp\_base[s]* slots if *bases* is `NULL`, see below).

    Metaclasses that override [`tp_new`](typeobj.html#c.PyTypeObject.tp_new "PyTypeObject.tp_new") are not
    supported, except if `tp_new` is `NULL`.
    (For backwards compatibility, other `PyType_From*` functions allow
    such metaclasses. They ignore `tp_new`, which may result in incomplete
    initialization. This is deprecated and in Python 3.14+ such metaclasses will
    not be supported.)

    The *bases* argument can be used to specify base classes; it can either
    be only one class or a tuple of classes.
    If *bases* is `NULL`, the *Py\_tp\_bases* slot is used instead.
    If that also is `NULL`, the *Py\_tp\_base* slot is used instead.
    If that also is `NULL`, the new type derives from [`object`](../library/functions.html#object "object").

    The *module* argument can be used to record the module in which the new
    class is defined. It must be a module object or `NULL`.
    If not `NULL`, the module is associated with the new type and can later be
    retrieved with [`PyType_GetModule()`](#c.PyType_GetModule "PyType_GetModule").
    The associated module is not inherited by subclasses; it must be specified
    for each class individually.

    This function calls [`PyType_Ready()`](#c.PyType_Ready "PyType_Ready") on the new type.

    Note that this function does *not* fully match the behavior of
    calling [`type()`](../library/functions.html#type "type") or using the [`class`](../reference/compound_stmts.html#class) statement.
    With user-provided base types or metaclasses, prefer
    [calling](call.html#capi-call) [`type`](../library/functions.html#type "type") (or the metaclass)
    over `PyType_From*` functions.
    Specifically: