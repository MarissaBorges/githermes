:   This function wraps the C function `getaddrinfo` of the underlying system.

    Translate the *host*/*port* argument into a sequence of 5-tuples that contain
    all the necessary arguments for creating a socket connected to that service.
    *host* is a domain name, a string representation of an IPv4/v6 address
    or `None`. *port* is a string service name such as `'http'`, a numeric
    port number or `None`. By passing `None` as the value of *host*
    and *port*, you can pass `NULL` to the underlying C API.

    The *family*, *type* and *proto* arguments can be optionally specified
    in order to provide options and limit the list of addresses returned.
    Pass their default values ([`AF_UNSPEC`](#socket.AF_UNSPEC "socket.AF_UNSPEC"), 0, and 0, respectively)
    to not limit the results. See the note below for details.

    The *flags* argument can be one or several of the `AI_*` constants,
    and will influence how results are computed and returned.
    For example, `AI_NUMERICHOST` will disable domain name resolution
    and will raise an error if *host* is a domain name.

    The function returns a list of 5-tuples with the following structure:

    `(family, type, proto, canonname, sockaddr)`

    In these tuples, *family*, *type*, *proto* are all integers and are
    meant to be passed to the [`socket()`](#socket.socket "socket.socket") function. *canonname* will be
    a string representing the canonical name of the *host* if
    `AI_CANONNAME` is part of the *flags* argument; else *canonname*
    will be empty. *sockaddr* is a tuple describing a socket address, whose
    format depends on the returned *family* (a `(address, port)` 2-tuple for
    [`AF_INET`](#socket.AF_INET "socket.AF_INET"), a `(address, port, flowinfo, scope_id)` 4-tuple for
    [`AF_INET6`](#socket.AF_INET6 "socket.AF_INET6")), and is meant to be passed to the [`socket.connect()`](#socket.socket.connect "socket.socket.connect")
    method.

    Note

    If you intend to use results from `getaddrinfo()` to create a socket
    (rather than, for example, retrieve *canonname*),
    consider limiting the results by *type* (e.g. [`SOCK_STREAM`](#socket.SOCK_STREAM "socket.SOCK_STREAM") or
    [`SOCK_DGRAM`](#socket.SOCK_DGRAM "socket.SOCK_DGRAM")) and/or *proto* (e.g. `IPPROTO_TCP` or
    `IPPROTO_UDP`) that your application can handle.

    The behavior with default values of *family*, *type*, *proto*
    and *flags* is system-specific.

    Many systems (for example, most Linux configurations) will return a sorted
    list of all matching addresses.
    These addresses should generally be tried in order until a connection succeeds
    (possibly tried in parallel, for example, using a [Happy Eyeballs](https://en.wikipedia.org/wiki/Happy_Eyeballs) algorithm).
    In these cases, limiting the *type* and/or *proto* can help eliminate
    unsuccessful or unusable connection attempts.

    Some systems will, however, only return a single address.
    (For example, this was reported on Solaris and AIX configurations.)
    On these systems, limiting the *type* and/or *proto* helps ensure that
    this address is usable.

    Raises an [auditing event](sys.html#auditing) `socket.getaddrinfo` with arguments `host`, `port`, `family`, `type`, `protocol`.

    The following example fetches address information for a hypothetical TCP
    connection to `example.org` on port 80 (results may differ on your
    system if IPv6 isn’t enabled):

    Copy

    ```
    >>> socket.getaddrinfo("example.org", 80, proto=socket.IPPROTO_TCP)
    [(socket.AF_INET6, socket.SOCK_STREAM,
     6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
     (socket.AF_INET, socket.SOCK_STREAM,
     6, '', ('93.184.216.34', 80))]

    ```

    Changed in version 3.2: parameters can now be passed using keyword arguments.

    Changed in version 3.7: for IPv6 multicast addresses, string representing an address will not
    contain `%scope_id` part.