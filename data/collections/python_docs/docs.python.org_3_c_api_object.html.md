:   *Part of the [Stable ABI](stable.html#stable).*

    Return `1` if *inst* is an instance of the class *cls* or a subclass of
    *cls*, or `0` if not. On error, returns `-1` and sets an exception.

    If *cls* is a tuple, the check will be done against every entry in *cls*.
    The result will be `1` when at least one of the checks returns `1`,
    otherwise it will be `0`.

    If *cls* has a [`__instancecheck__()`](../reference/datamodel.html#type.__instancecheck__ "type.__instancecheck__") method, it will be called to
    determine the subclass status as described in [**PEP 3119**](https://peps.python.org/pep-3119/). Otherwise, *inst*
    is an instance of *cls* if its class is a subclass of *cls*.

    An instance *inst* can override what is considered its class by having a
    [`__class__`](../reference/datamodel.html#object.__class__ "object.__class__") attribute.

    An object *cls* can override if it is considered a class, and what its base
    classes are, by having a [`__bases__`](../reference/datamodel.html#type.__bases__ "type.__bases__") attribute (which must be a tuple
    of base classes).