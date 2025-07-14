`xmlrpc.server` — Basic XML-RPC servers
=======================================

**Source code:** [Lib/xmlrpc/server.py](https://github.com/python/cpython/tree/3.13/Lib/xmlrpc/server.py)

---

The [`xmlrpc.server`](#module-xmlrpc.server "xmlrpc.server: Basic XML-RPC server implementations.") module provides a basic server framework for XML-RPC
servers written in Python. Servers can either be free standing, using
[`SimpleXMLRPCServer`](#xmlrpc.server.SimpleXMLRPCServer "xmlrpc.server.SimpleXMLRPCServer"), or embedded in a CGI environment, using
[`CGIXMLRPCRequestHandler`](#xmlrpc.server.CGIXMLRPCRequestHandler "xmlrpc.server.CGIXMLRPCRequestHandler").

Warning

The [`xmlrpc.server`](#module-xmlrpc.server "xmlrpc.server: Basic XML-RPC server implementations.") module is not secure against maliciously
constructed data. If you need to parse untrusted or unauthenticated data,
see [XML security](xml.html#xml-security).

*class* xmlrpc.server.SimpleXMLRPCServer(*addr*, *requestHandler=SimpleXMLRPCRequestHandler*, *logRequests=True*, *allow\_none=False*, *encoding=None*, *bind\_and\_activate=True*, *use\_builtin\_types=False*)
:   Create a new server instance. This class provides methods for registration of
    functions that can be called by the XML-RPC protocol. The *requestHandler*
    parameter should be a factory for request handler instances; it defaults to
    [`SimpleXMLRPCRequestHandler`](#xmlrpc.server.SimpleXMLRPCRequestHandler "xmlrpc.server.SimpleXMLRPCRequestHandler"). The *addr* and *requestHandler* parameters
    are passed to the [`socketserver.TCPServer`](socketserver.html#socketserver.TCPServer "socketserver.TCPServer") constructor. If *logRequests*
    is true (the default), requests will be logged; setting this parameter to false
    will turn off logging. The *allow\_none* and *encoding* parameters are passed
    on to [`xmlrpc.client`](xmlrpc.client.html#module-xmlrpc.client "xmlrpc.client: XML-RPC client access.") and control the XML-RPC responses that will be returned
    from the server. The *bind\_and\_activate* parameter controls whether
    `server_bind()` and `server_activate()` are called immediately by the
    constructor; it defaults to true. Setting it to false allows code to manipulate
    the *allow\_reuse\_address* class variable before the address is bound.
    The *use\_builtin\_types* parameter is passed to the
    [`loads()`](xmlrpc.client.html#xmlrpc.client.loads "xmlrpc.client.loads") function and controls which types are processed
    when date/times values or binary data are received; it defaults to false.

    Changed in version 3.3: The *use\_builtin\_types* flag was added.

*class* xmlrpc.server.CGIXMLRPCRequestHandler(*allow\_none=False*, *encoding=None*, *use\_builtin\_types=False*)
:   Create a new instance to handle XML-RPC requests in a CGI environment. The
    *allow\_none* and *encoding* parameters are passed on to [`xmlrpc.client`](xmlrpc.client.html#module-xmlrpc.client "xmlrpc.client: XML-RPC client access.")
    and control the XML-RPC responses that will be returned from the server.
    The *use\_builtin\_types* parameter is passed to the
    [`loads()`](xmlrpc.client.html#xmlrpc.client.loads "xmlrpc.client.loads") function and controls which types are processed
    when date/times values or binary data are received; it defaults to false.

    Changed in version 3.3: The *use\_builtin\_types* flag was added.

*class* xmlrpc.server.SimpleXMLRPCRequestHandler
:   Create a new request handler instance. This request handler supports `POST`
    requests and modifies logging so that the *logRequests* parameter to the
    [`SimpleXMLRPCServer`](#xmlrpc.server.SimpleXMLRPCServer "xmlrpc.server.SimpleXMLRPCServer") constructor parameter is honored.

SimpleXMLRPCServer Objects
--------------------------

The [`SimpleXMLRPCServer`](#xmlrpc.server.SimpleXMLRPCServer "xmlrpc.server.SimpleXMLRPCServer") class is based on
[`socketserver.TCPServer`](socketserver.html#socketserver.TCPServer "socketserver.TCPServer") and provides a means of creating simple, stand
alone XML-RPC servers.

SimpleXMLRPCServer.register\_function(*function=None*, *name=None*)
:   Register a function that can respond to XML-RPC requests. If *name* is given,
    it will be the method name associated with *function*, otherwise
    [`function.__name__`](../reference/datamodel.html#function.__name__ "function.__name__") will be used. *name* is a string, and may contain
    characters not legal in Python identifiers, including the period character.

    This method can also be used as a decorator. When used as a decorator,
    *name* can only be given as a keyword argument to register *function* under
    *name*. If no *name* is given, [`function.__name__`](../reference/datamodel.html#function.__name__ "function.__name__") will be used.

SimpleXMLRPCServer.register\_instance(*instance*, *allow\_dotted\_names=False*)
:   Register an object which is used to expose method names which have not been
    registered using [`register_function()`](#xmlrpc.server.SimpleXMLRPCServer.register_function "xmlrpc.server.SimpleXMLRPCServer.register_function"). If *instance* contains a
    `_dispatch()` method, it is called with the requested method name and the
    parameters from the request. Its API is `def _dispatch(self, method, params)`
    (note that *params* does not represent a variable argument list). If it calls
    an underlying function to perform its task, that function is called as
    `func(*params)`, expanding the parameter list. The return value from
    `_dispatch()` is returned to the client as the result. If *instance* does
    not have a `_dispatch()` method, it is searched for an attribute matching
    the name of the requested method.

    If the optional *allow\_dotted\_names* argument is true and the instance does not
    have a `_dispatch()` method, then if the requested method name contains
    periods, each component of the method name is searched for individually, with
    the effect that a simple hierarchical search is performed. The value found from
    this search is then called with the parameters from the request, and the return
    value is passed back to the client.

    Warning

    Enabling the *allow\_dotted\_names* option allows intruders to access your
    module’s global variables and may allow intruders to execute arbitrary code on
    your machine. Only use this option on a secure, closed network.

SimpleXMLRPCServer.register\_introspection\_functions()
:   Registers the XML-RPC introspection functions `system.listMethods`,
    `system.methodHelp` and `system.methodSignature`.

SimpleXMLRPCServer.register\_multicall\_functions()
:   Registers the XML-RPC multicall function system.multicall.

SimpleXMLRPCRequestHandler.rpc\_paths
:   An attribute value that must be a tuple listing valid path portions of the URL
    for receiving XML-RPC requests. Requests posted to other paths will result in a
    404 “no such page” HTTP error. If this tuple is empty, all paths will be
    considered valid. The default value is `('/', '/RPC2')`.

### SimpleXMLRPCServer Example

Server code:

Copy

```
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register pow() function; this will use the value of
    # pow.__name__ as the name, which is just 'pow'.
    server.register_function(pow)

    # Register a function under a different name
    def adder_function(x, y):
        return x + y
    server.register_function(adder_function, 'add')

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class MyFuncs:
        def mul(self, x, y):
            return x * y

    server.register_instance(MyFuncs())

    # Run the server's main loop
    server.serve_forever()

```

The following client code will call the methods made available by the preceding
server:

Copy

```
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')
print(s.pow(2,3))  # Returns 2**3 = 8
print(s.add(2,3))  # Returns 5
print(s.mul(5,2))  # Returns 5*2 = 10

# Print list of available methods
print(s.system.listMethods())

```

`register_function()` can also be used as a decorator. The previous server
example can register functions in a decorator way:

Copy

```
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register pow() function; this will use the value of
    # pow.__name__ as the name, which is just 'pow'.
    server.register_function(pow)

    # Register a function under a different name, using
    # register_function as a decorator. *name* can only be given
    # as a keyword argument.
    @server.register_function(name='add')
    def adder_function(x, y):
        return x + y

    # Register a function under function.__name__.
    @server.register_function
    def mul(x, y):
        return x * y

    server.serve_forever()

```

The following example included in the `Lib/xmlrpc/server.py` module shows
a server allowing dotted names and registering a multicall function.

Warning

Enabling the *allow\_dotted\_names* option allows intruders to access your
module’s global variables and may allow intruders to execute arbitrary code on
your machine. Only use this example only within a secure, closed network.

Copy

```
import datetime

class ExampleService:
    def getData(self):
        return '42'

    class currentTime:
        @staticmethod
        def getCurrentTime():
            return datetime.datetime.now()

with SimpleXMLRPCServer(("localhost", 8000)) as server:
    server.register_function(pow)
    server.register_function(lambda x,y: x+y, 'add')
    server.register_instance(ExampleService(), allow_dotted_names=True)
    server.register_multicall_functions()
    print('Serving XML-RPC on localhost port 8000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)

```

This ExampleService demo can be invoked from the command line:

Copy

```
python -m xmlrpc.server

```

The client that interacts with the above server is included in
`Lib/xmlrpc/client.py`:

Copy

```
server = ServerProxy("http://localhost:8000")

try:
    print(server.currentTime.getCurrentTime())
except Error as v:
    print("ERROR", v)

multi = MultiCall(server)
multi.getData()
multi.pow(2,9)
multi.add(1,2)
try:
    for response in multi():
        print(response)
except Error as v:
    print("ERROR", v)

```

This client which interacts with the demo XMLRPC server can be invoked as:

Copy

```
python -m xmlrpc.client

```

CGIXMLRPCRequestHandler
-----------------------

The [`CGIXMLRPCRequestHandler`](#xmlrpc.server.CGIXMLRPCRequestHandler "xmlrpc.server.CGIXMLRPCRequestHandler") class can be used to handle XML-RPC
requests sent to Python CGI scripts.

CGIXMLRPCRequestHandler.register\_function(*function=None*, *name=None*)
:   Register a function that can respond to XML-RPC requests. If *name* is given,
    it will be the method name associated with *function*, otherwise
    [`function.__name__`](../reference/datamodel.html#function.__name__ "function.__name__") will be used. *name* is a string, and may contain
    characters not legal in Python identifiers, including the period character.

    This method can also be used as a decorator. When used as a decorator,
    *name* can only be given as a keyword argument to register *function* under
    *name*. If no *name* is given, [`function.__name__`](../reference/datamodel.html#function.__name__ "function.__name__") will be used.

CGIXMLRPCRequestHandler.register\_instance(*instance*)
:   Register an object which is used to expose method names which have not been
    registered using [`register_function()`](#xmlrpc.server.CGIXMLRPCRequestHandler.register_function "xmlrpc.server.CGIXMLRPCRequestHandler.register_function"). If instance contains a
    `_dispatch()` method, it is called with the requested method name and the
    parameters from the request; the return value is returned to the client as the
    result. If instance does not have a `_dispatch()` method, it is searched
    for an attribute matching the name of the requested method; if the requested
    method name contains periods, each component of the method name is searched for
    individually, with the effect that a simple hierarchical search is performed.
    The value found from this search is then called with the parameters from the
    request, and the return value is passed back to the client.

CGIXMLRPCRequestHandler.register\_introspection\_functions()
:   Register the XML-RPC introspection functions `system.listMethods`,
    `system.methodHelp` and `system.methodSignature`.

CGIXMLRPCRequestHandler.register\_multicall\_functions()
:   Register the XML-RPC multicall function `system.multicall`.

CGIXMLRPCRequestHandler.handle\_request(*request\_text=None*)
:   Handle an XML-RPC request. If *request\_text* is given, it should be the POST
    data provided by the HTTP server, otherwise the contents of stdin will be used.

Example:

Copy

```
class MyFuncs:
    def mul(self, x, y):
        return x * y


handler = CGIXMLRPCRequestHandler()
handler.register_function(pow)
handler.register_function(lambda x,y: x+y, 'add')
handler.register_introspection_functions()
handler.register_instance(MyFuncs())
handler.handle_request()

```

Documenting XMLRPC server
-------------------------

These classes extend the above classes to serve HTML documentation in response
to HTTP GET requests. Servers can either be free standing, using
[`DocXMLRPCServer`](#xmlrpc.server.DocXMLRPCServer "xmlrpc.server.DocXMLRPCServer"), or embedded in a CGI environment, using
[`DocCGIXMLRPCRequestHandler`](#xmlrpc.server.DocCGIXMLRPCRequestHandler "xmlrpc.server.DocCGIXMLRPCRequestHandler").

*class* xmlrpc.server.DocXMLRPCServer(*addr*, *requestHandler=DocXMLRPCRequestHandler*, *logRequests=True*, *allow\_none=False*, *encoding=None*, *bind\_and\_activate=True*, *use\_builtin\_types=True*)
:   Create a new server instance. All parameters have the same meaning as for
    [`SimpleXMLRPCServer`](#xmlrpc.server.SimpleXMLRPCServer "xmlrpc.server.SimpleXMLRPCServer"); *requestHandler* defaults to
    [`DocXMLRPCRequestHandler`](#xmlrpc.server.DocXMLRPCRequestHandler "xmlrpc.server.DocXMLRPCRequestHandler").

    Changed in version 3.3: The *use\_builtin\_types* flag was added.

*class* xmlrpc.server.DocCGIXMLRPCRequestHandler
:   Create a new instance to handle XML-RPC requests in a CGI environment.

*class* xmlrpc.server.DocXMLRPCRequestHandler
:   Create a new request handler instance. This request handler supports XML-RPC
    POST requests, documentation GET requests, and modifies logging so that the
    *logRequests* parameter to the [`DocXMLRPCServer`](#xmlrpc.server.DocXMLRPCServer "xmlrpc.server.DocXMLRPCServer") constructor parameter is
    honored.

DocXMLRPCServer Objects
-----------------------

The [`DocXMLRPCServer`](#xmlrpc.server.DocXMLRPCServer "xmlrpc.server.DocXMLRPCServer") class is derived from [`SimpleXMLRPCServer`](#xmlrpc.server.SimpleXMLRPCServer "xmlrpc.server.SimpleXMLRPCServer")
and provides a means of creating self-documenting, stand alone XML-RPC
servers. HTTP POST requests are handled as XML-RPC method calls. HTTP GET
requests are handled by generating pydoc-style HTML documentation. This allows a
server to provide its own web-based documentation.

DocXMLRPCServer.set\_server\_title(*server\_title*)
:   Set the title used in the generated HTML documentation. This title will be used
    inside the HTML “title” element.

DocXMLRPCServer.set\_server\_name(*server\_name*)
:   Set the name used in the generated HTML documentation. This name will appear at
    the top of the generated documentation inside a “h1” element.

DocXMLRPCServer.set\_server\_documentation(*server\_documentation*)
:   Set the description used in the generated HTML documentation. This description
    will appear as a paragraph, below the server name, in the documentation.

DocCGIXMLRPCRequestHandler
--------------------------

The [`DocCGIXMLRPCRequestHandler`](#xmlrpc.server.DocCGIXMLRPCRequestHandler "xmlrpc.server.DocCGIXMLRPCRequestHandler") class is derived from
[`CGIXMLRPCRequestHandler`](#xmlrpc.server.CGIXMLRPCRequestHandler "xmlrpc.server.CGIXMLRPCRequestHandler") and provides a means of creating
self-documenting, XML-RPC CGI scripts. HTTP POST requests are handled as XML-RPC
method calls. HTTP GET requests are handled by generating pydoc-style HTML
documentation. This allows a server to provide its own web-based documentation.

DocCGIXMLRPCRequestHandler.set\_server\_title(*server\_title*)
:   Set the title used in the generated HTML documentation. This title will be used
    inside the HTML “title” element.

DocCGIXMLRPCRequestHandler.set\_server\_name(*server\_name*)
:   Set the name used in the generated HTML documentation. This name will appear at
    the top of the generated documentation inside a “h1” element.

DocCGIXMLRPCRequestHandler.set\_server\_documentation(*server\_documentation*)
:   Set the description used in the generated HTML documentation. This description
    will appear as a paragraph, below the server name, in the documentation.