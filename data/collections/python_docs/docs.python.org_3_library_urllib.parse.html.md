`urllib.parse` — Parse URLs into components
===========================================

**Source code:** [Lib/urllib/parse.py](https://github.com/python/cpython/tree/3.13/Lib/urllib/parse.py)

---

This module defines a standard interface to break Uniform Resource Locator (URL)
strings up in components (addressing scheme, network location, path etc.), to
combine the components back into a URL string, and to convert a “relative URL”
to an absolute URL given a “base URL.”

The module has been designed to match the internet RFC on Relative Uniform
Resource Locators. It supports the following URL schemes: `file`, `ftp`,
`gopher`, `hdl`, `http`, `https`, `imap`, `itms-services`, `mailto`, `mms`,
`news`, `nntp`, `prospero`, `rsync`, `rtsp`, `rtsps`, `rtspu`,
`sftp`, `shttp`, `sip`, `sips`, `snews`, `svn`, `svn+ssh`,
`telnet`, `wais`, `ws`, `wss`.

**CPython implementation detail:** The inclusion of the `itms-services` URL scheme can prevent an app from
passing Apple’s App Store review process for the macOS and iOS App Stores.
Handling for the `itms-services` scheme is always removed on iOS; on
macOS, it *may* be removed if CPython has been built with the
[`--with-app-store-compliance`](../using/configure.html#cmdoption-with-app-store-compliance) option.

The [`urllib.parse`](#module-urllib.parse "urllib.parse: Parse URLs into or assemble them from components.") module defines functions that fall into two broad
categories: URL parsing and URL quoting. These are covered in detail in
the following sections.

This module’s functions use the deprecated term `netloc` (or `net_loc`),
which was introduced in [**RFC 1808**](https://datatracker.ietf.org/doc/html/rfc1808.html). However, this term has been obsoleted by
[**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html), which introduced the term `authority` as its replacement.
The use of `netloc` is continued for backward compatibility.

URL Parsing
-----------

The URL parsing functions focus on splitting a URL string into its components,
or on combining URL components into a URL string.

urllib.parse.urlparse(*urlstring*, *scheme=''*, *allow\_fragments=True*)
:   Parse a URL into six components, returning a 6-item [named tuple](../glossary.html#term-named-tuple). This
    corresponds to the general structure of a URL:
    `scheme://netloc/path;parameters?query#fragment`.
    Each tuple item is a string, possibly empty. The components are not broken up
    into smaller parts (for example, the network location is a single string), and %
    escapes are not expanded. The delimiters as shown above are not part of the
    result, except for a leading slash in the *path* component, which is retained if
    present. For example:

    Copy

    ```
    >>> from urllib.parse import urlparse
    >>> urlparse("scheme://netloc/path;parameters?query#fragment")
    ParseResult(scheme='scheme', netloc='netloc', path='/path;parameters', params='',
                query='query', fragment='fragment')
    >>> o = urlparse("http://docs.python.org:80/3/library/urllib.parse.html?"
    ...              "highlight=params#url-parsing")
    >>> o
    ParseResult(scheme='http', netloc='docs.python.org:80',
                path='/3/library/urllib.parse.html', params='',
                query='highlight=params', fragment='url-parsing')
    >>> o.scheme
    'http'
    >>> o.netloc
    'docs.python.org:80'
    >>> o.hostname
    'docs.python.org'
    >>> o.port
    80
    >>> o._replace(fragment="").geturl()
    'http://docs.python.org:80/3/library/urllib.parse.html?highlight=params'

    ```

    Following the syntax specifications in [**RFC 1808**](https://datatracker.ietf.org/doc/html/rfc1808.html), urlparse recognizes
    a netloc only if it is properly introduced by ‘//’. Otherwise the
    input is presumed to be a relative URL and thus to start with
    a path component.

    Copy

    ```
    >>> from urllib.parse import urlparse
    >>> urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
    ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                params='', query='', fragment='')
    >>> urlparse('www.cwi.nl/%7Eguido/Python.html')
    ParseResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html',
                params='', query='', fragment='')
    >>> urlparse('help/Python.html')
    ParseResult(scheme='', netloc='', path='help/Python.html', params='',
                query='', fragment='')

    ```

    The *scheme* argument gives the default addressing scheme, to be
    used only if the URL does not specify one. It should be the same type
    (text or bytes) as *urlstring*, except that the default value `''` is
    always allowed, and is automatically converted to `b''` if appropriate.

    If the *allow\_fragments* argument is false, fragment identifiers are not
    recognized. Instead, they are parsed as part of the path, parameters
    or query component, and `fragment` is set to the empty string in
    the return value.

    The return value is a [named tuple](../glossary.html#term-named-tuple), which means that its items can
    be accessed by index or as named attributes, which are:

    | Attribute | Index | Value | Value if not present |
    | --- | --- | --- | --- |
    | `scheme` | 0 | URL scheme specifier | *scheme* parameter |
    | `netloc` | 1 | Network location part | empty string |
    | `path` | 2 | Hierarchical path | empty string |
    | `params` | 3 | Parameters for last path element | empty string |
    | `query` | 4 | Query component | empty string |
    | `fragment` | 5 | Fragment identifier | empty string |
    | `username` |  | User name | [`None`](constants.html#None "None") |
    | `password` |  | Password | [`None`](constants.html#None "None") |
    | `hostname` |  | Host name (lower case) | [`None`](constants.html#None "None") |
    | `port` |  | Port number as integer, if present | [`None`](constants.html#None "None") |

    Reading the `port` attribute will raise a [`ValueError`](exceptions.html#ValueError "ValueError") if
    an invalid port is specified in the URL. See section
    [Structured Parse Results](#urlparse-result-object) for more information on the result object.

    Unmatched square brackets in the `netloc` attribute will raise a
    [`ValueError`](exceptions.html#ValueError "ValueError").

    Characters in the `netloc` attribute that decompose under NFKC
    normalization (as used by the IDNA encoding) into any of `/`, `?`,
    `#`, `@`, or `:` will raise a [`ValueError`](exceptions.html#ValueError "ValueError"). If the URL is
    decomposed before parsing, no error will be raised.

    As is the case with all named tuples, the subclass has a few additional methods
    and attributes that are particularly useful. One such method is `_replace()`.
    The `_replace()` method will return a new ParseResult object replacing specified
    fields with new values.

    Copy

    ```
    >>> from urllib.parse import urlparse
    >>> u = urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
    >>> u
    ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                params='', query='', fragment='')
    >>> u._replace(scheme='http')
    ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                params='', query='', fragment='')

    ```

    Changed in version 3.2: Added IPv6 URL parsing capabilities.

    Changed in version 3.3: The fragment is now parsed for all URL schemes (unless *allow\_fragments* is
    false), in accordance with [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html). Previously, an allowlist of
    schemes that support fragments existed.

    Changed in version 3.6: Out-of-range port numbers now raise [`ValueError`](exceptions.html#ValueError "ValueError"), instead of
    returning [`None`](constants.html#None "None").

    Changed in version 3.8: Characters that affect netloc parsing under NFKC normalization will
    now raise [`ValueError`](exceptions.html#ValueError "ValueError").

urllib.parse.parse\_qs(*qs*, *keep\_blank\_values=False*, *strict\_parsing=False*, *encoding='utf-8'*, *errors='replace'*, *max\_num\_fields=None*, *separator='&'*)
:   Parse a query string given as a string argument (data of type
    *application/x-www-form-urlencoded*). Data are returned as a
    dictionary. The dictionary keys are the unique query variable names and the
    values are lists of values for each name.

    The optional argument *keep\_blank\_values* is a flag indicating whether blank
    values in percent-encoded queries should be treated as blank strings. A true value
    indicates that blanks should be retained as blank strings. The default false
    value indicates that blank values are to be ignored and treated as if they were
    not included.

    The optional argument *strict\_parsing* is a flag indicating what to do with
    parsing errors. If false (the default), errors are silently ignored. If true,
    errors raise a [`ValueError`](exceptions.html#ValueError "ValueError") exception.

    The optional *encoding* and *errors* parameters specify how to decode
    percent-encoded sequences into Unicode characters, as accepted by the
    [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode") method.

    The optional argument *max\_num\_fields* is the maximum number of fields to
    read. If set, then throws a [`ValueError`](exceptions.html#ValueError "ValueError") if there are more than
    *max\_num\_fields* fields read.

    The optional argument *separator* is the symbol to use for separating the
    query arguments. It defaults to `&`.

    Use the [`urllib.parse.urlencode()`](#urllib.parse.urlencode "urllib.parse.urlencode") function (with the `doseq`
    parameter set to `True`) to convert such dictionaries into query
    strings.

    Changed in version 3.2: Add *encoding* and *errors* parameters.

    Changed in version 3.8: Added *max\_num\_fields* parameter.

    Changed in version 3.10: Added *separator* parameter with the default value of `&`. Python
    versions earlier than Python 3.10 allowed using both `;` and `&` as
    query parameter separator. This has been changed to allow only a single
    separator key, with `&` as the default separator.

urllib.parse.parse\_qsl(*qs*, *keep\_blank\_values=False*, *strict\_parsing=False*, *encoding='utf-8'*, *errors='replace'*, *max\_num\_fields=None*, *separator='&'*)
:   Parse a query string given as a string argument (data of type
    *application/x-www-form-urlencoded*). Data are returned as a list of
    name, value pairs.

    The optional argument *keep\_blank\_values* is a flag indicating whether blank
    values in percent-encoded queries should be treated as blank strings. A true value
    indicates that blanks should be retained as blank strings. The default false
    value indicates that blank values are to be ignored and treated as if they were
    not included.

    The optional argument *strict\_parsing* is a flag indicating what to do with
    parsing errors. If false (the default), errors are silently ignored. If true,
    errors raise a [`ValueError`](exceptions.html#ValueError "ValueError") exception.

    The optional *encoding* and *errors* parameters specify how to decode
    percent-encoded sequences into Unicode characters, as accepted by the
    [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode") method.

    The optional argument *max\_num\_fields* is the maximum number of fields to
    read. If set, then throws a [`ValueError`](exceptions.html#ValueError "ValueError") if there are more than
    *max\_num\_fields* fields read.

    The optional argument *separator* is the symbol to use for separating the
    query arguments. It defaults to `&`.

    Use the [`urllib.parse.urlencode()`](#urllib.parse.urlencode "urllib.parse.urlencode") function to convert such lists of pairs into
    query strings.

    Changed in version 3.2: Add *encoding* and *errors* parameters.

    Changed in version 3.8: Added *max\_num\_fields* parameter.

    Changed in version 3.10: Added *separator* parameter with the default value of `&`. Python
    versions earlier than Python 3.10 allowed using both `;` and `&` as
    query parameter separator. This has been changed to allow only a single
    separator key, with `&` as the default separator.

urllib.parse.urlunparse(*parts*)
:   Construct a URL from a tuple as returned by `urlparse()`. The *parts*
    argument can be any six-item iterable. This may result in a slightly
    different, but equivalent URL, if the URL that was parsed originally had
    unnecessary delimiters (for example, a `?` with an empty query; the RFC
    states that these are equivalent).

urllib.parse.urlsplit(*urlstring*, *scheme=''*, *allow\_fragments=True*)
:   This is similar to [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse"), but does not split the params from the URL.
    This should generally be used instead of [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse") if the more recent URL
    syntax allowing parameters to be applied to each segment of the *path* portion
    of the URL (see [**RFC 2396**](https://datatracker.ietf.org/doc/html/rfc2396.html)) is wanted. A separate function is needed to
    separate the path segments and parameters. This function returns a 5-item
    [named tuple](../glossary.html#term-named-tuple):

    Copy

    ```
    (addressing scheme, network location, path, query, fragment identifier).

    ```

    The return value is a [named tuple](../glossary.html#term-named-tuple), its items can be accessed by index
    or as named attributes:

    | Attribute | Index | Value | Value if not present |
    | --- | --- | --- | --- |
    | `scheme` | 0 | URL scheme specifier | *scheme* parameter |
    | `netloc` | 1 | Network location part | empty string |
    | `path` | 2 | Hierarchical path | empty string |
    | `query` | 3 | Query component | empty string |
    | `fragment` | 4 | Fragment identifier | empty string |
    | `username` |  | User name | [`None`](constants.html#None "None") |
    | `password` |  | Password | [`None`](constants.html#None "None") |
    | `hostname` |  | Host name (lower case) | [`None`](constants.html#None "None") |
    | `port` |  | Port number as integer, if present | [`None`](constants.html#None "None") |

    Reading the `port` attribute will raise a [`ValueError`](exceptions.html#ValueError "ValueError") if
    an invalid port is specified in the URL. See section
    [Structured Parse Results](#urlparse-result-object) for more information on the result object.

    Unmatched square brackets in the `netloc` attribute will raise a
    [`ValueError`](exceptions.html#ValueError "ValueError").

    Characters in the `netloc` attribute that decompose under NFKC
    normalization (as used by the IDNA encoding) into any of `/`, `?`,
    `#`, `@`, or `:` will raise a [`ValueError`](exceptions.html#ValueError "ValueError"). If the URL is
    decomposed before parsing, no error will be raised.

    Following some of the [WHATWG spec](https://url.spec.whatwg.org/#concept-basic-url-parser) that updates RFC 3986, leading C0
    control and space characters are stripped from the URL. `\n`,
    `\r` and tab `\t` characters are removed from the URL at any position.

    Changed in version 3.6: Out-of-range port numbers now raise [`ValueError`](exceptions.html#ValueError "ValueError"), instead of
    returning [`None`](constants.html#None "None").

    Changed in version 3.8: Characters that affect netloc parsing under NFKC normalization will
    now raise [`ValueError`](exceptions.html#ValueError "ValueError").

    Changed in version 3.10: ASCII newline and tab characters are stripped from the URL.

    Changed in version 3.12: Leading WHATWG C0 control and space characters are stripped from the URL.

urllib.parse.urlunsplit(*parts*)
:   Combine the elements of a tuple as returned by [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") into a
    complete URL as a string. The *parts* argument can be any five-item
    iterable. This may result in a slightly different, but equivalent URL, if the
    URL that was parsed originally had unnecessary delimiters (for example, a ?
    with an empty query; the RFC states that these are equivalent).

urllib.parse.urljoin(*base*, *url*, *allow\_fragments=True*)
:   Construct a full (“absolute”) URL by combining a “base URL” (*base*) with
    another URL (*url*). Informally, this uses components of the base URL, in
    particular the addressing scheme, the network location and (part of) the
    path, to provide missing components in the relative URL. For example:

    Copy

    ```
    >>> from urllib.parse import urljoin
    >>> urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
    'http://www.cwi.nl/%7Eguido/FAQ.html'

    ```

    The *allow\_fragments* argument has the same meaning and default as for
    [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse").

    Note

    If *url* is an absolute URL (that is, it starts with `//` or `scheme://`),
    the *url*’s hostname and/or scheme will be present in the result. For example:

    Copy

    ```
    >>> urljoin('http://www.cwi.nl/%7Eguido/Python.html',
    ...         '//www.python.org/%7Eguido')
    'http://www.python.org/%7Eguido'

    ```

    If you do not want that behavior, preprocess the *url* with [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") and
    [`urlunsplit()`](#urllib.parse.urlunsplit "urllib.parse.urlunsplit"), removing possible *scheme* and *netloc* parts.

    Warning

    Because an absolute URL may be passed as the `url` parameter, it is
    generally **not secure** to use `urljoin` with an attacker-controlled
    `url`. For example in,
    `urljoin("https://website.com/users/", username)`, if `username` can
    contain an absolute URL, the result of `urljoin` will be the absolute
    URL.

    Changed in version 3.5: Behavior updated to match the semantics defined in [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html).

urllib.parse.urldefrag(*url*)
:   If *url* contains a fragment identifier, return a modified version of *url*
    with no fragment identifier, and the fragment identifier as a separate
    string. If there is no fragment identifier in *url*, return *url* unmodified
    and an empty string.

    The return value is a [named tuple](../glossary.html#term-named-tuple), its items can be accessed by index
    or as named attributes:

    | Attribute | Index | Value | Value if not present |
    | --- | --- | --- | --- |
    | `url` | 0 | URL with no fragment | empty string |
    | `fragment` | 1 | Fragment identifier | empty string |

    See section [Structured Parse Results](#urlparse-result-object) for more information on the result
    object.

    Changed in version 3.2: Result is a structured object rather than a simple 2-tuple.

urllib.parse.unwrap(*url*)
:   Extract the url from a wrapped URL (that is, a string formatted as
    `<URL:scheme://host/path>`, `<scheme://host/path>`, `URL:scheme://host/path`
    or `scheme://host/path`). If *url* is not a wrapped URL, it is returned
    without changes.

URL parsing security
--------------------

The [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") and [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse") APIs do not perform **validation** of
inputs. They may not raise errors on inputs that other applications consider
invalid. They may also succeed on some inputs that might not be considered
URLs elsewhere. Their purpose is for practical functionality rather than
purity.

Instead of raising an exception on unusual input, they may instead return some
component parts as empty strings. Or components may contain more than perhaps
they should.

We recommend that users of these APIs where the values may be used anywhere
with security implications code defensively. Do some verification within your
code before trusting a returned component part. Does that `scheme` make
sense? Is that a sensible `path`? Is there anything strange about that
`hostname`? etc.

What constitutes a URL is not universally well defined. Different applications
have different needs and desired constraints. For instance the living [WHATWG
spec](https://url.spec.whatwg.org/#concept-basic-url-parser) describes what user facing web clients such as a web browser require.
While [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html) is more general. These functions incorporate some aspects of
both, but cannot be claimed compliant with either. The APIs and existing user
code with expectations on specific behaviors predate both standards leading us
to be very cautious about making API behavior changes.

Parsing ASCII Encoded Bytes
---------------------------

The URL parsing functions were originally designed to operate on character
strings only. In practice, it is useful to be able to manipulate properly
quoted and encoded URLs as sequences of ASCII bytes. Accordingly, the
URL parsing functions in this module all operate on [`bytes`](stdtypes.html#bytes "bytes") and
[`bytearray`](stdtypes.html#bytearray "bytearray") objects in addition to [`str`](stdtypes.html#str "str") objects.

If [`str`](stdtypes.html#str "str") data is passed in, the result will also contain only
[`str`](stdtypes.html#str "str") data. If [`bytes`](stdtypes.html#bytes "bytes") or [`bytearray`](stdtypes.html#bytearray "bytearray") data is
passed in, the result will contain only [`bytes`](stdtypes.html#bytes "bytes") data.

Attempting to mix [`str`](stdtypes.html#str "str") data with [`bytes`](stdtypes.html#bytes "bytes") or
[`bytearray`](stdtypes.html#bytearray "bytearray") in a single function call will result in a
[`TypeError`](exceptions.html#TypeError "TypeError") being raised, while attempting to pass in non-ASCII
byte values will trigger [`UnicodeDecodeError`](exceptions.html#UnicodeDecodeError "UnicodeDecodeError").

To support easier conversion of result objects between [`str`](stdtypes.html#str "str") and
[`bytes`](stdtypes.html#bytes "bytes"), all return values from URL parsing functions provide
either an `encode()` method (when the result contains [`str`](stdtypes.html#str "str")
data) or a `decode()` method (when the result contains [`bytes`](stdtypes.html#bytes "bytes")
data). The signatures of these methods match those of the corresponding
[`str`](stdtypes.html#str "str") and [`bytes`](stdtypes.html#bytes "bytes") methods (except that the default encoding
is `'ascii'` rather than `'utf-8'`). Each produces a value of a
corresponding type that contains either [`bytes`](stdtypes.html#bytes "bytes") data (for
`encode()` methods) or [`str`](stdtypes.html#str "str") data (for
`decode()` methods).

Applications that need to operate on potentially improperly quoted URLs
that may contain non-ASCII data will need to do their own decoding from
bytes to characters before invoking the URL parsing methods.

The behaviour described in this section applies only to the URL parsing
functions. The URL quoting functions use their own rules when producing
or consuming byte sequences as detailed in the documentation of the
individual URL quoting functions.

Changed in version 3.2: URL parsing functions now accept ASCII encoded byte sequences

Structured Parse Results
------------------------

The result objects from the [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse"), [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") and
[`urldefrag()`](#urllib.parse.urldefrag "urllib.parse.urldefrag") functions are subclasses of the [`tuple`](stdtypes.html#tuple "tuple") type.
These subclasses add the attributes listed in the documentation for
those functions, the encoding and decoding support described in the
previous section, as well as an additional method:

urllib.parse.SplitResult.geturl()
:   Return the re-combined version of the original URL as a string. This may
    differ from the original URL in that the scheme may be normalized to lower
    case and empty components may be dropped. Specifically, empty parameters,
    queries, and fragment identifiers will be removed.

    For [`urldefrag()`](#urllib.parse.urldefrag "urllib.parse.urldefrag") results, only empty fragment identifiers will be removed.
    For [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") and [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse") results, all noted changes will be
    made to the URL returned by this method.

    The result of this method remains unchanged if passed back through the original
    parsing function:

    Copy

    ```
    >>> from urllib.parse import urlsplit
    >>> url = 'HTTP://www.Python.org/doc/#'
    >>> r1 = urlsplit(url)
    >>> r1.geturl()
    'http://www.Python.org/doc/'
    >>> r2 = urlsplit(r1.geturl())
    >>> r2.geturl()
    'http://www.Python.org/doc/'

    ```

The following classes provide the implementations of the structured parse
results when operating on [`str`](stdtypes.html#str "str") objects:

*class* urllib.parse.DefragResult(*url*, *fragment*)
:   Concrete class for [`urldefrag()`](#urllib.parse.urldefrag "urllib.parse.urldefrag") results containing [`str`](stdtypes.html#str "str")
    data. The `encode()` method returns a [`DefragResultBytes`](#urllib.parse.DefragResultBytes "urllib.parse.DefragResultBytes")
    instance.

*class* urllib.parse.ParseResult(*scheme*, *netloc*, *path*, *params*, *query*, *fragment*)
:   Concrete class for [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse") results containing [`str`](stdtypes.html#str "str")
    data. The `encode()` method returns a [`ParseResultBytes`](#urllib.parse.ParseResultBytes "urllib.parse.ParseResultBytes")
    instance.

*class* urllib.parse.SplitResult(*scheme*, *netloc*, *path*, *query*, *fragment*)
:   Concrete class for [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") results containing [`str`](stdtypes.html#str "str")
    data. The `encode()` method returns a [`SplitResultBytes`](#urllib.parse.SplitResultBytes "urllib.parse.SplitResultBytes")
    instance.

The following classes provide the implementations of the parse results when
operating on [`bytes`](stdtypes.html#bytes "bytes") or [`bytearray`](stdtypes.html#bytearray "bytearray") objects:

*class* urllib.parse.DefragResultBytes(*url*, *fragment*)
:   Concrete class for [`urldefrag()`](#urllib.parse.urldefrag "urllib.parse.urldefrag") results containing [`bytes`](stdtypes.html#bytes "bytes")
    data. The `decode()` method returns a [`DefragResult`](#urllib.parse.DefragResult "urllib.parse.DefragResult")
    instance.

*class* urllib.parse.ParseResultBytes(*scheme*, *netloc*, *path*, *params*, *query*, *fragment*)
:   Concrete class for [`urlparse()`](#urllib.parse.urlparse "urllib.parse.urlparse") results containing [`bytes`](stdtypes.html#bytes "bytes")
    data. The `decode()` method returns a [`ParseResult`](#urllib.parse.ParseResult "urllib.parse.ParseResult")
    instance.

*class* urllib.parse.SplitResultBytes(*scheme*, *netloc*, *path*, *query*, *fragment*)
:   Concrete class for [`urlsplit()`](#urllib.parse.urlsplit "urllib.parse.urlsplit") results containing [`bytes`](stdtypes.html#bytes "bytes")
    data. The `decode()` method returns a [`SplitResult`](#urllib.parse.SplitResult "urllib.parse.SplitResult")
    instance.

URL Quoting
-----------

The URL quoting functions focus on taking program data and making it safe
for use as URL components by quoting special characters and appropriately
encoding non-ASCII text. They also support reversing these operations to
recreate the original data from the contents of a URL component if that
task isn’t already covered by the URL parsing functions above.

urllib.parse.quote(*string*, *safe='/'*, *encoding=None*, *errors=None*)
:   Replace special characters in *string* using the `%xx` escape. Letters,
    digits, and the characters `'_.-~'` are never quoted. By default, this
    function is intended for quoting the path section of a URL. The optional
    *safe* parameter specifies additional ASCII characters that should not be
    quoted — its default value is `'/'`.

    *string* may be either a [`str`](stdtypes.html#str "str") or a [`bytes`](stdtypes.html#bytes "bytes") object.

    Changed in version 3.7: Moved from [**RFC 2396**](https://datatracker.ietf.org/doc/html/rfc2396.html) to [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html) for quoting URL strings. “~” is now
    included in the set of unreserved characters.

    The optional *encoding* and *errors* parameters specify how to deal with
    non-ASCII characters, as accepted by the [`str.encode()`](stdtypes.html#str.encode "str.encode") method.
    *encoding* defaults to `'utf-8'`.
    *errors* defaults to `'strict'`, meaning unsupported characters raise a
    [`UnicodeEncodeError`](exceptions.html#UnicodeEncodeError "UnicodeEncodeError").
    *encoding* and *errors* must not be supplied if *string* is a
    [`bytes`](stdtypes.html#bytes "bytes"), or a [`TypeError`](exceptions.html#TypeError "TypeError") is raised.

    Note that `quote(string, safe, encoding, errors)` is equivalent to
    `quote_from_bytes(string.encode(encoding, errors), safe)`.

    Example: `quote('/El Niño/')` yields `'/El%20Ni%C3%B1o/'`.

urllib.parse.quote\_plus(*string*, *safe=''*, *encoding=None*, *errors=None*)
:   Like [`quote()`](#urllib.parse.quote "urllib.parse.quote"), but also replace spaces with plus signs, as required for
    quoting HTML form values when building up a query string to go into a URL.
    Plus signs in the original string are escaped unless they are included in
    *safe*. It also does not have *safe* default to `'/'`.

    Example: `quote_plus('/El Niño/')` yields `'%2FEl+Ni%C3%B1o%2F'`.

urllib.parse.quote\_from\_bytes(*bytes*, *safe='/'*)
:   Like [`quote()`](#urllib.parse.quote "urllib.parse.quote"), but accepts a [`bytes`](stdtypes.html#bytes "bytes") object rather than a
    [`str`](stdtypes.html#str "str"), and does not perform string-to-bytes encoding.

    Example: `quote_from_bytes(b'a&\xef')` yields
    `'a%26%EF'`.

urllib.parse.unquote(*string*, *encoding='utf-8'*, *errors='replace'*)
:   Replace `%xx` escapes with their single-character equivalent.
    The optional *encoding* and *errors* parameters specify how to decode
    percent-encoded sequences into Unicode characters, as accepted by the
    [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode") method.

    *string* may be either a [`str`](stdtypes.html#str "str") or a [`bytes`](stdtypes.html#bytes "bytes") object.

    *encoding* defaults to `'utf-8'`.
    *errors* defaults to `'replace'`, meaning invalid sequences are replaced
    by a placeholder character.

    Example: `unquote('/El%20Ni%C3%B1o/')` yields `'/El Niño/'`.

    Changed in version 3.9: *string* parameter supports bytes and str objects (previously only str).

urllib.parse.unquote\_plus(*string*, *encoding='utf-8'*, *errors='replace'*)
:   Like [`unquote()`](#urllib.parse.unquote "urllib.parse.unquote"), but also replace plus signs with spaces, as required
    for unquoting HTML form values.

    *string* must be a [`str`](stdtypes.html#str "str").

    Example: `unquote_plus('/El+Ni%C3%B1o/')` yields `'/El Niño/'`.

urllib.parse.unquote\_to\_bytes(*string*)
:   Replace `%xx` escapes with their single-octet equivalent, and return a
    [`bytes`](stdtypes.html#bytes "bytes") object.

    *string* may be either a [`str`](stdtypes.html#str "str") or a [`bytes`](stdtypes.html#bytes "bytes") object.

    If it is a [`str`](stdtypes.html#str "str"), unescaped non-ASCII characters in *string*
    are encoded into UTF-8 bytes.

    Example: `unquote_to_bytes('a%26%EF')` yields `b'a&\xef'`.

urllib.parse.urlencode(*query*, *doseq=False*, *safe=''*, *encoding=None*, *errors=None*, *quote\_via=quote\_plus*)
:   Convert a mapping object or a sequence of two-element tuples, which may
    contain [`str`](stdtypes.html#str "str") or [`bytes`](stdtypes.html#bytes "bytes") objects, to a percent-encoded ASCII
    text string. If the resultant string is to be used as a *data* for POST
    operation with the [`urlopen()`](urllib.request.html#urllib.request.urlopen "urllib.request.urlopen") function, then
    it should be encoded to bytes, otherwise it would result in a
    [`TypeError`](exceptions.html#TypeError "TypeError").

    The resulting string is a series of `key=value` pairs separated by `'&'`
    characters, where both *key* and *value* are quoted using the *quote\_via*
    function. By default, [`quote_plus()`](#urllib.parse.quote_plus "urllib.parse.quote_plus") is used to quote the values, which
    means spaces are quoted as a `'+'` character and ‘/’ characters are
    encoded as `%2F`, which follows the standard for GET requests
    (`application/x-www-form-urlencoded`). An alternate function that can be
    passed as *quote\_via* is [`quote()`](#urllib.parse.quote "urllib.parse.quote"), which will encode spaces as `%20`
    and not encode ‘/’ characters. For maximum control of what is quoted, use
    `quote` and specify a value for *safe*.

    When a sequence of two-element tuples is used as the *query*
    argument, the first element of each tuple is a key and the second is a
    value. The value element in itself can be a sequence and in that case, if
    the optional parameter *doseq* evaluates to `True`, individual
    `key=value` pairs separated by `'&'` are generated for each element of
    the value sequence for the key. The order of parameters in the encoded
    string will match the order of parameter tuples in the sequence.

    The *safe*, *encoding*, and *errors* parameters are passed down to
    *quote\_via* (the *encoding* and *errors* parameters are only passed
    when a query element is a [`str`](stdtypes.html#str "str")).

    To reverse this encoding process, [`parse_qs()`](#urllib.parse.parse_qs "urllib.parse.parse_qs") and [`parse_qsl()`](#urllib.parse.parse_qsl "urllib.parse.parse_qsl") are
    provided in this module to parse query strings into Python data structures.

    Refer to [urllib examples](urllib.request.html#urllib-examples) to find out how the
    [`urllib.parse.urlencode()`](#urllib.parse.urlencode "urllib.parse.urlencode") method can be used for generating the query
    string of a URL or data for a POST request.

    Changed in version 3.2: *query* supports bytes and string objects.

    Changed in version 3.5: Added the *quote\_via* parameter.

See also

[WHATWG](https://url.spec.whatwg.org/) - URL Living standard
:   Working Group for the URL Standard that defines URLs, domains, IP addresses, the
    application/x-www-form-urlencoded format, and their API.

[**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html) - Uniform Resource Identifiers
:   This is the current standard (STD66). Any changes to urllib.parse module
    should conform to this. Certain deviations could be observed, which are
    mostly for backward compatibility purposes and for certain de-facto
    parsing requirements as commonly observed in major browsers.

[**RFC 2732**](https://datatracker.ietf.org/doc/html/rfc2732.html) - Format for Literal IPv6 Addresses in URL’s.
:   This specifies the parsing requirements of IPv6 URLs.

[**RFC 2396**](https://datatracker.ietf.org/doc/html/rfc2396.html) - Uniform Resource Identifiers (URI): Generic Syntax
:   Document describing the generic syntactic requirements for both Uniform Resource
    Names (URNs) and Uniform Resource Locators (URLs).

[**RFC 2368**](https://datatracker.ietf.org/doc/html/rfc2368.html) - The mailto URL scheme.
:   Parsing requirements for mailto URL schemes.

[**RFC 1808**](https://datatracker.ietf.org/doc/html/rfc1808.html) - Relative Uniform Resource Locators
:   This Request For Comments includes the rules for joining an absolute and a
    relative URL, including a fair number of “Abnormal Examples” which govern the
    treatment of border cases.

[**RFC 1738**](https://datatracker.ietf.org/doc/html/rfc1738.html) - Uniform Resource Locators (URL)
:   This specifies the formal syntax and semantics of absolute URLs.