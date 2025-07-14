:   This will send a request to the server using the HTTP request
    method *method* and the request URI *url*. The provided *url* must be
    an absolute path to conform with [**RFC 2616 §5.1.2**](https://datatracker.ietf.org/doc/html/rfc2616.html#section-5.1.2)
    (unless connecting to an HTTP proxy server or using the `OPTIONS` or
    `CONNECT` methods).

    If *body* is specified, the specified data is sent after the headers are
    finished. It may be a [`str`](stdtypes.html#str "str"), a [bytes-like object](../glossary.html#term-bytes-like-object), an
    open [file object](../glossary.html#term-file-object), or an iterable of [`bytes`](stdtypes.html#bytes "bytes"). If *body*
    is a string, it is encoded as ISO-8859-1, the default for HTTP. If it
    is a bytes-like object, the bytes are sent as is. If it is a [file
    object](../glossary.html#term-file-object), the contents of the file is sent; this file object should
    support at least the `read()` method. If the file object is an
    instance of [`io.TextIOBase`](io.html#io.TextIOBase "io.TextIOBase"), the data returned by the `read()`
    method will be encoded as ISO-8859-1, otherwise the data returned by
    `read()` is sent as is. If *body* is an iterable, the elements of the
    iterable are sent as is until the iterable is exhausted.

    The *headers* argument should be a mapping of extra HTTP headers to send
    with the request. A [**Host header**](https://datatracker.ietf.org/doc/html/rfc2616.html#section-14.23)
    must be provided to conform with [**RFC 2616 §5.1.2**](https://datatracker.ietf.org/doc/html/rfc2616.html#section-5.1.2)
    (unless connecting to an HTTP proxy server or using the `OPTIONS` or
    `CONNECT` methods).

    If *headers* contains neither Content-Length nor Transfer-Encoding,
    but there is a request body, one of those
    header fields will be added automatically. If
    *body* is `None`, the Content-Length header is set to `0` for
    methods that expect a body (`PUT`, `POST`, and `PATCH`). If
    *body* is a string or a bytes-like object that is not also a
    [file](../glossary.html#term-file-object), the Content-Length header is
    set to its length. Any other type of *body* (files
    and iterables in general) will be chunk-encoded, and the
    Transfer-Encoding header will automatically be set instead of
    Content-Length.

    The *encode\_chunked* argument is only relevant if Transfer-Encoding is
    specified in *headers*. If *encode\_chunked* is `False`, the
    HTTPConnection object assumes that all encoding is handled by the
    calling code. If it is `True`, the body will be chunk-encoded.

    For example, to perform a `GET` request to `https://docs.python.org/3/`:

    Copy

    ```
    >>> import http.client
    >>> host = "docs.python.org"
    >>> conn = http.client.HTTPSConnection(host)
    >>> conn.request("GET", "/3/", headers={"Host": host})
    >>> response = conn.getresponse()
    >>> print(response.status, response.reason)
    200 OK

    ```

    Note

    Chunked transfer encoding has been added to the HTTP protocol
    version 1.1. Unless the HTTP server is known to handle HTTP 1.1,
    the caller must either specify the Content-Length, or must pass a
    [`str`](stdtypes.html#str "str") or bytes-like object that is not also a file as the
    body representation.

    Changed in version 3.2: *body* can now be an iterable.

    Changed in version 3.6: If neither Content-Length nor Transfer-Encoding are set in
    *headers*, file and iterable *body* objects are now chunk-encoded.
    The *encode\_chunked* argument was added.
    No attempt is made to determine the Content-Length for file
    objects.