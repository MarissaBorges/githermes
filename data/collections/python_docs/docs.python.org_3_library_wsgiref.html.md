`wsgiref` — WSGI Utilities and Reference Implementation
=======================================================

**Source code:** [Lib/wsgiref](https://github.com/python/cpython/tree/3.13/Lib/wsgiref)

---

The Web Server Gateway Interface (WSGI) is a standard interface between web
server software and web applications written in Python. Having a standard
interface makes it easy to use an application that supports WSGI with a number
of different web servers.

Only authors of web servers and programming frameworks need to know every detail
and corner case of the WSGI design. You don’t need to understand every detail
of WSGI just to install a WSGI application or to write a web application using
an existing framework.

[`wsgiref`](#module-wsgiref "wsgiref: WSGI Utilities and Reference Implementation.") is a reference implementation of the WSGI specification that can
be used to add WSGI support to a web server or framework. It provides utilities
for manipulating WSGI environment variables and response headers, base classes
for implementing WSGI servers, a demo HTTP server that serves WSGI applications,
types for static type checking,
and a validation tool that checks WSGI servers and applications for conformance
to the WSGI specification ([**PEP 3333**](https://peps.python.org/pep-3333/)).

See [wsgi.readthedocs.io](https://wsgi.readthedocs.io/) for more information about WSGI, and links
to tutorials and other resources.

[`wsgiref.util`](#module-wsgiref.util "wsgiref.util: WSGI environment utilities.") – WSGI environment utilities
---------------------------------------------------------------------------------------------------------------

This module provides a variety of utility functions for working with WSGI
environments. A WSGI environment is a dictionary containing HTTP request
variables as described in [**PEP 3333**](https://peps.python.org/pep-3333/). All of the functions taking an *environ*
parameter expect a WSGI-compliant dictionary to be supplied; please see
[**PEP 3333**](https://peps.python.org/pep-3333/) for a detailed specification and
[`WSGIEnvironment`](#wsgiref.types.WSGIEnvironment "wsgiref.types.WSGIEnvironment") for a type alias that can be used
in type annotations.

wsgiref.util.guess\_scheme(*environ*)
:   Return a guess for whether `wsgi.url_scheme` should be “http” or “https”, by
    checking for a `HTTPS` environment variable in the *environ* dictionary. The
    return value is a string.

    This function is useful when creating a gateway that wraps CGI or a CGI-like
    protocol such as FastCGI. Typically, servers providing such protocols will
    include a `HTTPS` variable with a value of “1”, “yes”, or “on” when a request
    is received via SSL. So, this function returns “https” if such a value is
    found, and “http” otherwise.

wsgiref.util.request\_uri(*environ*, *include\_query=True*)
:   Return the full request URI, optionally including the query string, using the
    algorithm found in the “URL Reconstruction” section of [**PEP 3333**](https://peps.python.org/pep-3333/). If
    *include\_query* is false, the query string is not included in the resulting URI.

wsgiref.util.application\_uri(*environ*)
:   Similar to [`request_uri()`](#wsgiref.util.request_uri "wsgiref.util.request_uri"), except that the `PATH_INFO` and
    `QUERY_STRING` variables are ignored. The result is the base URI of the
    application object addressed by the request.

wsgiref.util.shift\_path\_info(*environ*)
:   Shift a single name from `PATH_INFO` to `SCRIPT_NAME` and return the name.
    The *environ* dictionary is *modified* in-place; use a copy if you need to keep
    the original `PATH_INFO` or `SCRIPT_NAME` intact.

    If there are no remaining path segments in `PATH_INFO`, `None` is returned.

    Typically, this routine is used to process each portion of a request URI path,
    for example to treat the path as a series of dictionary keys. This routine
    modifies the passed-in environment to make it suitable for invoking another WSGI
    application that is located at the target URI. For example, if there is a WSGI
    application at `/foo`, and the request URI path is `/foo/bar/baz`, and the
    WSGI application at `/foo` calls [`shift_path_info()`](#wsgiref.util.shift_path_info "wsgiref.util.shift_path_info"), it will receive the
    string “bar”, and the environment will be updated to be suitable for passing to
    a WSGI application at `/foo/bar`. That is, `SCRIPT_NAME` will change from
    `/foo` to `/foo/bar`, and `PATH_INFO` will change from `/bar/baz` to
    `/baz`.

    When `PATH_INFO` is just a “/”, this routine returns an empty string and
    appends a trailing slash to `SCRIPT_NAME`, even though empty path segments are
    normally ignored, and `SCRIPT_NAME` doesn’t normally end in a slash. This is
    intentional behavior, to ensure that an application can tell the difference
    between URIs ending in `/x` from ones ending in `/x/` when using this
    routine to do object traversal.

wsgiref.util.setup\_testing\_defaults(*environ*)
:   Update *environ* with trivial defaults for testing purposes.

    This routine adds various parameters required for WSGI, including `HTTP_HOST`,
    `SERVER_NAME`, `SERVER_PORT`, `REQUEST_METHOD`, `SCRIPT_NAME`,
    `PATH_INFO`, and all of the [**PEP 3333**](https://peps.python.org/pep-3333/)-defined `wsgi.*` variables. It
    only supplies default values, and does not replace any existing settings for
    these variables.

    This routine is intended to make it easier for unit tests of WSGI servers and
    applications to set up dummy environments. It should NOT be used by actual WSGI
    servers or applications, since the data is fake!

    Example usage (see also [`demo_app()`](#wsgiref.simple_server.demo_app "wsgiref.simple_server.demo_app")
    for another example):

    Copy

    ```
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    # A relatively simple WSGI application. It's going to print out the
    # environment dictionary after being updated by setup_testing_defaults
    def simple_app(environ, start_response):
        setup_testing_defaults(environ)

        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)

        ret = [("%s: %s\n" % (key, value)).encode("utf-8")
               for key, value in environ.items()]
        return ret

    with make_server('', 8000, simple_app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

    ```

In addition to the environment functions above, the [`wsgiref.util`](#module-wsgiref.util "wsgiref.util: WSGI environment utilities.") module
also provides these miscellaneous utilities:

wsgiref.util.is\_hop\_by\_hop(*header\_name*)
:   Return `True` if ‘header\_name’ is an HTTP/1.1 “Hop-by-Hop” header, as defined by
    [**RFC 2616**](https://datatracker.ietf.org/doc/html/rfc2616.html).

*class* wsgiref.util.FileWrapper(*filelike*, *blksize=8192*)
:   A concrete implementation of the [`wsgiref.types.FileWrapper`](#wsgiref.types.FileWrapper "wsgiref.types.FileWrapper")
    protocol used to convert a file-like object to an [iterator](../glossary.html#term-iterator).
    The resulting objects
    are [iterable](../glossary.html#term-iterable)s. As the object is iterated over, the
    optional *blksize* parameter will be repeatedly passed to the *filelike*
    object’s `read()` method to obtain bytestrings to yield. When `read()`
    returns an empty bytestring, iteration is ended and is not resumable.

    If *filelike* has a `close()` method, the returned object will also have a
    `close()` method, and it will invoke the *filelike* object’s `close()`
    method when called.

    Example usage:

    Copy

    ```
    from io import StringIO
    from wsgiref.util import FileWrapper

    # We're using a StringIO-buffer for as the file-like object
    filelike = StringIO("This is an example file-like object"*10)
    wrapper = FileWrapper(filelike, blksize=5)

    for chunk in wrapper:
        print(chunk)

    ```

    Changed in version 3.11: Support for [`__getitem__()`](../reference/datamodel.html#object.__getitem__ "object.__getitem__") method has been removed.

This module implements a simple HTTP server (based on [`http.server`](http.server.html#module-http.server "http.server: HTTP server and request handlers."))
that serves WSGI applications. Each server instance serves a single WSGI
application on a given host and port. If you want to serve multiple
applications on a single host and port, you should create a WSGI application
that parses `PATH_INFO` to select which application to invoke for each
request. (E.g., using the `shift_path_info()` function from
[`wsgiref.util`](#module-wsgiref.util "wsgiref.util: WSGI environment utilities.").)

wsgiref.simple\_server.make\_server(*host*, *port*, *app*, *server\_class=WSGIServer*, *handler\_class=WSGIRequestHandler*)
:   Create a new WSGI server listening on *host* and *port*, accepting connections
    for *app*. The return value is an instance of the supplied *server\_class*, and
    will process requests using the specified *handler\_class*. *app* must be a WSGI
    application object, as defined by [**PEP 3333**](https://peps.python.org/pep-3333/).

    Example usage:

    Copy

    ```
    from wsgiref.simple_server import make_server, demo_app

    with make_server('', 8000, demo_app) as httpd:
        print("Serving HTTP on port 8000...")

        # Respond to requests until process is killed
        httpd.serve_forever()

        # Alternative: serve one request, then exit
        httpd.handle_request()

    ```

wsgiref.simple\_server.demo\_app(*environ*, *start\_response*)
:   This function is a small but complete WSGI application that returns a text page
    containing the message “Hello world!” and a list of the key/value pairs provided
    in the *environ* parameter. It’s useful for verifying that a WSGI server (such
    as [`wsgiref.simple_server`](#module-wsgiref.simple_server "wsgiref.simple_server: A simple WSGI HTTP server.")) is able to run a simple WSGI application
    correctly.

    The *start\_response* callable should follow the [`StartResponse`](#wsgiref.types.StartResponse "wsgiref.types.StartResponse") protocol.

*class* wsgiref.simple\_server.WSGIServer(*server\_address*, *RequestHandlerClass*)
:   Create a [`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") instance. *server\_address* should be a
    `(host,port)` tuple, and *RequestHandlerClass* should be the subclass of
    [`http.server.BaseHTTPRequestHandler`](http.server.html#http.server.BaseHTTPRequestHandler "http.server.BaseHTTPRequestHandler") that will be used to process
    requests.

    You do not normally need to call this constructor, as the [`make_server()`](#wsgiref.simple_server.make_server "wsgiref.simple_server.make_server")
    function can handle all the details for you.

    [`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") is a subclass of [`http.server.HTTPServer`](http.server.html#http.server.HTTPServer "http.server.HTTPServer"), so all
    of its methods (such as `serve_forever()` and `handle_request()`) are
    available. [`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") also provides these WSGI-specific methods:

    set\_app(*application*)
    :   Sets the callable *application* as the WSGI application that will receive
        requests.

    get\_app()
    :   Returns the currently set application callable.

    Normally, however, you do not need to use these additional methods, as
    [`set_app()`](#wsgiref.simple_server.WSGIServer.set_app "wsgiref.simple_server.WSGIServer.set_app") is normally called by [`make_server()`](#wsgiref.simple_server.make_server "wsgiref.simple_server.make_server"), and the
    [`get_app()`](#wsgiref.simple_server.WSGIServer.get_app "wsgiref.simple_server.WSGIServer.get_app") exists mainly for the benefit of request handler instances.

*class* wsgiref.simple\_server.WSGIRequestHandler(*request*, *client\_address*, *server*)
:   Create an HTTP handler for the given *request* (i.e. a socket), *client\_address*
    (a `(host,port)` tuple), and *server* ([`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") instance).

    You do not need to create instances of this class directly; they are
    automatically created as needed by [`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") objects. You can,
    however, subclass this class and supply it as a *handler\_class* to the
    [`make_server()`](#wsgiref.simple_server.make_server "wsgiref.simple_server.make_server") function. Some possibly relevant methods for overriding in
    subclasses:

    get\_environ()
    :   Return a [`WSGIEnvironment`](#wsgiref.types.WSGIEnvironment "wsgiref.types.WSGIEnvironment") dictionary for a
        request. The default
        implementation copies the contents of the [`WSGIServer`](#wsgiref.simple_server.WSGIServer "wsgiref.simple_server.WSGIServer") object’s
        `base_environ` dictionary attribute and then adds various headers derived
        from the HTTP request. Each call to this method should return a new dictionary
        containing all of the relevant CGI environment variables as specified in
        [**PEP 3333**](https://peps.python.org/pep-3333/).

    get\_stderr()
    :   Return the object that should be used as the `wsgi.errors` stream. The default
        implementation just returns `sys.stderr`.

    handle()
    :   Process the HTTP request. The default implementation creates a handler instance
        using a [`wsgiref.handlers`](#module-wsgiref.handlers "wsgiref.handlers: WSGI server/gateway base classes.") class to implement the actual WSGI application
        interface.

When creating new WSGI application objects, frameworks, servers, or middleware,
it can be useful to validate the new code’s conformance using
[`wsgiref.validate`](#module-wsgiref.validate "wsgiref.validate: WSGI conformance checker."). This module provides a function that creates WSGI
application objects that validate communications between a WSGI server or
gateway and a WSGI application object, to check both sides for protocol
conformance.

Note that this utility does not guarantee complete [**PEP 3333**](https://peps.python.org/pep-3333/) compliance; an
absence of errors from this module does not necessarily mean that errors do not
exist. However, if this module does produce an error, then it is virtually
certain that either the server or application is not 100% compliant.

This module is based on the `paste.lint` module from Ian Bicking’s “Python
Paste” library.

wsgiref.validate.validator(*application*)
:   Wrap *application* and return a new WSGI application object. The returned
    application will forward all requests to the original *application*, and will
    check that both the *application* and the server invoking it are conforming to
    the WSGI specification and to [**RFC 2616**](https://datatracker.ietf.org/doc/html/rfc2616.html).

    Any detected nonconformance results in an [`AssertionError`](exceptions.html#AssertionError "AssertionError") being raised;
    note, however, that how these errors are handled is server-dependent. For
    example, [`wsgiref.simple_server`](#module-wsgiref.simple_server "wsgiref.simple_server: A simple WSGI HTTP server.") and other servers based on
    [`wsgiref.handlers`](#module-wsgiref.handlers "wsgiref.handlers: WSGI server/gateway base classes.") (that don’t override the error handling methods to do
    something else) will simply output a message that an error has occurred, and
    dump the traceback to `sys.stderr` or some other error stream.

    This wrapper may also generate output using the [`warnings`](warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module to
    indicate behaviors that are questionable but which may not actually be
    prohibited by [**PEP 3333**](https://peps.python.org/pep-3333/). Unless they are suppressed using Python command-line
    options or the [`warnings`](warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") API, any such warnings will be written to
    `sys.stderr` (*not* `wsgi.errors`, unless they happen to be the same
    object).

    Example usage:

    Copy

    ```
    from wsgiref.validate import validator
    from wsgiref.simple_server import make_server

    # Our callable object which is intentionally not compliant to the
    # standard, so the validator is going to break
    def simple_app(environ, start_response):
        status = '200 OK'  # HTTP Status
        headers = [('Content-type', 'text/plain')]  # HTTP Headers
        start_response(status, headers)

        # This is going to break because we need to return a list, and
        # the validator is going to inform us
        return b"Hello World"

    # This is the application wrapped in a validator
    validator_app = validator(simple_app)

    with make_server('', 8000, validator_app) as httpd:
        print("Listening on port 8000....")
        httpd.serve_forever()

    ```

This module provides base handler classes for implementing WSGI servers and
gateways. These base classes handle most of the work of communicating with a
WSGI application, as long as they are given a CGI-like environment, along with
input, output, and error streams.

*class* wsgiref.handlers.CGIHandler
:   CGI-based invocation via `sys.stdin`, `sys.stdout`, `sys.stderr` and
    `os.environ`. This is useful when you have a WSGI application and want to run
    it as a CGI script. Simply invoke `CGIHandler().run(app)`, where `app` is
    the WSGI application object you wish to invoke.

    This class is a subclass of [`BaseCGIHandler`](#wsgiref.handlers.BaseCGIHandler "wsgiref.handlers.BaseCGIHandler") that sets `wsgi.run_once`
    to true, `wsgi.multithread` to false, and `wsgi.multiprocess` to true, and
    always uses [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.") and [`os`](os.html#module-os "os: Miscellaneous operating system interfaces.") to obtain the necessary CGI streams and
    environment.

*class* wsgiref.handlers.IISCGIHandler
:   A specialized alternative to [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler"), for use when deploying on
    Microsoft’s IIS web server, without having set the config allowPathInfo
    option (IIS>=7) or metabase allowPathInfoForScriptMappings (IIS<7).

    By default, IIS gives a `PATH_INFO` that duplicates the `SCRIPT_NAME` at
    the front, causing problems for WSGI applications that wish to implement
    routing. This handler strips any such duplicated path.

    IIS can be configured to pass the correct `PATH_INFO`, but this causes
    another bug where `PATH_TRANSLATED` is wrong. Luckily this variable is
    rarely used and is not guaranteed by WSGI. On IIS<7, though, the
    setting can only be made on a vhost level, affecting all other script
    mappings, many of which break when exposed to the `PATH_TRANSLATED` bug.
    For this reason IIS<7 is almost never deployed with the fix (Even IIS7
    rarely uses it because there is still no UI for it.).

    There is no way for CGI code to tell whether the option was set, so a
    separate handler class is provided. It is used in the same way as
    [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler"), i.e., by calling `IISCGIHandler().run(app)`, where
    `app` is the WSGI application object you wish to invoke.

*class* wsgiref.handlers.BaseCGIHandler(*stdin*, *stdout*, *stderr*, *environ*, *multithread=True*, *multiprocess=False*)
:   Similar to [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler"), but instead of using the [`sys`](sys.html#module-sys "sys: Access system-specific parameters and functions.") and
    [`os`](os.html#module-os "os: Miscellaneous operating system interfaces.") modules, the CGI environment and I/O streams are specified explicitly.
    The *multithread* and *multiprocess* values are used to set the
    `wsgi.multithread` and `wsgi.multiprocess` flags for any applications run by
    the handler instance.

    This class is a subclass of [`SimpleHandler`](#wsgiref.handlers.SimpleHandler "wsgiref.handlers.SimpleHandler") intended for use with
    software other than HTTP “origin servers”. If you are writing a gateway
    protocol implementation (such as CGI, FastCGI, SCGI, etc.) that uses a
    `Status:` header to send an HTTP status, you probably want to subclass this
    instead of [`SimpleHandler`](#wsgiref.handlers.SimpleHandler "wsgiref.handlers.SimpleHandler").

*class* wsgiref.handlers.SimpleHandler(*stdin*, *stdout*, *stderr*, *environ*, *multithread=True*, *multiprocess=False*)
:   Similar to [`BaseCGIHandler`](#wsgiref.handlers.BaseCGIHandler "wsgiref.handlers.BaseCGIHandler"), but designed for use with HTTP origin
    servers. If you are writing an HTTP server implementation, you will probably
    want to subclass this instead of [`BaseCGIHandler`](#wsgiref.handlers.BaseCGIHandler "wsgiref.handlers.BaseCGIHandler").

    This class is a subclass of [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler"). It overrides the
    `__init__()`, [`get_stdin()`](#wsgiref.handlers.BaseHandler.get_stdin "wsgiref.handlers.BaseHandler.get_stdin"),
    [`get_stderr()`](#wsgiref.handlers.BaseHandler.get_stderr "wsgiref.handlers.BaseHandler.get_stderr"), [`add_cgi_vars()`](#wsgiref.handlers.BaseHandler.add_cgi_vars "wsgiref.handlers.BaseHandler.add_cgi_vars"),
    [`_write()`](#wsgiref.handlers.BaseHandler._write "wsgiref.handlers.BaseHandler._write"), and [`_flush()`](#wsgiref.handlers.BaseHandler._flush "wsgiref.handlers.BaseHandler._flush") methods to
    support explicitly setting the
    environment and streams via the constructor. The supplied environment and
    streams are stored in the `stdin`, `stdout`, `stderr`, and
    `environ` attributes.

    The [`write()`](io.html#io.BufferedIOBase.write "io.BufferedIOBase.write") method of *stdout* should write
    each chunk in full, like [`io.BufferedIOBase`](io.html#io.BufferedIOBase "io.BufferedIOBase").

*class* wsgiref.handlers.BaseHandler
:   This is an abstract base class for running WSGI applications. Each instance
    will handle a single HTTP request, although in principle you could create a
    subclass that was reusable for multiple requests.

    [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler") instances have only one method intended for external use:

    run(*app*)
    :   Run the specified WSGI application, *app*.

    All of the other [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler") methods are invoked by this method in the
    process of running the application, and thus exist primarily to allow
    customizing the process.

    The following methods MUST be overridden in a subclass:

    \_write(*data*)
    :   Buffer the bytes *data* for transmission to the client. It’s okay if this
        method actually transmits the data; [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler") just separates write
        and flush operations for greater efficiency when the underlying system actually
        has such a distinction.

    \_flush()
    :   Force buffered data to be transmitted to the client. It’s okay if this method
        is a no-op (i.e., if [`_write()`](#wsgiref.handlers.BaseHandler._write "wsgiref.handlers.BaseHandler._write") actually sends the data).

    get\_stdin()
    :   Return an object compatible with [`InputStream`](#wsgiref.types.InputStream "wsgiref.types.InputStream")
        suitable for use as the `wsgi.input` of the
        request currently being processed.

    get\_stderr()
    :   Return an object compatible with [`ErrorStream`](#wsgiref.types.ErrorStream "wsgiref.types.ErrorStream")
        suitable for use as the `wsgi.errors` of the
        request currently being processed.

    add\_cgi\_vars()
    :   Insert CGI variables for the current request into the `environ` attribute.

    Here are some other methods and attributes you may wish to override. This list
    is only a summary, however, and does not include every method that can be
    overridden. You should consult the docstrings and source code for additional
    information before attempting to create a customized [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler")
    subclass.

    Attributes and methods for customizing the WSGI environment:

    wsgi\_multithread
    :   The value to be used for the `wsgi.multithread` environment variable. It
        defaults to true in [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler"), but may have a different default (or
        be set by the constructor) in the other subclasses.

    wsgi\_multiprocess
    :   The value to be used for the `wsgi.multiprocess` environment variable. It
        defaults to true in [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler"), but may have a different default (or
        be set by the constructor) in the other subclasses.

    wsgi\_run\_once
    :   The value to be used for the `wsgi.run_once` environment variable. It
        defaults to false in [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler"), but [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler") sets it to
        true by default.

    os\_environ
    :   The default environment variables to be included in every request’s WSGI
        environment. By default, this is a copy of `os.environ` at the time that
        [`wsgiref.handlers`](#module-wsgiref.handlers "wsgiref.handlers: WSGI server/gateway base classes.") was imported, but subclasses can either create their own
        at the class or instance level. Note that the dictionary should be considered
        read-only, since the default value is shared between multiple classes and
        instances.

    server\_software
    :   If the [`origin_server`](#wsgiref.handlers.BaseHandler.origin_server "wsgiref.handlers.BaseHandler.origin_server") attribute is set, this attribute’s value is used to
        set the default `SERVER_SOFTWARE` WSGI environment variable, and also to set a
        default `Server:` header in HTTP responses. It is ignored for handlers (such
        as [`BaseCGIHandler`](#wsgiref.handlers.BaseCGIHandler "wsgiref.handlers.BaseCGIHandler") and [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler")) that are not HTTP origin
        servers.

        Changed in version 3.3: The term “Python” is replaced with implementation specific term like
        “CPython”, “Jython” etc.

    get\_scheme()
    :   Return the URL scheme being used for the current request. The default
        implementation uses the `guess_scheme()` function from [`wsgiref.util`](#module-wsgiref.util "wsgiref.util: WSGI environment utilities.")
        to guess whether the scheme should be “http” or “https”, based on the current
        request’s `environ` variables.

    setup\_environ()
    :   Set the `environ` attribute to a fully populated WSGI environment. The
        default implementation uses all of the above methods and attributes, plus the
        [`get_stdin()`](#wsgiref.handlers.BaseHandler.get_stdin "wsgiref.handlers.BaseHandler.get_stdin"), [`get_stderr()`](#wsgiref.handlers.BaseHandler.get_stderr "wsgiref.handlers.BaseHandler.get_stderr"), and [`add_cgi_vars()`](#wsgiref.handlers.BaseHandler.add_cgi_vars "wsgiref.handlers.BaseHandler.add_cgi_vars") methods and the
        [`wsgi_file_wrapper`](#wsgiref.handlers.BaseHandler.wsgi_file_wrapper "wsgiref.handlers.BaseHandler.wsgi_file_wrapper") attribute. It also inserts a `SERVER_SOFTWARE` key
        if not present, as long as the [`origin_server`](#wsgiref.handlers.BaseHandler.origin_server "wsgiref.handlers.BaseHandler.origin_server") attribute is a true value
        and the [`server_software`](#wsgiref.handlers.BaseHandler.server_software "wsgiref.handlers.BaseHandler.server_software") attribute is set.

    Methods and attributes for customizing exception handling:

    log\_exception(*exc\_info*)
    :   Log the *exc\_info* tuple in the server log. *exc\_info* is a `(type, value,
        traceback)` tuple. The default implementation simply writes the traceback to
        the request’s `wsgi.errors` stream and flushes it. Subclasses can override
        this method to change the format or retarget the output, mail the traceback to
        an administrator, or whatever other action may be deemed suitable.

    traceback\_limit
    :   The maximum number of frames to include in tracebacks output by the default
        [`log_exception()`](#wsgiref.handlers.BaseHandler.log_exception "wsgiref.handlers.BaseHandler.log_exception") method. If `None`, all frames are included.

    error\_output(*environ*, *start\_response*)
    :   This method is a WSGI application to generate an error page for the user. It is
        only invoked if an error occurs before headers are sent to the client.

        This method can access the current error using `sys.exception()`,
        and should pass that information to *start\_response* when calling it (as
        described in the “Error Handling” section of [**PEP 3333**](https://peps.python.org/pep-3333/)). In particular,
        the *start\_response* callable should follow the [`StartResponse`](#wsgiref.types.StartResponse "wsgiref.types.StartResponse")
        protocol.

        The default implementation just uses the [`error_status`](#wsgiref.handlers.BaseHandler.error_status "wsgiref.handlers.BaseHandler.error_status"),
        [`error_headers`](#wsgiref.handlers.BaseHandler.error_headers "wsgiref.handlers.BaseHandler.error_headers"), and [`error_body`](#wsgiref.handlers.BaseHandler.error_body "wsgiref.handlers.BaseHandler.error_body") attributes to generate an output
        page. Subclasses can override this to produce more dynamic error output.

        Note, however, that it’s not recommended from a security perspective to spit out
        diagnostics to any old user; ideally, you should have to do something special to
        enable diagnostic output, which is why the default implementation doesn’t
        include any.

    error\_status
    :   The HTTP status used for error responses. This should be a status string as
        defined in [**PEP 3333**](https://peps.python.org/pep-3333/); it defaults to a 500 code and message.

    error\_headers
    :   The HTTP headers used for error responses. This should be a list of WSGI
        response headers (`(name, value)` tuples), as described in [**PEP 3333**](https://peps.python.org/pep-3333/). The
        default list just sets the content type to `text/plain`.

    error\_body
    :   The error response body. This should be an HTTP response body bytestring. It
        defaults to the plain text, “A server error occurred. Please contact the
        administrator.”

    Methods and attributes for [**PEP 3333**](https://peps.python.org/pep-3333/)’s “Optional Platform-Specific File
    Handling” feature:

    wsgi\_file\_wrapper
    :   A `wsgi.file_wrapper` factory, compatible with
        [`wsgiref.types.FileWrapper`](#wsgiref.types.FileWrapper "wsgiref.types.FileWrapper"), or `None`. The default value
        of this attribute is the [`wsgiref.util.FileWrapper`](#wsgiref.util.FileWrapper "wsgiref.util.FileWrapper") class.

    sendfile()
    :   Override to implement platform-specific file transmission. This method is
        called only if the application’s return value is an instance of the class
        specified by the [`wsgi_file_wrapper`](#wsgiref.handlers.BaseHandler.wsgi_file_wrapper "wsgiref.handlers.BaseHandler.wsgi_file_wrapper") attribute. It should return a true
        value if it was able to successfully transmit the file, so that the default
        transmission code will not be executed. The default implementation of this
        method just returns a false value.

    Miscellaneous methods and attributes:

    origin\_server
    :   This attribute should be set to a true value if the handler’s [`_write()`](#wsgiref.handlers.BaseHandler._write "wsgiref.handlers.BaseHandler._write") and
        [`_flush()`](#wsgiref.handlers.BaseHandler._flush "wsgiref.handlers.BaseHandler._flush") are being used to communicate directly to the client, rather than
        via a CGI-like gateway protocol that wants the HTTP status in a special
        `Status:` header.

        This attribute’s default value is true in [`BaseHandler`](#wsgiref.handlers.BaseHandler "wsgiref.handlers.BaseHandler"), but false in
        [`BaseCGIHandler`](#wsgiref.handlers.BaseCGIHandler "wsgiref.handlers.BaseCGIHandler") and [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler").

    http\_version
    :   If [`origin_server`](#wsgiref.handlers.BaseHandler.origin_server "wsgiref.handlers.BaseHandler.origin_server") is true, this string attribute is used to set the HTTP
        version of the response set to the client. It defaults to `"1.0"`.

wsgiref.handlers.read\_environ()
:   Transcode CGI variables from `os.environ` to [**PEP 3333**](https://peps.python.org/pep-3333/) “bytes in unicode”
    strings, returning a new dictionary. This function is used by
    [`CGIHandler`](#wsgiref.handlers.CGIHandler "wsgiref.handlers.CGIHandler") and [`IISCGIHandler`](#wsgiref.handlers.IISCGIHandler "wsgiref.handlers.IISCGIHandler") in place of directly using
    `os.environ`, which is not necessarily WSGI-compliant on all platforms
    and web servers using Python 3 – specifically, ones where the OS’s
    actual environment is Unicode (i.e. Windows), or ones where the environment
    is bytes, but the system encoding used by Python to decode it is anything
    other than ISO-8859-1 (e.g. Unix systems using UTF-8).

    If you are implementing a CGI-based handler of your own, you probably want
    to use this routine instead of just copying values out of `os.environ`
    directly.

Examples
--------

This is a working “Hello World” WSGI application, where the *start\_response*
callable should follow the [`StartResponse`](#wsgiref.types.StartResponse "wsgiref.types.StartResponse") protocol:

Copy

```
"""
Every WSGI application must have an application object - a callable
object that accepts two arguments. For that purpose, we're going to
use a function (note that you're not limited to a function, you can
use a class for example). The first argument passed to the function
is a dictionary containing CGI-style environment variables and the
second variable is the callable object.
"""
from wsgiref.simple_server import make_server


def hello_world_app(environ, start_response):
    status = "200 OK"  # HTTP Status
    headers = [("Content-type", "text/plain; charset=utf-8")]  # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b"Hello World"]

with make_server("", 8000, hello_world_app) as httpd:
    print("Serving on port 8000...")

    # Serve until process is killed
    httpd.serve_forever()

```

Example of a WSGI application serving the current directory, accept optional
directory and port number (default: 8000) on the command line:

Copy

```
"""
Small wsgiref based web server. Takes a path to serve from and an
optional port number (defaults to 8000), then tries to serve files.
MIME types are guessed from the file names, 404 errors are raised
if the file is not found.
"""
import mimetypes
import os
import sys
from wsgiref import simple_server, util


def app(environ, respond):
    # Get the file name and MIME type
    fn = os.path.join(path, environ["PATH_INFO"][1:])
    if "." not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, "index.html")
    mime_type = mimetypes.guess_file_type(fn)[0]

    # Return 200 OK if file exists, otherwise 404 Not Found
    if os.path.exists(fn):
        respond("200 OK", [("Content-Type", mime_type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond("404 Not Found", [("Content-Type", "text/plain")])
        return [b"not found"]


if __name__ == "__main__":
    # Get the path and port from command-line arguments
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    # Make and start the server until control-c
    httpd = simple_server.make_server("", port, app)
    print(f"Serving {path} on port {port}, control-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()

```