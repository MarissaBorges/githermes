`plistlib` — Generate and parse Apple `.plist` files
====================================================

**Source code:** [Lib/plistlib.py](https://github.com/python/cpython/tree/3.13/Lib/plistlib.py)

---

This module provides an interface for reading and writing the “property list”
files used by Apple, primarily on macOS and iOS. This module supports both binary
and XML plist files.

The property list (`.plist`) file format is a simple serialization supporting
basic object types, like dictionaries, lists, numbers and strings. Usually the
top level object is a dictionary.

To write out and to parse a plist file, use the [`dump()`](#plistlib.dump "plistlib.dump") and
[`load()`](#plistlib.load "plistlib.load") functions.

To work with plist data in bytes or string objects, use [`dumps()`](#plistlib.dumps "plistlib.dumps")
and [`loads()`](#plistlib.loads "plistlib.loads").

Values can be strings, integers, floats, booleans, tuples, lists, dictionaries
(but only with string keys), [`bytes`](stdtypes.html#bytes "bytes"), [`bytearray`](stdtypes.html#bytearray "bytearray")
or [`datetime.datetime`](datetime.html#datetime.datetime "datetime.datetime") objects.

Changed in version 3.4: New API, old API deprecated. Support for binary format plists added.

Changed in version 3.8: Support added for reading and writing [`UID`](#plistlib.UID "plistlib.UID") tokens in binary plists as used
by NSKeyedArchiver and NSKeyedUnarchiver.

Changed in version 3.9: Old API removed.

This module defines the following functions:

plistlib.load(*fp*, *\**, *fmt=None*, *dict\_type=dict*, *aware\_datetime=False*)
:   Read a plist file. *fp* should be a readable and binary file object.
    Return the unpacked root object (which usually is a
    dictionary).

    The *fmt* is the format of the file and the following values are valid:

    The *dict\_type* is the type used for dictionaries that are read from the
    plist file.

    When *aware\_datetime* is true, fields with type `datetime.datetime` will
    be created as [aware object](datetime.html#datetime-naive-aware), with
    `tzinfo` as [`datetime.UTC`](datetime.html#datetime.UTC "datetime.UTC").

    XML data for the [`FMT_XML`](#plistlib.FMT_XML "plistlib.FMT_XML") format is parsed using the Expat parser
    from [`xml.parsers.expat`](pyexpat.html#module-xml.parsers.expat "xml.parsers.expat: An interface to the Expat non-validating XML parser.") – see its documentation for possible
    exceptions on ill-formed XML. Unknown elements will simply be ignored
    by the plist parser.

    The parser raises [`InvalidFileException`](#plistlib.InvalidFileException "plistlib.InvalidFileException") when the file cannot be parsed.

    Changed in version 3.13: The keyword-only parameter *aware\_datetime* has been added.

plistlib.loads(*data*, *\**, *fmt=None*, *dict\_type=dict*, *aware\_datetime=False*)
:   Load a plist from a bytes or string object. See [`load()`](#plistlib.load "plistlib.load") for an
    explanation of the keyword arguments.

    Changed in version 3.13: *data* can be a string when *fmt* equals [`FMT_XML`](#plistlib.FMT_XML "plistlib.FMT_XML").

plistlib.dump(*value*, *fp*, *\**, *fmt=FMT\_XML*, *sort\_keys=True*, *skipkeys=False*, *aware\_datetime=False*)
:   Write *value* to a plist file. *fp* should be a writable, binary
    file object.

    The *fmt* argument specifies the format of the plist file and can be
    one of the following values:

    When *sort\_keys* is true (the default) the keys for dictionaries will be
    written to the plist in sorted order, otherwise they will be written in
    the iteration order of the dictionary.

    When *skipkeys* is false (the default) the function raises [`TypeError`](exceptions.html#TypeError "TypeError")
    when a key of a dictionary is not a string, otherwise such keys are skipped.

    When *aware\_datetime* is true and any field with type `datetime.datetime`
    is set as an [aware object](datetime.html#datetime-naive-aware), it will convert to
    UTC timezone before writing it.

    A [`TypeError`](exceptions.html#TypeError "TypeError") will be raised if the object is of an unsupported type or
    a container that contains objects of unsupported types.

    An [`OverflowError`](exceptions.html#OverflowError "OverflowError") will be raised for integer values that cannot
    be represented in (binary) plist files.

    Changed in version 3.13: The keyword-only parameter *aware\_datetime* has been added.

plistlib.dumps(*value*, *\**, *fmt=FMT\_XML*, *sort\_keys=True*, *skipkeys=False*, *aware\_datetime=False*)
:   Return *value* as a plist-formatted bytes object. See
    the documentation for [`dump()`](#plistlib.dump "plistlib.dump") for an explanation of the keyword
    arguments of this function.

The following classes are available:

*class* plistlib.UID(*data*)
:   Wraps an [`int`](functions.html#int "int"). This is used when reading or writing NSKeyedArchiver
    encoded data, which contains UID (see PList manual).

    data
    :   Int value of the UID. It must be in the range `0 <= data < 2**64`.

The following constants are available:

plistlib.FMT\_XML
:   The XML format for plist files.

plistlib.FMT\_BINARY
:   The binary format for plist files

The module defines the following exceptions:

*exception* plistlib.InvalidFileException
:   Raised when a file cannot be parsed.

Examples
--------

Generating a plist:

Copy

```
import datetime
import plistlib

pl = dict(
    aString = "Doodah",
    aList = ["A", "B", 12, 32.1, [1, 2, 3]],
    aFloat = 0.1,
    anInt = 728,
    aDict = dict(
        anotherString = "<hello & hi there!>",
        aThirdString = "M\xe4ssig, Ma\xdf",
        aTrueValue = True,
        aFalseValue = False,
    ),
    someData = b"<binary gunk>",
    someMoreData = b"<lots of binary gunk>" * 10,
    aDate = datetime.datetime.now()
)
print(plistlib.dumps(pl).decode())

```

Parsing a plist:

Copy

```
import plistlib

plist = b"""<plist version="1.0">
<dict>
    <key>foo</key>
    <string>bar</string>
</dict>
</plist>"""
pl = plistlib.loads(plist)
print(pl["foo"])

```