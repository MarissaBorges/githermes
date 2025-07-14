:   A [`ServerProxy`](#xmlrpc.client.ServerProxy "xmlrpc.client.ServerProxy") instance is an object that manages communication with a
    remote XML-RPC server. The required first argument is a URI (Uniform Resource
    Indicator), and will normally be the URL of the server. The optional second
    argument is a transport factory instance; by default it is an internal
    `SafeTransport` instance for https: URLs and an internal HTTP
    `Transport` instance otherwise. The optional third argument is an
    encoding, by default UTF-8. The optional fourth argument is a debugging flag.

    The following parameters govern the use of the returned proxy instance.
    If *allow\_none* is true, the Python constant `None` will be translated into
    XML; the default behaviour is for `None` to raise a [`TypeError`](exceptions.html#TypeError "TypeError"). This is
    a commonly used extension to the XML-RPC specification, but isn’t supported by
    all clients and servers; see [http://ontosys.com/xml-rpc/extensions.php](https://web.archive.org/web/20130120074804/http://ontosys.com/xml-rpc/extensions.php)
    for a description.
    The *use\_builtin\_types* flag can be used to cause date/time values
    to be presented as [`datetime.datetime`](datetime.html#datetime.datetime "datetime.datetime") objects and binary data to be
    presented as [`bytes`](stdtypes.html#bytes "bytes") objects; this flag is false by default.
    [`datetime.datetime`](datetime.html#datetime.datetime "datetime.datetime"), [`bytes`](stdtypes.html#bytes "bytes") and [`bytearray`](stdtypes.html#bytearray "bytearray") objects
    may be passed to calls.
    The *headers* parameter is an optional sequence of HTTP headers to send with
    each request, expressed as a sequence of 2-tuples representing the header
    name and value. (e.g. `[('Header-Name', 'value')]`).
    If an HTTPS URL is provided, *context* may be [`ssl.SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext")
    and configures the SSL settings of the underlying HTTPS connection.
    The obsolete *use\_datetime* flag is similar to *use\_builtin\_types* but it
    applies only to date/time values.

    Changed in version 3.3: The *use\_builtin\_types* flag was added.

    Changed in version 3.8: The *headers* parameter was added.

    Both the HTTP and HTTPS transports support the URL syntax extension for HTTP
    Basic Authentication: `http://user:pass@host:port/path`. The `user:pass`
    portion will be base64-encoded as an HTTP ‘Authorization’ header, and sent to
    the remote server as part of the connection process when invoking an XML-RPC
    method. You only need to use this if the remote server requires a Basic
    Authentication user and password.

    The returned instance is a proxy object with methods that can be used to invoke
    corresponding RPC calls on the remote server. If the remote server supports the
    introspection API, the proxy can also be used to query the remote server for the
    methods it supports (service discovery) and fetch other server-associated
    metadata.

    Types that are conformable (e.g. that can be marshalled through XML),
    include the following (and except where noted, they are unmarshalled
    as the same Python type):

    | XML-RPC type | Python type |
    | --- | --- |
    | `boolean` | [`bool`](functions.html#bool "bool") |
    | `int`, `i1`, `i2`, `i4`, `i8` or `biginteger` | [`int`](functions.html#int "int") in range from -2147483648 to 2147483647. Values get the `<int>` tag. |
    | `double` or `float` | [`float`](functions.html#float "float"). Values get the `<double>` tag. |
    | `string` | [`str`](stdtypes.html#str "str") |
    | `array` | [`list`](stdtypes.html#list "list") or [`tuple`](stdtypes.html#tuple "tuple") containing conformable elements. Arrays are returned as [`lists`](stdtypes.html#list "list"). |
    | `struct` | [`dict`](stdtypes.html#dict "dict"). Keys must be strings, values may be any conformable type. Objects of user-defined classes can be passed in; only their [`__dict__`](../reference/datamodel.html#object.__dict__ "object.__dict__") attribute is transmitted. |
    | `dateTime.iso8601` | [`DateTime`](#xmlrpc.client.DateTime "xmlrpc.client.DateTime") or [`datetime.datetime`](datetime.html#datetime.datetime "datetime.datetime"). Returned type depends on values of *use\_builtin\_types* and *use\_datetime* flags. |
    | `base64` | [`Binary`](#xmlrpc.client.Binary "xmlrpc.client.Binary"), [`bytes`](stdtypes.html#bytes "bytes") or [`bytearray`](stdtypes.html#bytearray "bytearray"). Returned type depends on the value of the *use\_builtin\_types* flag. |
    | `nil` | The `None` constant. Passing is allowed only if *allow\_none* is true. |
    | `bigdecimal` | [`decimal.Decimal`](decimal.html#decimal.Decimal "decimal.Decimal"). Returned type only. |

    This is the full set of data types supported by XML-RPC. Method calls may also
    raise a special [`Fault`](#xmlrpc.client.Fault "xmlrpc.client.Fault") instance, used to signal XML-RPC server errors, or
    [`ProtocolError`](#xmlrpc.client.ProtocolError "xmlrpc.client.ProtocolError") used to signal an error in the HTTP/HTTPS transport layer.
    Both [`Fault`](#xmlrpc.client.Fault "xmlrpc.client.Fault") and [`ProtocolError`](#xmlrpc.client.ProtocolError "xmlrpc.client.ProtocolError") derive from a base class called
    `Error`. Note that the xmlrpc client module currently does not marshal
    instances of subclasses of built-in types.

    When passing strings, characters special to XML such as `<`, `>`, and `&`
    will be automatically escaped. However, it’s the caller’s responsibility to
    ensure that the string is free of characters that aren’t allowed in XML, such as
    the control characters with ASCII values between 0 and 31 (except, of course,
    tab, newline and carriage return); failing to do this will result in an XML-RPC
    request that isn’t well-formed XML. If you have to pass arbitrary bytes
    via XML-RPC, use [`bytes`](stdtypes.html#bytes "bytes") or [`bytearray`](stdtypes.html#bytearray "bytearray") classes or the
    [`Binary`](#xmlrpc.client.Binary "xmlrpc.client.Binary") wrapper class described below.

    `Server` is retained as an alias for [`ServerProxy`](#xmlrpc.client.ServerProxy "xmlrpc.client.ServerProxy") for backwards
    compatibility. New code should use [`ServerProxy`](#xmlrpc.client.ServerProxy "xmlrpc.client.ServerProxy").

    Changed in version 3.5: Added the *context* argument.

    Changed in version 3.6: Added support of type tags with prefixes (e.g. `ex:nil`).
    Added support of unmarshalling additional types used by Apache XML-RPC
    implementation for numerics: `i1`, `i2`, `i8`, `biginteger`,
    `float` and `bigdecimal`.
    See <https://ws.apache.org/xmlrpc/types.html> for a description.