`types` — Dynamic type creation and names for built-in types
============================================================

**Source code:** [Lib/types.py](https://github.com/python/cpython/tree/3.13/Lib/types.py)

---

This module defines utility functions to assist in dynamic creation of
new types.

It also defines names for some object types that are used by the standard
Python interpreter, but not exposed as builtins like [`int`](functions.html#int "int") or
[`str`](stdtypes.html#str "str") are.

Finally, it provides some additional type-related utility classes and functions
that are not fundamental enough to be builtins.

Dynamic Type Creation
---------------------

types.new\_class(*name*, *bases=()*, *kwds=None*, *exec\_body=None*)
:   Creates a class object dynamically using the appropriate metaclass.

    The first three arguments are the components that make up a class
    definition header: the class name, the base classes (in order), the
    keyword arguments (such as `metaclass`).

    The *exec\_body* argument is a callback that is used to populate the
    freshly created class namespace. It should accept the class namespace
    as its sole argument and update the namespace directly with the class
    contents. If no callback is provided, it has the same effect as passing
    in `lambda ns: None`.

types.prepare\_class(*name*, *bases=()*, *kwds=None*)
:   Calculates the appropriate metaclass and creates the class namespace.

    The arguments are the components that make up a class definition header:
    the class name, the base classes (in order) and the keyword arguments
    (such as `metaclass`).

    The return value is a 3-tuple: `metaclass, namespace, kwds`

    *metaclass* is the appropriate metaclass, *namespace* is the
    prepared class namespace and *kwds* is an updated copy of the passed
    in *kwds* argument with any `'metaclass'` entry removed. If no *kwds*
    argument is passed in, this will be an empty dict.

    Changed in version 3.6: The default value for the `namespace` element of the returned
    tuple has changed. Now an insertion-order-preserving mapping is
    used when the metaclass does not have a `__prepare__` method.

See also

[Metaclasses](../reference/datamodel.html#metaclasses)
:   Full details of the class creation process supported by these functions

[**PEP 3115**](https://peps.python.org/pep-3115/) - Metaclasses in Python 3000
:   Introduced the `__prepare__` namespace hook

types.resolve\_bases(*bases*)
:   Resolve MRO entries dynamically as specified by [**PEP 560**](https://peps.python.org/pep-0560/).

    This function looks for items in *bases* that are not instances of
    [`type`](functions.html#type "type"), and returns a tuple where each such object that has
    an [`__mro_entries__()`](../reference/datamodel.html#object.__mro_entries__ "object.__mro_entries__") method is replaced with an unpacked result of
    calling this method. If a *bases* item is an instance of [`type`](functions.html#type "type"),
    or it doesn’t have an `__mro_entries__()` method, then it is included in
    the return tuple unchanged.

types.get\_original\_bases(*cls*, */*)
:   Return the tuple of objects originally given as the bases of *cls* before
    the [`__mro_entries__()`](../reference/datamodel.html#object.__mro_entries__ "object.__mro_entries__") method has been called on any bases
    (following the mechanisms laid out in [**PEP 560**](https://peps.python.org/pep-0560/)). This is useful for
    introspecting [Generics](typing.html#user-defined-generics).

    For classes that have an `__orig_bases__` attribute, this
    function returns the value of `cls.__orig_bases__`.
    For classes without the `__orig_bases__` attribute,
    [`cls.__bases__`](../reference/datamodel.html#type.__bases__ "type.__bases__") is returned.

    Examples:

    Copy

    ```
    from typing import TypeVar, Generic, NamedTuple, TypedDict

    T = TypeVar("T")
    class Foo(Generic[T]): ...
    class Bar(Foo[int], float): ...
    class Baz(list[str]): ...
    Eggs = NamedTuple("Eggs", [("a", int), ("b", str)])
    Spam = TypedDict("Spam", {"a": int, "b": str})

    assert Bar.__bases__ == (Foo, float)
    assert get_original_bases(Bar) == (Foo[int], float)

    assert Baz.__bases__ == (list,)
    assert get_original_bases(Baz) == (list[str],)

    assert Eggs.__bases__ == (tuple,)
    assert get_original_bases(Eggs) == (NamedTuple,)

    assert Spam.__bases__ == (dict,)
    assert get_original_bases(Spam) == (TypedDict,)

    assert int.__bases__ == (object,)
    assert get_original_bases(int) == (object,)

    ```

See also

[**PEP 560**](https://peps.python.org/pep-0560/) - Core support for typing module and generic types

Standard Interpreter Types
--------------------------

This module provides names for many of the types that are required to
implement a Python interpreter. It deliberately avoids including some of
the types that arise only incidentally during processing such as the
`listiterator` type.

Typical use of these names is for [`isinstance()`](functions.html#isinstance "isinstance") or
[`issubclass()`](functions.html#issubclass "issubclass") checks.

If you instantiate any of these types, note that signatures may vary between Python versions.

Standard names are defined for the following types:

types.NoneType
:   The type of [`None`](constants.html#None "None").

types.FunctionType

types.LambdaType
:   The type of user-defined functions and functions created by
    [`lambda`](../reference/expressions.html#lambda) expressions.

    Raises an [auditing event](sys.html#auditing) `function.__new__` with argument `code`.

    The audit event only occurs for direct instantiation of function objects,
    and is not raised for normal compilation.

types.GeneratorType
:   The type of [generator](../glossary.html#term-generator)-iterator objects, created by
    generator functions.

types.CoroutineType
:   The type of [coroutine](../glossary.html#term-coroutine) objects, created by
    [`async def`](../reference/compound_stmts.html#async-def) functions.

types.AsyncGeneratorType
:   The type of [asynchronous generator](../glossary.html#term-asynchronous-generator)-iterator objects, created by
    asynchronous generator functions.

*class* types.CodeType(*\*\*kwargs*)
:   The type of [code objects](../reference/datamodel.html#code-objects) such as returned by [`compile()`](functions.html#compile "compile").

    Raises an [auditing event](sys.html#auditing) `code.__new__` with arguments `code`, `filename`, `name`, `argcount`, `posonlyargcount`, `kwonlyargcount`, `nlocals`, `stacksize`, `flags`.

    Note that the audited arguments may not match the names or positions
    required by the initializer. The audit event only occurs for direct
    instantiation of code objects, and is not raised for normal compilation.

types.CellType
:   The type for cell objects: such objects are used as containers for
    a function’s [closure variables](../glossary.html#term-closure-variable).

types.MethodType
:   The type of methods of user-defined class instances.

types.BuiltinFunctionType

types.BuiltinMethodType
:   The type of built-in functions like [`len()`](functions.html#len "len") or [`sys.exit()`](sys.html#sys.exit "sys.exit"), and
    methods of built-in classes. (Here, the term “built-in” means “written in
    C”.)

types.WrapperDescriptorType
:   The type of methods of some built-in data types and base classes such as
    [`object.__init__()`](../reference/datamodel.html#object.__init__ "object.__init__") or [`object.__lt__()`](../reference/datamodel.html#object.__lt__ "object.__lt__").

types.MethodWrapperType
:   The type of *bound* methods of some built-in data types and base classes.
    For example it is the type of `object().__str__`.

types.NotImplementedType
:   The type of [`NotImplemented`](constants.html#NotImplemented "NotImplemented").

types.MethodDescriptorType
:   The type of methods of some built-in data types such as [`str.join()`](stdtypes.html#str.join "str.join").

types.ClassMethodDescriptorType
:   The type of *unbound* class methods of some built-in data types such as
    `dict.__dict__['fromkeys']`.

*class* types.ModuleType(*name*, *doc=None*)
:   The type of [modules](../glossary.html#term-module). The constructor takes the name of the
    module to be created and optionally its [docstring](../glossary.html#term-docstring).

    See also

    [Documentation on module objects](../reference/datamodel.html#module-objects)
    :   Provides details on the special attributes that can be found on
        instances of `ModuleType`.

    [`importlib.util.module_from_spec()`](importlib.html#importlib.util.module_from_spec "importlib.util.module_from_spec")
    :   Modules created using the `ModuleType` constructor are
        created with many of their special attributes unset or set to default
        values. `module_from_spec()` provides a more robust way of
        creating `ModuleType` instances which ensures the various
        attributes are set appropriately.

types.EllipsisType
:   The type of [`Ellipsis`](constants.html#Ellipsis "Ellipsis").

*class* types.GenericAlias(*t\_origin*, *t\_args*)
:   The type of [parameterized generics](stdtypes.html#types-genericalias) such as
    `list[int]`.

    `t_origin` should be a non-parameterized generic class, such as `list`,
    `tuple` or `dict`. `t_args` should be a [`tuple`](stdtypes.html#tuple "tuple") (possibly of
    length 1) of types which parameterize `t_origin`:

    Copy

    ```
    >>> from types import GenericAlias

    >>> list[int] == GenericAlias(list, (int,))
    True
    >>> dict[str, int] == GenericAlias(dict, (str, int))
    True

    ```

    Changed in version 3.9.2: This type can now be subclassed.

    See also

    [Generic Alias Types](stdtypes.html#types-genericalias)
    :   In-depth documentation on instances of `types.GenericAlias`

    [**PEP 585**](https://peps.python.org/pep-0585/) - Type Hinting Generics In Standard Collections
    :   Introducing the `types.GenericAlias` class

*class* types.UnionType
:   The type of [union type expressions](stdtypes.html#types-union).

*class* types.TracebackType(*tb\_next*, *tb\_frame*, *tb\_lasti*, *tb\_lineno*)
:   The type of traceback objects such as found in `sys.exception().__traceback__`.

    See [the language reference](../reference/datamodel.html#traceback-objects) for details of the
    available attributes and operations, and guidance on creating tracebacks
    dynamically.

types.FrameType
:   The type of [frame objects](../reference/datamodel.html#frame-objects) such as found in
    [`tb.tb_frame`](../reference/datamodel.html#traceback.tb_frame "traceback.tb_frame") if `tb` is a traceback object.

types.GetSetDescriptorType
:   The type of objects defined in extension modules with `PyGetSetDef`, such
    as [`FrameType.f_locals`](../reference/datamodel.html#frame.f_locals "frame.f_locals") or `array.array.typecode`.
    This type is used as
    descriptor for object attributes; it has the same purpose as the
    [`property`](functions.html#property "property") type, but for classes defined in extension modules.

types.MemberDescriptorType
:   The type of objects defined in extension modules with `PyMemberDef`, such
    as `datetime.timedelta.days`. This type is used as descriptor for simple C
    data members which use standard conversion functions; it has the same purpose
    as the [`property`](functions.html#property "property") type, but for classes defined in extension modules.

    In addition, when a class is defined with a [`__slots__`](../reference/datamodel.html#object.__slots__ "object.__slots__") attribute, then for
    each slot, an instance of `MemberDescriptorType` will be added as an attribute
    on the class. This allows the slot to appear in the class’s [`__dict__`](../reference/datamodel.html#type.__dict__ "type.__dict__").

    **CPython implementation detail:** In other implementations of Python, this type may be identical to
    `GetSetDescriptorType`.

*class* types.MappingProxyType(*mapping*)
:   Read-only proxy of a mapping. It provides a dynamic view on the mapping’s
    entries, which means that when the mapping changes, the view reflects these
    changes.

    Changed in version 3.9: Updated to support the new union (`|`) operator from [**PEP 584**](https://peps.python.org/pep-0584/), which
    simply delegates to the underlying mapping.

    key in proxy
    :   Return `True` if the underlying mapping has a key *key*, else
        `False`.

    proxy[key]
    :   Return the item of the underlying mapping with key *key*. Raises a
        [`KeyError`](exceptions.html#KeyError "KeyError") if *key* is not in the underlying mapping.

    iter(proxy)
    :   Return an iterator over the keys of the underlying mapping. This is a
        shortcut for `iter(proxy.keys())`.

    len(proxy)
    :   Return the number of items in the underlying mapping.

    copy()
    :   Return a shallow copy of the underlying mapping.

    get(*key*[, *default*])
    :   Return the value for *key* if *key* is in the underlying mapping, else
        *default*. If *default* is not given, it defaults to `None`, so that
        this method never raises a [`KeyError`](exceptions.html#KeyError "KeyError").

    items()
    :   Return a new view of the underlying mapping’s items (`(key, value)`
        pairs).

    keys()
    :   Return a new view of the underlying mapping’s keys.

    values()
    :   Return a new view of the underlying mapping’s values.

    reversed(proxy)
    :   Return a reverse iterator over the keys of the underlying mapping.

    hash(proxy)
    :   Return a hash of the underlying mapping.

*class* types.CapsuleType
:   The type of [capsule objects](../c-api/capsule.html#capsules).

Additional Utility Classes and Functions
----------------------------------------

*class* types.SimpleNamespace
:   A simple [`object`](functions.html#object "object") subclass that provides attribute access to its
    namespace, as well as a meaningful repr.

    Unlike [`object`](functions.html#object "object"), with `SimpleNamespace` you can add and remove
    attributes.

    [`SimpleNamespace`](#types.SimpleNamespace "types.SimpleNamespace") objects may be initialized
    in the same way as [`dict`](stdtypes.html#dict "dict"): either with keyword arguments,
    with a single positional argument, or with both.
    When initialized with keyword arguments,
    those are directly added to the underlying namespace.
    Alternatively, when initialized with a positional argument,
    the underlying namespace will be updated with key-value pairs
    from that argument (either a mapping object or
    an [iterable](../glossary.html#term-iterable) object producing key-value pairs).
    All such keys must be strings.

    The type is roughly equivalent to the following code:

    Copy

    ```
    class SimpleNamespace:
        def __init__(self, mapping_or_iterable=(), /, **kwargs):
            self.__dict__.update(mapping_or_iterable)
            self.__dict__.update(kwargs)

        def __repr__(self):
            items = (f"{k}={v!r}" for k, v in self.__dict__.items())
            return "{}({})".format(type(self).__name__, ", ".join(items))

        def __eq__(self, other):
            if isinstance(self, SimpleNamespace) and isinstance(other, SimpleNamespace):
               return self.__dict__ == other.__dict__
            return NotImplemented

    ```

    `SimpleNamespace` may be useful as a replacement for `class NS: pass`.
    However, for a structured record type use [`namedtuple()`](collections.html#collections.namedtuple "collections.namedtuple")
    instead.

    `SimpleNamespace` objects are supported by [`copy.replace()`](copy.html#copy.replace "copy.replace").

    Changed in version 3.9: Attribute order in the repr changed from alphabetical to insertion (like
    `dict`).

    Changed in version 3.13: Added support for an optional positional argument.

types.DynamicClassAttribute(*fget=None*, *fset=None*, *fdel=None*, *doc=None*)
:   Route attribute access on a class to \_\_getattr\_\_.

    This is a descriptor, used to define attributes that act differently when
    accessed through an instance and through a class. Instance access remains
    normal, but access to an attribute through a class will be routed to the
    class’s \_\_getattr\_\_ method; this is done by raising AttributeError.

    This allows one to have properties active on an instance, and have virtual
    attributes on the class with the same name (see [`enum.Enum`](enum.html#enum.Enum "enum.Enum") for an example).

Coroutine Utility Functions
---------------------------

types.coroutine(*gen\_func*)
:   This function transforms a [generator](../glossary.html#term-generator) function into a
    [coroutine function](../glossary.html#term-coroutine-function) which returns a generator-based coroutine.
    The generator-based coroutine is still a [generator iterator](../glossary.html#term-generator-iterator),
    but is also considered to be a [coroutine](../glossary.html#term-coroutine) object and is
    [awaitable](../glossary.html#term-awaitable). However, it may not necessarily implement
    the [`__await__()`](../reference/datamodel.html#object.__await__ "object.__await__") method.

    If *gen\_func* is a generator function, it will be modified in-place.

    If *gen\_func* is not a generator function, it will be wrapped. If it
    returns an instance of [`collections.abc.Generator`](collections.abc.html#collections.abc.Generator "collections.abc.Generator"), the instance
    will be wrapped in an *awaitable* proxy object. All other types
    of objects will be returned as is.