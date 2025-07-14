:   Extensible JSON encoder for Python data structures.

    Supports the following objects and types by default:

    | Python | JSON |
    | --- | --- |
    | dict | object |
    | list, tuple | array |
    | str | string |
    | int, float, int- & float-derived Enums | number |
    | True | true |
    | False | false |
    | None | null |

    Changed in version 3.4: Added support for int- and float-derived Enum classes.

    To extend this to recognize other objects, subclass and implement a
    [`default()`](#json.JSONEncoder.default "json.JSONEncoder.default") method with another method that returns a serializable object
    for `o` if possible, otherwise it should call the superclass implementation
    (to raise [`TypeError`](exceptions.html#TypeError "TypeError")).

    If *skipkeys* is false (the default), a [`TypeError`](exceptions.html#TypeError "TypeError") will be raised when
    trying to encode keys that are not [`str`](stdtypes.html#str "str"), [`int`](functions.html#int "int"), [`float`](functions.html#float "float"),
    [`bool`](functions.html#bool "bool") or `None`. If *skipkeys* is true, such items are simply skipped.

    If *ensure\_ascii* is true (the default), the output is guaranteed to
    have all incoming non-ASCII characters escaped. If *ensure\_ascii* is
    false, these characters will be output as-is.

    If *check\_circular* is true (the default), then lists, dicts, and custom
    encoded objects will be checked for circular references during encoding to
    prevent an infinite recursion (which would cause a [`RecursionError`](exceptions.html#RecursionError "RecursionError")).
    Otherwise, no such check takes place.

    If *allow\_nan* is true (the default), then `NaN`, `Infinity`, and
    `-Infinity` will be encoded as such. This behavior is not JSON
    specification compliant, but is consistent with most JavaScript based
    encoders and decoders. Otherwise, it will be a [`ValueError`](exceptions.html#ValueError "ValueError") to encode
    such floats.

    If *sort\_keys* is true (default: `False`), then the output of dictionaries
    will be sorted by key; this is useful for regression tests to ensure that
    JSON serializations can be compared on a day-to-day basis.

    If *indent* is a non-negative integer or string, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent level
    of 0, negative, or `""` will only insert newlines. `None` (the default)
    selects the most compact representation. Using a positive integer indent
    indents that many spaces per level. If *indent* is a string (such as `"\t"`),
    that string is used to indent each level.

    Changed in version 3.2: Allow strings for *indent* in addition to integers.

    If specified, *separators* should be an `(item_separator, key_separator)`
    tuple. The default is `(', ', ': ')` if *indent* is `None` and
    `(',', ': ')` otherwise. To get the most compact JSON representation,
    you should specify `(',', ':')` to eliminate whitespace.

    Changed in version 3.4: Use `(',', ': ')` as default if *indent* is not `None`.

    If specified, *default* should be a function that gets called for objects that
    can’t otherwise be serialized. It should return a JSON encodable version of
    the object or raise a [`TypeError`](exceptions.html#TypeError "TypeError"). If not specified, [`TypeError`](exceptions.html#TypeError "TypeError")
    is raised.

    Changed in version 3.6: All parameters are now [keyword-only](../glossary.html#keyword-only-parameter).

    default(*o*)
    :   Implement this method in a subclass such that it returns a serializable
        object for *o*, or calls the base implementation (to raise a
        [`TypeError`](exceptions.html#TypeError "TypeError")).

        For example, to support arbitrary iterators, you could implement
        [`default()`](#json.JSONEncoder.default "json.JSONEncoder.default") like this:

        Copy

        ```
        def default(self, o):
           try:
               iterable = iter(o)
           except TypeError:
               pass
           else:
               return list(iterable)
           # Let the base class default method raise the TypeError
           return super().default(o)

        ```

    encode(*o*)
    :   Return a JSON string representation of a Python data structure, *o*. For
        example:

        Copy

        ```
        >>> json.JSONEncoder().encode({"foo": ["bar", "baz"]})
        '{"foo": ["bar", "baz"]}'

        ```

    iterencode(*o*)
    :   Encode the given object, *o*, and yield each string representation as
        available. For example:

        Copy

        ```
        for chunk in json.JSONEncoder().iterencode(bigobject):
            mysocket.write(chunk)

        ```