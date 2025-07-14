`syslog` — Unix syslog library routines
=======================================

---

This module provides an interface to the Unix `syslog` library routines.
Refer to the Unix manual pages for a detailed description of the `syslog`
facility.

This module wraps the system `syslog` family of routines. A pure Python
library that can speak to a syslog server is available in the
[`logging.handlers`](logging.handlers.html#module-logging.handlers "logging.handlers: Handlers for the logging module.") module as [`SysLogHandler`](logging.handlers.html#logging.handlers.SysLogHandler "logging.handlers.SysLogHandler").

The module defines the following functions:

syslog.syslog(*message*)

syslog.syslog(*priority*, *message*)
:   Send the string *message* to the system logger. A trailing newline is added
    if necessary. Each message is tagged with a priority composed of a
    *facility* and a *level*. The optional *priority* argument, which defaults
    to [`LOG_INFO`](#syslog.LOG_INFO "syslog.LOG_INFO"), determines the message priority. If the facility is
    not encoded in *priority* using logical-or (`LOG_INFO | LOG_USER`), the
    value given in the [`openlog()`](#syslog.openlog "syslog.openlog") call is used.

    If [`openlog()`](#syslog.openlog "syslog.openlog") has not been called prior to the call to [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)"),
    [`openlog()`](#syslog.openlog "syslog.openlog") will be called with no arguments.

    Raises an [auditing event](sys.html#auditing) `syslog.syslog` with arguments `priority`, `message`.

    Changed in version 3.2: In previous versions, [`openlog()`](#syslog.openlog "syslog.openlog") would not be called automatically if
    it wasn’t called prior to the call to [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)"), deferring to the syslog
    implementation to call `openlog()`.

    Changed in version 3.12: This function is restricted in subinterpreters.
    (Only code that runs in multiple interpreters is affected and
    the restriction is not relevant for most users.)
    [`openlog()`](#syslog.openlog "syslog.openlog") must be called in the main interpreter before [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") may be used
    in a subinterpreter. Otherwise it will raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

syslog.openlog([*ident*[, *logoption*[, *facility*]]])
:   Logging options of subsequent [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") calls can be set by calling
    [`openlog()`](#syslog.openlog "syslog.openlog"). [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") will call [`openlog()`](#syslog.openlog "syslog.openlog") with no arguments
    if the log is not currently open.

    The optional *ident* keyword argument is a string which is prepended to every
    message, and defaults to `sys.argv[0]` with leading path components
    stripped. The optional *logoption* keyword argument (default is 0) is a bit
    field – see below for possible values to combine. The optional *facility*
    keyword argument (default is [`LOG_USER`](#syslog.LOG_USER "syslog.LOG_USER")) sets the default facility for
    messages which do not have a facility explicitly encoded.

    Raises an [auditing event](sys.html#auditing) `syslog.openlog` with arguments `ident`, `logoption`, `facility`.

    Changed in version 3.2: In previous versions, keyword arguments were not allowed, and *ident* was
    required.

    Changed in version 3.12: This function is restricted in subinterpreters.
    (Only code that runs in multiple interpreters is affected and
    the restriction is not relevant for most users.)
    This may only be called in the main interpreter.
    It will raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if called in a subinterpreter.

syslog.closelog()
:   Reset the syslog module values and call the system library `closelog()`.

    This causes the module to behave as it does when initially imported. For
    example, [`openlog()`](#syslog.openlog "syslog.openlog") will be called on the first [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") call (if
    [`openlog()`](#syslog.openlog "syslog.openlog") hasn’t already been called), and *ident* and other
    [`openlog()`](#syslog.openlog "syslog.openlog") parameters are reset to defaults.

    Raises an [auditing event](sys.html#auditing) `syslog.closelog` with no arguments.

    Changed in version 3.12: This function is restricted in subinterpreters.
    (Only code that runs in multiple interpreters is affected and
    the restriction is not relevant for most users.)
    This may only be called in the main interpreter.
    It will raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if called in a subinterpreter.

syslog.setlogmask(*maskpri*)
:   Set the priority mask to *maskpri* and return the previous mask value. Calls
    to [`syslog()`](#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") with a priority level not set in *maskpri* are ignored.
    The default is to log all priorities. The function `LOG_MASK(pri)`
    calculates the mask for the individual priority *pri*. The function
    `LOG_UPTO(pri)` calculates the mask for all priorities up to and including
    *pri*.

    Raises an [auditing event](sys.html#auditing) `syslog.setlogmask` with argument `maskpri`.

The module defines the following constants:

syslog.LOG\_EMERG

syslog.LOG\_ALERT

syslog.LOG\_CRIT

syslog.LOG\_ERR

syslog.LOG\_WARNING

syslog.LOG\_NOTICE

syslog.LOG\_INFO

syslog.LOG\_DEBUG
:   Priority levels (high to low).

syslog.LOG\_AUTH

syslog.LOG\_AUTHPRIV

syslog.LOG\_CRON

syslog.LOG\_DAEMON

syslog.LOG\_FTP

syslog.LOG\_INSTALL

syslog.LOG\_KERN

syslog.LOG\_LAUNCHD

syslog.LOG\_LPR

syslog.LOG\_MAIL

syslog.LOG\_NETINFO

syslog.LOG\_NEWS

syslog.LOG\_RAS

syslog.LOG\_REMOTEAUTH

syslog.LOG\_SYSLOG

syslog.LOG\_USER

syslog.LOG\_UUCP

syslog.LOG\_LOCAL0

syslog.LOG\_LOCAL1

syslog.LOG\_LOCAL2

syslog.LOG\_LOCAL3

syslog.LOG\_LOCAL4

syslog.LOG\_LOCAL5

syslog.LOG\_LOCAL6

syslog.LOG\_LOCAL7
:   Facilities, depending on availability in `<syslog.h>` for [`LOG_AUTHPRIV`](#syslog.LOG_AUTHPRIV "syslog.LOG_AUTHPRIV"),
    [`LOG_FTP`](#syslog.LOG_FTP "syslog.LOG_FTP"), [`LOG_NETINFO`](#syslog.LOG_NETINFO "syslog.LOG_NETINFO"), [`LOG_REMOTEAUTH`](#syslog.LOG_REMOTEAUTH "syslog.LOG_REMOTEAUTH"),
    [`LOG_INSTALL`](#syslog.LOG_INSTALL "syslog.LOG_INSTALL") and [`LOG_RAS`](#syslog.LOG_RAS "syslog.LOG_RAS").

syslog.LOG\_PID

syslog.LOG\_CONS

syslog.LOG\_NDELAY

syslog.LOG\_ODELAY

syslog.LOG\_NOWAIT

syslog.LOG\_PERROR
:   Log options, depending on availability in `<syslog.h>` for
    [`LOG_ODELAY`](#syslog.LOG_ODELAY "syslog.LOG_ODELAY"), [`LOG_NOWAIT`](#syslog.LOG_NOWAIT "syslog.LOG_NOWAIT") and [`LOG_PERROR`](#syslog.LOG_PERROR "syslog.LOG_PERROR").

Examples
--------

### Simple example

A simple set of examples:

Copy

```
import syslog

syslog.syslog('Processing started')
if error:
    syslog.syslog(syslog.LOG_ERR, 'Processing started')

```

An example of setting some log options, these would include the process ID in
logged messages, and write the messages to the destination facility used for
mail logging:

Copy

```
syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
syslog.syslog('E-mail processing initiated...')

```