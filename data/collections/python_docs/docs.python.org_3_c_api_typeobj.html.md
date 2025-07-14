:   These fields allow calculating the size in bytes of instances of the type.

    There are two kinds of types: types with fixed-length instances have a zero
    `tp_itemsize` field, types with variable-length instances have a non-zero
    `tp_itemsize` field. For a type with fixed-length instances, all
    instances have the same size, given in `tp_basicsize`.
    (Exceptions to this rule can be made using
    [`PyUnstable_Object_GC_NewWithExtraData()`](gcsupport.html#c.PyUnstable_Object_GC_NewWithExtraData "PyUnstable_Object_GC_NewWithExtraData").)

    For a type with variable-length instances, the instances must have an
    [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") field, and the instance size is
    `tp_basicsize` plus N times `tp_itemsize`,
    where N is the “length” of the object.

    Functions like [`PyObject_NewVar()`](allocation.html#c.PyObject_NewVar "PyObject_NewVar") will take the value of N as an
    argument, and store in the instance’s [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") field.
    Note that the [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") field may later be used for
    other purposes. For example, [`int`](../library/functions.html#int "int") instances use the bits of
    [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") in an implementation-defined
    way; the underlying storage and its size should be accessed using
    `PyLong_Export()`.

    Also, the presence of an [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") field in the
    instance layout doesn’t mean that the instance structure is variable-length.
    For example, the [`list`](../library/stdtypes.html#list "list") type has fixed-length instances, yet those
    instances have a [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") field.
    (As with [`int`](../library/functions.html#int "int"), avoid reading lists’ `ob_size` directly.
    Call [`PyList_Size()`](list.html#c.PyList_Size "PyList_Size") instead.)

    The `tp_basicsize` includes size needed for data of the type’s
    [`tp_base`](#c.PyTypeObject.tp_base "PyTypeObject.tp_base"), plus any extra data needed
    by each instance.

    The correct way to set `tp_basicsize` is to use the
    `sizeof` operator on the struct used to declare the instance layout.
    This struct must include the struct used to declare the base type.
    In other words, `tp_basicsize` must be greater than or equal
    to the base’s `tp_basicsize`.

    Since every type is a subtype of [`object`](../library/functions.html#object "object"), this struct must
    include [`PyObject`](structures.html#c.PyObject "PyObject") or [`PyVarObject`](structures.html#c.PyVarObject "PyVarObject") (depending on
    whether [`ob_size`](#c.PyVarObject.ob_size "PyVarObject.ob_size") should be included). These are
    usually defined by the macro [`PyObject_HEAD`](structures.html#c.PyObject_HEAD "PyObject_HEAD") or
    [`PyObject_VAR_HEAD`](structures.html#c.PyObject_VAR_HEAD "PyObject_VAR_HEAD"), respectively.

    The basic size does not include the GC header size, as that header is not
    part of [`PyObject_HEAD`](structures.html#c.PyObject_HEAD "PyObject_HEAD").

    For cases where struct used to declare the base type is unknown,
    see [`PyType_Spec.basicsize`](type.html#c.PyType_Spec.basicsize "PyType_Spec.basicsize") and [`PyType_FromMetaclass()`](type.html#c.PyType_FromMetaclass "PyType_FromMetaclass").

    Notes about alignment:

    * `tp_basicsize` must be a multiple of `_Alignof(PyObject)`.
      When using `sizeof` on a `struct` that includes
      [`PyObject_HEAD`](structures.html#c.PyObject_HEAD "PyObject_HEAD"), as recommended, the compiler ensures this.
      When not using a C `struct`, or when using compiler
      extensions like `__attribute__((packed))`, it is up to you.
    * If the variable items require a particular alignment,
      `tp_basicsize` and `tp_itemsize` must each be a
      multiple of that alignment.
      For example, if a type’s variable part stores a `double`, it is
      your responsibility that both fields are a multiple of
      `_Alignof(double)`.

    **Inheritance:**

    These fields are inherited separately by subtypes.
    (That is, if the field is set to zero, [`PyType_Ready()`](type.html#c.PyType_Ready "PyType_Ready") will copy
    the value from the base type, indicating that the instances do not
    need additional storage.)

    If the base type has a non-zero [`tp_itemsize`](#c.PyTypeObject.tp_itemsize "PyTypeObject.tp_itemsize"), it is generally not safe to set
    [`tp_itemsize`](#c.PyTypeObject.tp_itemsize "PyTypeObject.tp_itemsize") to a different non-zero value in a subtype (though this
    depends on the implementation of the base type).