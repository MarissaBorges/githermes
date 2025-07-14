urllib.request.urlopen(*url*, *data=None*, [*timeout*, ]*\**, *context=None*)
:   Open *url*, which can be either a string containing a valid, properly
    encoded URL, or a [`Request`](#urllib.request.Request "urllib.request.Request") object.

    *data* must be an object specifying additional data to be sent to the
    server, or `None` if no such data is needed. See [`Request`](#urllib.request.Request "urllib.request.Request")
    for details.

    urllib.request module uses HTTP/1.1 and includes `Connection:close` header
    in its HTTP requests.

    The optional *timeout* parameter specifies a timeout in seconds for
    blocking operations like the connection attempt (if not specified,
    the global default timeout setting will be used). This actually
    only works for HTTP, HTTPS and FTP connections.

    If *context* is specified, it must be a [`ssl.SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") instance
    describing the various SSL options. See [`HTTPSConnection`](http.client.html#http.client.HTTPSConnection "http.client.HTTPSConnection")
    for more details.

    This function always returns an object which can work as a
    [context manager](../glossary.html#term-context-manager) and has the properties *url*, *headers*, and *status*.
    See [`urllib.response.addinfourl`](#urllib.response.addinfourl "urllib.response.addinfourl") for more detail on these properties.

    For HTTP and HTTPS URLs, this function returns a
    [`http.client.HTTPResponse`](http.client.html#http.client.HTTPResponse "http.client.HTTPResponse") object slightly modified. In addition
    to the three new methods above, the msg attribute contains the
    same information as the [`reason`](http.client.html#http.client.HTTPResponse.reason "http.client.HTTPResponse.reason")
    attribute — the reason phrase returned by server — instead of
    the response headers as it is specified in the documentation for
    [`HTTPResponse`](http.client.html#http.client.HTTPResponse "http.client.HTTPResponse").

    For FTP, file, and data URLs and requests explicitly handled by legacy
    [`URLopener`](#urllib.request.URLopener "urllib.request.URLopener") and [`FancyURLopener`](#urllib.request.FancyURLopener "urllib.request.FancyURLopener") classes, this function
    returns a [`urllib.response.addinfourl`](#urllib.response.addinfourl "urllib.response.addinfourl") object.

    Raises [`URLError`](urllib.error.html#urllib.error.URLError "urllib.error.URLError") on protocol errors.

    Note that `None` may be returned if no handler handles the request (though
    the default installed global [`OpenerDirector`](#urllib.request.OpenerDirector "urllib.request.OpenerDirector") uses
    [`UnknownHandler`](#urllib.request.UnknownHandler "urllib.request.UnknownHandler") to ensure this never happens).

    In addition, if proxy settings are detected (for example, when a `*_proxy`
    environment variable like `http_proxy` is set),
    [`ProxyHandler`](#urllib.request.ProxyHandler "urllib.request.ProxyHandler") is default installed and makes sure the requests are
    handled through the proxy.

    The legacy `urllib.urlopen` function from Python 2.6 and earlier has been
    discontinued; [`urllib.request.urlopen()`](#urllib.request.urlopen "urllib.request.urlopen") corresponds to the old
    `urllib2.urlopen`. Proxy handling, which was done by passing a dictionary
    parameter to `urllib.urlopen`, can be obtained by using
    [`ProxyHandler`](#urllib.request.ProxyHandler "urllib.request.ProxyHandler") objects.

    The default opener raises an [auditing event](sys.html#auditing)
    `urllib.Request` with arguments `fullurl`, `data`, `headers`,
    `method` taken from the request object.

    Changed in version 3.2: *cafile* and *capath* were added.

    HTTPS virtual hosts are now supported if possible (that is, if
    [`ssl.HAS_SNI`](ssl.html#ssl.HAS_SNI "ssl.HAS_SNI") is true).

    *data* can be an iterable object.

    Changed in version 3.3: *cadefault* was added.

    Changed in version 3.4.3: *context* was added.

    Changed in version 3.10: HTTPS connection now send an ALPN extension with protocol indicator
    `http/1.1` when no *context* is given. Custom *context* should set
    ALPN protocols with [`set_alpn_protocols()`](ssl.html#ssl.SSLContext.set_alpn_protocols "ssl.SSLContext.set_alpn_protocols").

    Changed in version 3.13: Remove *cafile*, *capath* and *cadefault* parameters: use the *context*
    parameter instead.

*class* urllib.request.Request(*url*, *data=None*, *headers={}*, *origin\_req\_host=None*, *unverifiable=False*, *method=None*)
:   This class is an abstraction of a URL request.

    *url* should be a string containing a valid, properly encoded URL.

    *data* must be an object specifying additional data to send to the
    server, or `None` if no such data is needed. Currently HTTP
    requests are the only ones that use *data*. The supported object
    types include bytes, file-like objects, and iterables of bytes-like objects.
    If no `Content-Length` nor `Transfer-Encoding` header field
    has been provided, [`HTTPHandler`](#urllib.request.HTTPHandler "urllib.request.HTTPHandler") will set these headers according
    to the type of *data*. `Content-Length` will be used to send
    bytes objects, while `Transfer-Encoding: chunked` as specified in
    [**RFC 7230**](https://datatracker.ietf.org/doc/html/rfc7230.html), Section 3.3.1 will be used to send files and other iterables.

    For an HTTP POST request method, *data* should be a buffer in the
    standard *application/x-www-form-urlencoded* format. The
    [`urllib.parse.urlencode()`](urllib.parse.html#urllib.parse.urlencode "urllib.parse.urlencode") function takes a mapping or sequence
    of 2-tuples and returns an ASCII string in this format. It should
    be encoded to bytes before being used as the *data* parameter.

    *headers* should be a dictionary, and will be treated as if
    [`add_header()`](#urllib.request.Request.add_header "urllib.request.Request.add_header") was called with each key and value as arguments.
    This is often used to “spoof” the `User-Agent` header value, which is
    used by a browser to identify itself – some HTTP servers only
    allow requests coming from common browsers as opposed to scripts.
    For example, Mozilla Firefox may identify itself as `"Mozilla/5.0
    (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"`, while
    [`urllib`](urllib.html#module-urllib "urllib")’s default user agent string is
    `"Python-urllib/2.6"` (on Python 2.6).
    All header keys are sent in camel case.

    An appropriate `Content-Type` header should be included if the *data*
    argument is present. If this header has not been provided and *data*
    is not `None`, `Content-Type: application/x-www-form-urlencoded` will
    be added as a default.

    The next two arguments are only of interest for correct handling
    of third-party HTTP cookies:

    *origin\_req\_host* should be the request-host of the origin
    transaction, as defined by [**RFC 2965**](https://datatracker.ietf.org/doc/html/rfc2965.html). It defaults to
    `http.cookiejar.request_host(self)`. This is the host name or IP
    address of the original request that was initiated by the user.
    For example, if the request is for an image in an HTML document,
    this should be the request-host of the request for the page
    containing the image.

    *unverifiable* should indicate whether the request is unverifiable,
    as defined by [**RFC 2965**](https://datatracker.ietf.org/doc/html/rfc2965.html). It defaults to `False`. An unverifiable
    request is one whose URL the user did not have the option to
    approve. For example, if the request is for an image in an HTML
    document, and the user had no option to approve the automatic
    fetching of the image, this should be true.

    *method* should be a string that indicates the HTTP request method that
    will be used (e.g. `'HEAD'`). If provided, its value is stored in the
    [`method`](#urllib.request.Request.method "urllib.request.Request.method") attribute and is used by [`get_method()`](#urllib.request.Request.get_method "urllib.request.Request.get_method").
    The default is `'GET'` if *data* is `None` or `'POST'` otherwise.
    Subclasses may indicate a different default method by setting the
    [`method`](#urllib.request.Request.method "urllib.request.Request.method") attribute in the class itself.

    Note

    The request will not work as expected if the data object is unable
    to deliver its content more than once (e.g. a file or an iterable
    that can produce the content only once) and the request is retried
    for HTTP redirects or authentication. The *data* is sent to the
    HTTP server right away after the headers. There is no support for
    a 100-continue expectation in the library.

    Changed in version 3.3: [`Request.method`](#urllib.request.Request.method "urllib.request.Request.method") argument is added to the Request class.

    Changed in version 3.4: Default [`Request.method`](#urllib.request.Request.method "urllib.request.Request.method") may be indicated at the class level.

    Changed in version 3.6: Do not raise an error if the `Content-Length` has not been
    provided and *data* is neither `None` nor a bytes object.
    Fall back to use chunked transfer encoding instead.

Examples
--------

In addition to the examples below, more examples are given in
[HOWTO Fetch Internet Resources Using The urllib Package](../howto/urllib2.html#urllib-howto).

This example gets the python.org main page and displays the first 300 bytes of
it:

Copy

```
>>> import urllib.request
>>> with urllib.request.urlopen('http://www.python.org/') as f:
...     print(f.read(300))
...
b'<!doctype html>\n<!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->\n<!--[if IE 7]>      <html class="no-js ie7 lt-ie8 lt-ie9">          <![endif]-->\n<!--[if IE 8]>      <html class="no-js ie8 lt-ie9">

```

Note that urlopen returns a bytes object. This is because there is no way
for urlopen to automatically determine the encoding of the byte stream
it receives from the HTTP server. In general, a program will decode
the returned bytes object to string once it determines or guesses
the appropriate encoding.

The following HTML spec document, <https://html.spec.whatwg.org/#charset>, lists
the various ways in which an HTML or an XML document could have specified its
encoding information.

For additional information, see the W3C document: <https://www.w3.org/International/questions/qa-html-encoding-declarations>.

As the python.org website uses *utf-8* encoding as specified in its meta tag, we
will use the same for decoding the bytes object:

Copy

```
>>> with urllib.request.urlopen('http://www.python.org/') as f:
...     print(f.read(100).decode('utf-8'))
...
<!doctype html>
<!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->
<!-

```

It is also possible to achieve the same result without using the
[context manager](../glossary.html#term-context-manager) approach:

Copy

```
>>> import urllib.request
>>> f = urllib.request.urlopen('http://www.python.org/')
>>> try:
...     print(f.read(100).decode('utf-8'))
... finally:
...     f.close()
...
<!doctype html>
<!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->
<!--

```

In the following example, we are sending a data-stream to the stdin of a CGI
and reading the data it returns to us. Note that this example will only work
when the Python installation supports SSL.

Copy

```
>>> import urllib.request
>>> req = urllib.request.Request(url='https://localhost/cgi-bin/test.cgi',
...                       data=b'This data is passed to stdin of the CGI')
>>> with urllib.request.urlopen(req) as f:
...     print(f.read().decode('utf-8'))
...
Got Data: "This data is passed to stdin of the CGI"

```

The code for the sample CGI used in the above example is:

Copy

```
#!/usr/bin/env python
import sys
data = sys.stdin.read()
print('Content-type: text/plain\n\nGot Data: "%s"' % data)

```

Here is an example of doing a `PUT` request using [`Request`](#urllib.request.Request "urllib.request.Request"):

Copy

```
import urllib.request
DATA = b'some data'
req = urllib.request.Request(url='http://localhost:8080', data=DATA, method='PUT')
with urllib.request.urlopen(req) as f:
    pass
print(f.status)
print(f.reason)

```

Use of Basic HTTP Authentication:

Copy

```
import urllib.request
# Create an OpenerDirector with support for Basic HTTP Authentication...
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='PDQ Application',
                          uri='https://mahler:8092/site-updates.py',
                          user='klem',
                          passwd='kadidd!ehopper')
opener = urllib.request.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib.request.install_opener(opener)
with urllib.request.urlopen('http://www.example.com/login.html') as f:
    print(f.read().decode('utf-8'))

```

[`build_opener()`](#urllib.request.build_opener "urllib.request.build_opener") provides many handlers by default, including a
[`ProxyHandler`](#urllib.request.ProxyHandler "urllib.request.ProxyHandler"). By default, [`ProxyHandler`](#urllib.request.ProxyHandler "urllib.request.ProxyHandler") uses the environment
variables named `<scheme>_proxy`, where `<scheme>` is the URL scheme
involved. For example, the `http_proxy` environment variable is read to
obtain the HTTP proxy’s URL.

This example replaces the default [`ProxyHandler`](#urllib.request.ProxyHandler "urllib.request.ProxyHandler") with one that uses
programmatically supplied proxy URLs, and adds proxy authorization support with
[`ProxyBasicAuthHandler`](#urllib.request.ProxyBasicAuthHandler "urllib.request.ProxyBasicAuthHandler").

Copy

```
proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
# This time, rather than install the OpenerDirector, we use it directly:
with opener.open('http://www.example.com/login.html') as f:
   print(f.read().decode('utf-8'))

```

Adding HTTP headers:

Use the *headers* argument to the [`Request`](#urllib.request.Request "urllib.request.Request") constructor, or:

Copy

```
import urllib.request
req = urllib.request.Request('http://www.example.com/')
req.add_header('Referer', 'http://www.python.org/')
# Customize the default User-Agent header value:
req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
with urllib.request.urlopen(req) as f:
    print(f.read().decode('utf-8'))

```

[`OpenerDirector`](#urllib.request.OpenerDirector "urllib.request.OpenerDirector") automatically adds a header to
every [`Request`](#urllib.request.Request "urllib.request.Request"). To change this:

Copy

```
import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
with opener.open('http://www.example.com/') as f:
   print(f.read().decode('utf-8'))

```

Also, remember that a few standard headers (,
and )
are added when the [`Request`](#urllib.request.Request "urllib.request.Request") is passed to [`urlopen()`](#urllib.request.urlopen "urllib.request.urlopen") (or
[`OpenerDirector.open()`](#urllib.request.OpenerDirector.open "urllib.request.OpenerDirector.open")).

Here is an example session that uses the `GET` method to retrieve a URL
containing parameters:

Copy

```
>>> import urllib.request
>>> import urllib.parse
>>> params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
>>> url = "http://www.musi-cal.com/cgi-bin/query?%s" % params
>>> with urllib.request.urlopen(url) as f:
...     print(f.read().decode('utf-8'))
...

```

The following example uses the `POST` method instead. Note that params output
from urlencode is encoded to bytes before it is sent to urlopen as data:

Copy

```
>>> import urllib.request
>>> import urllib.parse
>>> data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
>>> data = data.encode('ascii')
>>> with urllib.request.urlopen("http://requestb.in/xrbl82xr", data) as f:
...     print(f.read().decode('utf-8'))
...

```

The following example uses an explicitly specified HTTP proxy, overriding
environment settings:

Copy

```
>>> import urllib.request
>>> proxies = {'http': 'http://proxy.example.com:8080/'}
>>> opener = urllib.request.FancyURLopener(proxies)
>>> with opener.open("http://www.python.org") as f:
...     f.read().decode('utf-8')
...

```

The following example uses no proxies at all, overriding environment settings:

Copy

```
>>> import urllib.request
>>> opener = urllib.request.FancyURLopener({})
>>> with opener.open("http://www.python.org/") as f:
...     f.read().decode('utf-8')
...

```