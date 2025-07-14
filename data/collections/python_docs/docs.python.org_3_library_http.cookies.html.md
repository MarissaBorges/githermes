`http.cookies` — HTTP state management
======================================

**Source code:** [Lib/http/cookies.py](https://github.com/python/cpython/tree/3.13/Lib/http/cookies.py)

---

The [`http.cookies`](#module-http.cookies "http.cookies: Support for HTTP state management (cookies).") module defines classes for abstracting the concept of
cookies, an HTTP state management mechanism. It supports both simple string-only
cookies, and provides an abstraction for having any serializable data-type as
cookie value.

The module formerly strictly applied the parsing rules described in the
[**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) and [**RFC 2068**](https://datatracker.ietf.org/doc/html/rfc2068.html) specifications. It has since been discovered that
MSIE 3.0x didn’t follow the character rules outlined in those specs; many
current-day browsers and servers have also relaxed parsing rules when it comes
to cookie handling. As a result, this module now uses parsing rules that are a
bit less strict than they once were.

The character set, [`string.ascii_letters`](string.html#string.ascii_letters "string.ascii_letters"), [`string.digits`](string.html#string.digits "string.digits") and
`!#$%&'*+-.^_`|~:` denote the set of valid characters allowed by this module
in a cookie name (as [`key`](#http.cookies.Morsel.key "http.cookies.Morsel.key")).

Changed in version 3.3: Allowed ‘:’ as a valid cookie name character.

Note

On encountering an invalid cookie, [`CookieError`](#http.cookies.CookieError "http.cookies.CookieError") is raised, so if your
cookie data comes from a browser you should always prepare for invalid data
and catch [`CookieError`](#http.cookies.CookieError "http.cookies.CookieError") on parsing.

*exception* http.cookies.CookieError
:   Exception failing because of [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) invalidity: incorrect attributes,
    incorrect header, etc.

*class* http.cookies.BaseCookie([*input*])
:   This class is a dictionary-like object whose keys are strings and whose values
    are [`Morsel`](#http.cookies.Morsel "http.cookies.Morsel") instances. Note that upon setting a key to a value, the
    value is first converted to a [`Morsel`](#http.cookies.Morsel "http.cookies.Morsel") containing the key and the value.

    If *input* is given, it is passed to the [`load()`](#http.cookies.BaseCookie.load "http.cookies.BaseCookie.load") method.

*class* http.cookies.SimpleCookie([*input*])
:   This class derives from [`BaseCookie`](#http.cookies.BaseCookie "http.cookies.BaseCookie") and overrides [`value_decode()`](#http.cookies.BaseCookie.value_decode "http.cookies.BaseCookie.value_decode")
    and [`value_encode()`](#http.cookies.BaseCookie.value_encode "http.cookies.BaseCookie.value_encode"). `SimpleCookie` supports
    strings as cookie values. When setting the value, `SimpleCookie`
    calls the builtin [`str()`](stdtypes.html#str "str") to convert
    the value to a string. Values received from HTTP are kept as strings.

See also

Module [`http.cookiejar`](http.cookiejar.html#module-http.cookiejar "http.cookiejar: Classes for automatic handling of HTTP cookies.")
:   HTTP cookie handling for web *clients*. The [`http.cookiejar`](http.cookiejar.html#module-http.cookiejar "http.cookiejar: Classes for automatic handling of HTTP cookies.") and
    [`http.cookies`](#module-http.cookies "http.cookies: Support for HTTP state management (cookies).") modules do not depend on each other.

[**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) - HTTP State Management Mechanism
:   This is the state management specification implemented by this module.

Cookie Objects
--------------

BaseCookie.value\_decode(*val*)
:   Return a tuple `(real_value, coded_value)` from a string representation.
    `real_value` can be any type. This method does no decoding in
    [`BaseCookie`](#http.cookies.BaseCookie "http.cookies.BaseCookie") — it exists so it can be overridden.

BaseCookie.value\_encode(*val*)
:   Return a tuple `(real_value, coded_value)`. *val* can be any type, but
    `coded_value` will always be converted to a string.
    This method does no encoding in [`BaseCookie`](#http.cookies.BaseCookie "http.cookies.BaseCookie") — it exists so it can
    be overridden.

    In general, it should be the case that [`value_encode()`](#http.cookies.BaseCookie.value_encode "http.cookies.BaseCookie.value_encode") and
    [`value_decode()`](#http.cookies.BaseCookie.value_decode "http.cookies.BaseCookie.value_decode") are inverses on the range of *value\_decode*.

BaseCookie.output(*attrs=None*, *header='Set-Cookie:'*, *sep='\r\n'*)
:   Return a string representation suitable to be sent as HTTP headers. *attrs* and
    *header* are sent to each [`Morsel`](#http.cookies.Morsel "http.cookies.Morsel")’s [`output()`](#http.cookies.Morsel.output "http.cookies.Morsel.output") method. *sep* is used
    to join the headers together, and is by default the combination `'\r\n'`
    (CRLF).

BaseCookie.js\_output(*attrs=None*)
:   Return an embeddable JavaScript snippet, which, if run on a browser which
    supports JavaScript, will act the same as if the HTTP headers was sent.

    The meaning for *attrs* is the same as in [`output()`](#http.cookies.BaseCookie.output "http.cookies.BaseCookie.output").

BaseCookie.load(*rawdata*)
:   If *rawdata* is a string, parse it as an `HTTP_COOKIE` and add the values
    found there as [`Morsel`](#http.cookies.Morsel "http.cookies.Morsel")s. If it is a dictionary, it is equivalent to:

    Copy

    ```
    for k, v in rawdata.items():
        cookie[k] = v

    ```

Morsel Objects
--------------

*class* http.cookies.Morsel
:   Abstract a key/value pair, which has some [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) attributes.

    Morsels are dictionary-like objects, whose set of keys is constant — the valid
    [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) attributes, which are:

    > expires
    >
    > path
    >
    > domain
    >
    > max-age
    >
    > secure
    >
    > version
    >
    > httponly
    >
    > samesite

    The attribute [`httponly`](#http.cookies.Morsel.httponly "http.cookies.Morsel.httponly") specifies that the cookie is only transferred
    in HTTP requests, and is not accessible through JavaScript. This is intended
    to mitigate some forms of cross-site scripting.

    The attribute [`samesite`](#http.cookies.Morsel.samesite "http.cookies.Morsel.samesite") specifies that the browser is not allowed to
    send the cookie along with cross-site requests. This helps to mitigate CSRF
    attacks. Valid values for this attribute are “Strict” and “Lax”.

    The keys are case-insensitive and their default value is `''`.

    Changed in version 3.5: `__eq__()` now takes [`key`](#http.cookies.Morsel.key "http.cookies.Morsel.key") and [`value`](#http.cookies.Morsel.value "http.cookies.Morsel.value")
    into account.

    Changed in version 3.8: Added support for the [`samesite`](#http.cookies.Morsel.samesite "http.cookies.Morsel.samesite") attribute.

Morsel.value
:   The value of the cookie.

Morsel.coded\_value
:   The encoded value of the cookie — this is what should be sent.

Morsel.key
:   The name of the cookie.

Morsel.set(*key*, *value*, *coded\_value*)
:   Set the *key*, *value* and *coded\_value* attributes.

Morsel.isReservedKey(*K*)
:   Whether *K* is a member of the set of keys of a [`Morsel`](#http.cookies.Morsel "http.cookies.Morsel").

Morsel.output(*attrs=None*, *header='Set-Cookie:'*)
:   Return a string representation of the Morsel, suitable to be sent as an HTTP
    header. By default, all the attributes are included, unless *attrs* is given, in
    which case it should be a list of attributes to use. *header* is by default
    `"Set-Cookie:"`.

Morsel.js\_output(*attrs=None*)
:   Return an embeddable JavaScript snippet, which, if run on a browser which
    supports JavaScript, will act the same as if the HTTP header was sent.

    The meaning for *attrs* is the same as in [`output()`](#http.cookies.Morsel.output "http.cookies.Morsel.output").

Morsel.OutputString(*attrs=None*)
:   Return a string representing the Morsel, without any surrounding HTTP or
    JavaScript.

    The meaning for *attrs* is the same as in [`output()`](#http.cookies.Morsel.output "http.cookies.Morsel.output").

Morsel.update(*values*)
:   Update the values in the Morsel dictionary with the values in the dictionary
    *values*. Raise an error if any of the keys in the *values* dict is not a
    valid [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) attribute.

    Changed in version 3.5: an error is raised for invalid keys.

Morsel.copy(*value*)
:   Return a shallow copy of the Morsel object.

    Changed in version 3.5: return a Morsel object instead of a dict.

Morsel.setdefault(*key*, *value=None*)
:   Raise an error if key is not a valid [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) attribute, otherwise
    behave the same as [`dict.setdefault()`](stdtypes.html#dict.setdefault "dict.setdefault").

Example
-------

The following example demonstrates how to use the [`http.cookies`](#module-http.cookies "http.cookies: Support for HTTP state management (cookies).") module.

Copy

```
>>> from http import cookies
>>> C = cookies.SimpleCookie()
>>> C["fig"] = "newton"
>>> C["sugar"] = "wafer"
>>> print(C) # generate HTTP headers
Set-Cookie: fig=newton
Set-Cookie: sugar=wafer
>>> print(C.output()) # same thing
Set-Cookie: fig=newton
Set-Cookie: sugar=wafer
>>> C = cookies.SimpleCookie()
>>> C["rocky"] = "road"
>>> C["rocky"]["path"] = "/cookie"
>>> print(C.output(header="Cookie:"))
Cookie: rocky=road; Path=/cookie
>>> print(C.output(attrs=[], header="Cookie:"))
Cookie: rocky=road
>>> C = cookies.SimpleCookie()
>>> C.load("chips=ahoy; vienna=finger") # load from a string (HTTP header)
>>> print(C)
Set-Cookie: chips=ahoy
Set-Cookie: vienna=finger
>>> C = cookies.SimpleCookie()
>>> C.load('keebler="E=everybody; L=\\"Loves\\"; fudge=\\012;";')
>>> print(C)
Set-Cookie: keebler="E=everybody; L=\"Loves\"; fudge=\012;"
>>> C = cookies.SimpleCookie()
>>> C["oreo"] = "doublestuff"
>>> C["oreo"]["path"] = "/"
>>> print(C)
Set-Cookie: oreo=doublestuff; Path=/
>>> C = cookies.SimpleCookie()
>>> C["twix"] = "none for you"
>>> C["twix"].value
'none for you'
>>> C = cookies.SimpleCookie()
>>> C["number"] = 7 # equivalent to C["number"] = str(7)
>>> C["string"] = "seven"
>>> C["number"].value
'7'
>>> C["string"].value
'seven'
>>> print(C)
Set-Cookie: number=7
Set-Cookie: string=seven

```