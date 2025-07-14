:   Resolve a name to an object.

    This functionality is used in numerous places in the standard library (see
    [bpo-12915](https://bugs.python.org/issue?@action=redirect&bpo=12915)) - and equivalent functionality is also in widely used
    third-party packages such as setuptools, Django and Pyramid.

    It is expected that *name* will be a string in one of the following
    formats, where W is shorthand for a valid Python identifier and dot stands
    for a literal period in these pseudo-regexes:

    The first form is intended for backward compatibility only. It assumes that
    some part of the dotted name is a package, and the rest is an object
    somewhere within that package, possibly nested inside other objects.
    Because the place where the package stops and the object hierarchy starts
    can’t be inferred by inspection, repeated attempts to import must be done
    with this form.

    In the second form, the caller makes the division point clear through the
    provision of a single colon: the dotted name to the left of the colon is a
    package to be imported, and the dotted name to the right is the object
    hierarchy within that package. Only one import is needed in this form. If
    it ends with the colon, then a module object is returned.

    The function will return an object (which might be a module), or raise one
    of the following exceptions:

    [`ValueError`](exceptions.html#ValueError "ValueError") – if *name* isn’t in a recognised format.

    [`ImportError`](exceptions.html#ImportError "ImportError") – if an import failed when it shouldn’t have.

    [`AttributeError`](exceptions.html#AttributeError "AttributeError") – If a failure occurred when traversing the object
    hierarchy within the imported package to get to the desired object.