Freeze is a tool to create stand-alone applications. When freezing Tkinter
applications, the applications will not be truly stand-alone, as the application
will still need the Tcl and Tk libraries.

One solution is to ship the application with the Tcl and Tk libraries, and point
to them at run-time using the `TCL_LIBRARY` and `TK_LIBRARY`
environment variables.

Various third-party freeze libraries such as py2exe and cx\_Freeze have
handling for Tkinter applications built-in.

On platforms other than Windows, yes, and you don’t even
need threads! But you’ll have to restructure your I/O
code a bit. Tk has the equivalent of Xt’s `XtAddInput()` call, which allows you
to register a callback function which will be called from the Tk mainloop when
I/O is possible on a file descriptor. See [File Handlers](../library/tkinter.html#tkinter-file-handlers).

An often-heard complaint is that event handlers [bound](../library/tkinter.html#bindings-and-events)
to events with the `bind()` method
don’t get handled even when the appropriate key is pressed.

The most common cause is that the widget to which the binding applies doesn’t
have “keyboard focus”. Check out the Tk documentation for the focus command.
Usually a widget is given the keyboard focus by clicking in it (but not for
labels; see the takefocus option).