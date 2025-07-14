`curses` — Terminal handling for character-cell displays
========================================================

**Source code:** [Lib/curses](https://github.com/python/cpython/tree/3.13/Lib/curses)

---

The [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") module provides an interface to the curses library, the
de-facto standard for portable advanced terminal handling.

While curses is most widely used in the Unix environment, versions are available
for Windows, DOS, and possibly other systems as well. This extension module is
designed to match the API of ncurses, an open-source curses library hosted on
Linux and the BSD variants of Unix.

Note

Whenever the documentation mentions a *character* it can be specified
as an integer, a one-character Unicode string or a one-byte byte string.

Whenever the documentation mentions a *character string* it can be specified
as a Unicode string or a byte string.

See also

Module [`curses.ascii`](curses.ascii.html#module-curses.ascii "curses.ascii: Constants and set-membership functions for ASCII characters.")
:   Utilities for working with ASCII characters, regardless of your locale settings.

Module [`curses.panel`](curses.panel.html#module-curses.panel "curses.panel: A panel stack extension that adds depth to curses windows.")
:   A panel stack extension that adds depth to curses windows.

Module [`curses.textpad`](#module-curses.textpad "curses.textpad: Emacs-like input editing in a curses window.")
:   Editable text widget for curses supporting **Emacs**-like bindings.

[Curses Programming with Python](../howto/curses.html#curses-howto)
:   Tutorial material on using curses with Python, by Andrew Kuchling and Eric
    Raymond.

Functions
---------

The module [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") defines the following exception:

*exception* curses.error
:   Exception raised when a curses library function returns an error.

Note

Whenever *x* or *y* arguments to a function or a method are optional, they
default to the current cursor location. Whenever *attr* is optional, it defaults
to [`A_NORMAL`](#curses.A_NORMAL "curses.A_NORMAL").

The module [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") defines the following functions:

curses.baudrate()
:   Return the output speed of the terminal in bits per second. On software
    terminal emulators it will have a fixed high value. Included for historical
    reasons; in former times, it was used to write output loops for time delays and
    occasionally to change interfaces depending on the line speed.

curses.beep()
:   Emit a short attention sound.

curses.can\_change\_color()
:   Return `True` or `False`, depending on whether the programmer can change the colors
    displayed by the terminal.

curses.cbreak()
:   Enter cbreak mode. In cbreak mode (sometimes called “rare” mode) normal tty
    line buffering is turned off and characters are available to be read one by one.
    However, unlike raw mode, special characters (interrupt, quit, suspend, and flow
    control) retain their effects on the tty driver and calling program. Calling
    first [`raw()`](#curses.raw "curses.raw") then [`cbreak()`](#curses.cbreak "curses.cbreak") leaves the terminal in cbreak mode.

curses.color\_content(*color\_number*)
:   Return the intensity of the red, green, and blue (RGB) components in the color
    *color\_number*, which must be between `0` and `COLORS - 1`. Return a 3-tuple,
    containing the R,G,B values for the given color, which will be between
    `0` (no component) and `1000` (maximum amount of component).

curses.color\_pair(*pair\_number*)
:   Return the attribute value for displaying text in the specified color pair.
    Only the first 256 color pairs are supported. This
    attribute value can be combined with [`A_STANDOUT`](#curses.A_STANDOUT "curses.A_STANDOUT"), [`A_REVERSE`](#curses.A_REVERSE "curses.A_REVERSE"),
    and the other `A_*` attributes. [`pair_number()`](#curses.pair_number "curses.pair_number") is the counterpart
    to this function.

curses.curs\_set(*visibility*)
:   Set the cursor state. *visibility* can be set to `0`, `1`, or `2`, for invisible,
    normal, or very visible. If the terminal supports the visibility requested, return the
    previous cursor state; otherwise raise an exception. On many
    terminals, the “visible” mode is an underline cursor and the “very visible” mode
    is a block cursor.

curses.def\_prog\_mode()
:   Save the current terminal mode as the “program” mode, the mode when the running
    program is using curses. (Its counterpart is the “shell” mode, for when the
    program is not in curses.) Subsequent calls to [`reset_prog_mode()`](#curses.reset_prog_mode "curses.reset_prog_mode") will
    restore this mode.

curses.def\_shell\_mode()
:   Save the current terminal mode as the “shell” mode, the mode when the running
    program is not using curses. (Its counterpart is the “program” mode, when the
    program is using curses capabilities.) Subsequent calls to
    [`reset_shell_mode()`](#curses.reset_shell_mode "curses.reset_shell_mode") will restore this mode.

curses.delay\_output(*ms*)
:   Insert an *ms* millisecond pause in output.

curses.doupdate()
:   Update the physical screen. The curses library keeps two data structures, one
    representing the current physical screen contents and a virtual screen
    representing the desired next state. The [`doupdate()`](#curses.doupdate "curses.doupdate") ground updates the
    physical screen to match the virtual screen.

    The virtual screen may be updated by a [`noutrefresh()`](#curses.window.noutrefresh "curses.window.noutrefresh") call after write
    operations such as [`addstr()`](#curses.window.addstr "curses.window.addstr") have been performed on a window. The normal
    [`refresh()`](#curses.window.refresh "curses.window.refresh") call is simply `noutrefresh()` followed by `doupdate()`;
    if you have to update multiple windows, you can speed performance and perhaps
    reduce screen flicker by issuing `noutrefresh()` calls on all windows,
    followed by a single `doupdate()`.

curses.echo()
:   Enter echo mode. In echo mode, each character input is echoed to the screen as
    it is entered.

curses.endwin()
:   De-initialize the library, and return terminal to normal status.

curses.erasechar()
:   Return the user’s current erase character as a one-byte bytes object. Under Unix operating systems this
    is a property of the controlling tty of the curses program, and is not set by
    the curses library itself.

curses.filter()
:   The [`filter()`](#curses.filter "curses.filter") routine, if used, must be called before [`initscr()`](#curses.initscr "curses.initscr") is
    called. The effect is that, during those calls, `LINES` is set to `1`; the
    capabilities `clear`, `cup`, `cud`, `cud1`, `cuu1`, `cuu`, `vpa` are disabled; and the `home`
    string is set to the value of `cr`. The effect is that the cursor is confined to
    the current line, and so are screen updates. This may be used for enabling
    character-at-a-time line editing without touching the rest of the screen.

curses.flash()
:   Flash the screen. That is, change it to reverse-video and then change it back
    in a short interval. Some people prefer such as ‘visible bell’ to the audible
    attention signal produced by [`beep()`](#curses.beep "curses.beep").

curses.flushinp()
:   Flush all input buffers. This throws away any typeahead that has been typed
    by the user and has not yet been processed by the program.

curses.getmouse()
:   After [`getch()`](#curses.window.getch "curses.window.getch") returns [`KEY_MOUSE`](#curses.KEY_MOUSE "curses.KEY_MOUSE") to signal a mouse event, this
    method should be called to retrieve the queued mouse event, represented as a
    5-tuple `(id, x, y, z, bstate)`. *id* is an ID value used to distinguish
    multiple devices, and *x*, *y*, *z* are the event’s coordinates. (*z* is
    currently unused.) *bstate* is an integer value whose bits will be set to
    indicate the type of event, and will be the bitwise OR of one or more of the
    following constants, where *n* is the button number from 1 to 5:
    [`BUTTONn_PRESSED`](#curses.BUTTONn_PRESSED "curses.BUTTONn_PRESSED"), [`BUTTONn_RELEASED`](#curses.BUTTONn_RELEASED "curses.BUTTONn_RELEASED"), [`BUTTONn_CLICKED`](#curses.BUTTONn_CLICKED "curses.BUTTONn_CLICKED"),
    [`BUTTONn_DOUBLE_CLICKED`](#curses.BUTTONn_DOUBLE_CLICKED "curses.BUTTONn_DOUBLE_CLICKED"), [`BUTTONn_TRIPLE_CLICKED`](#curses.BUTTONn_TRIPLE_CLICKED "curses.BUTTONn_TRIPLE_CLICKED"),
    [`BUTTON_SHIFT`](#curses.BUTTON_SHIFT "curses.BUTTON_SHIFT"), [`BUTTON_CTRL`](#curses.BUTTON_CTRL "curses.BUTTON_CTRL"), [`BUTTON_ALT`](#curses.BUTTON_ALT "curses.BUTTON_ALT").

    Changed in version 3.10: The `BUTTON5_*` constants are now exposed if they are provided by the
    underlying curses library.

curses.getsyx()
:   Return the current coordinates of the virtual screen cursor as a tuple
    `(y, x)`. If [`leaveok`](#curses.window.leaveok "curses.window.leaveok") is currently `True`, then return `(-1, -1)`.

curses.getwin(*file*)
:   Read window related data stored in the file by an earlier [`window.putwin()`](#curses.window.putwin "curses.window.putwin") call.
    The routine then creates and initializes a new window using that data, returning
    the new window object.

curses.has\_colors()
:   Return `True` if the terminal can display colors; otherwise, return `False`.

curses.has\_extended\_color\_support()
:   Return `True` if the module supports extended colors; otherwise, return
    `False`. Extended color support allows more than 256 color pairs for
    terminals that support more than 16 colors (e.g. xterm-256color).

    Extended color support requires ncurses version 6.1 or later.

curses.has\_ic()
:   Return `True` if the terminal has insert- and delete-character capabilities.
    This function is included for historical reasons only, as all modern software
    terminal emulators have such capabilities.

curses.has\_il()
:   Return `True` if the terminal has insert- and delete-line capabilities, or can
    simulate them using scrolling regions. This function is included for
    historical reasons only, as all modern software terminal emulators have such
    capabilities.

curses.has\_key(*ch*)
:   Take a key value *ch*, and return `True` if the current terminal type recognizes
    a key with that value.

curses.halfdelay(*tenths*)
:   Used for half-delay mode, which is similar to cbreak mode in that characters
    typed by the user are immediately available to the program. However, after
    blocking for *tenths* tenths of seconds, raise an exception if nothing has
    been typed. The value of *tenths* must be a number between `1` and `255`. Use
    [`nocbreak()`](#curses.nocbreak "curses.nocbreak") to leave half-delay mode.

curses.init\_color(*color\_number*, *r*, *g*, *b*)
:   Change the definition of a color, taking the number of the color to be changed
    followed by three RGB values (for the amounts of red, green, and blue
    components). The value of *color\_number* must be between `0` and
    `COLORS - 1`. Each of *r*, *g*, *b*, must be a value between `0` and
    `1000`. When [`init_color()`](#curses.init_color "curses.init_color") is used, all occurrences of that color on the
    screen immediately change to the new definition. This function is a no-op on
    most terminals; it is active only if [`can_change_color()`](#curses.can_change_color "curses.can_change_color") returns `True`.

curses.init\_pair(*pair\_number*, *fg*, *bg*)
:   Change the definition of a color-pair. It takes three arguments: the number of
    the color-pair to be changed, the foreground color number, and the background
    color number. The value of *pair\_number* must be between `1` and
    `COLOR_PAIRS - 1` (the `0` color pair is wired to white on black and cannot
    be changed). The value of *fg* and *bg* arguments must be between `0` and
    `COLORS - 1`, or, after calling [`use_default_colors()`](#curses.use_default_colors "curses.use_default_colors"), `-1`.
    If the color-pair was previously initialized, the screen is
    refreshed and all occurrences of that color-pair are changed to the new
    definition.

curses.initscr()
:   Initialize the library. Return a [window](#curses-window-objects) object
    which represents the whole screen.

    Note

    If there is an error opening the terminal, the underlying curses library may
    cause the interpreter to exit.

curses.is\_term\_resized(*nlines*, *ncols*)
:   Return `True` if [`resize_term()`](#curses.resize_term "curses.resize_term") would modify the window structure,
    `False` otherwise.

curses.isendwin()
:   Return `True` if [`endwin()`](#curses.endwin "curses.endwin") has been called (that is, the curses library has
    been deinitialized).

curses.keyname(*k*)
:   Return the name of the key numbered *k* as a bytes object. The name of a key generating printable
    ASCII character is the key’s character. The name of a control-key combination
    is a two-byte bytes object consisting of a caret (`b'^'`) followed by the corresponding
    printable ASCII character. The name of an alt-key combination (128–255) is a
    bytes object consisting of the prefix `b'M-'` followed by the name of the corresponding
    ASCII character.

curses.killchar()
:   Return the user’s current line kill character as a one-byte bytes object. Under Unix operating systems
    this is a property of the controlling tty of the curses program, and is not set
    by the curses library itself.

curses.longname()
:   Return a bytes object containing the terminfo long name field describing the current
    terminal. The maximum length of a verbose description is 128 characters. It is
    defined only after the call to [`initscr()`](#curses.initscr "curses.initscr").

curses.meta(*flag*)
:   If *flag* is `True`, allow 8-bit characters to be input. If
    *flag* is `False`, allow only 7-bit chars.

curses.mouseinterval(*interval*)
:   Set the maximum time in milliseconds that can elapse between press and release
    events in order for them to be recognized as a click, and return the previous
    interval value. The default value is 200 milliseconds, or one fifth of a second.

curses.mousemask(*mousemask*)
:   Set the mouse events to be reported, and return a tuple `(availmask,
    oldmask)`. *availmask* indicates which of the specified mouse events can be
    reported; on complete failure it returns `0`. *oldmask* is the previous value of
    the given window’s mouse event mask. If this function is never called, no mouse
    events are ever reported.

curses.napms(*ms*)
:   Sleep for *ms* milliseconds.

curses.newpad(*nlines*, *ncols*)
:   Create and return a pointer to a new pad data structure with the given number
    of lines and columns. Return a pad as a window object.

    A pad is like a window, except that it is not restricted by the screen size, and
    is not necessarily associated with a particular part of the screen. Pads can be
    used when a large window is needed, and only a part of the window will be on the
    screen at one time. Automatic refreshes of pads (such as from scrolling or
    echoing of input) do not occur. The [`refresh()`](#curses.window.refresh "curses.window.refresh") and [`noutrefresh()`](#curses.window.noutrefresh "curses.window.noutrefresh")
    methods of a pad require 6 arguments to specify the part of the pad to be
    displayed and the location on the screen to be used for the display. The
    arguments are *pminrow*, *pmincol*, *sminrow*, *smincol*, *smaxrow*, *smaxcol*; the *p*
    arguments refer to the upper left corner of the pad region to be displayed and
    the *s* arguments define a clipping box on the screen within which the pad region
    is to be displayed.

curses.newwin(*nlines*, *ncols*)

curses.newwin(*nlines*, *ncols*, *begin\_y*, *begin\_x*)
:   Return a new [window](#curses-window-objects), whose left-upper corner
    is at `(begin_y, begin_x)`, and whose height/width is *nlines*/*ncols*.

    By default, the window will extend from the specified position to the lower
    right corner of the screen.

curses.nl()
:   Enter newline mode. This mode translates the return key into newline on input,
    and translates newline into return and line-feed on output. Newline mode is
    initially on.

curses.nocbreak()
:   Leave cbreak mode. Return to normal “cooked” mode with line buffering.

curses.noecho()
:   Leave echo mode. Echoing of input characters is turned off.

curses.nonl()
:   Leave newline mode. Disable translation of return into newline on input, and
    disable low-level translation of newline into newline/return on output (but this
    does not change the behavior of `addch('\n')`, which always does the
    equivalent of return and line feed on the virtual screen). With translation
    off, curses can sometimes speed up vertical motion a little; also, it will be
    able to detect the return key on input.

curses.noqiflush()
:   When the `noqiflush()` routine is used, normal flush of input and output queues
    associated with the `INTR`, `QUIT` and `SUSP` characters will not be done. You may
    want to call `noqiflush()` in a signal handler if you want output to
    continue as though the interrupt had not occurred, after the handler exits.

curses.noraw()
:   Leave raw mode. Return to normal “cooked” mode with line buffering.

curses.pair\_content(*pair\_number*)
:   Return a tuple `(fg, bg)` containing the colors for the requested color pair.
    The value of *pair\_number* must be between `0` and `COLOR_PAIRS - 1`.

curses.pair\_number(*attr*)
:   Return the number of the color-pair set by the attribute value *attr*.
    [`color_pair()`](#curses.color_pair "curses.color_pair") is the counterpart to this function.

curses.putp(*str*)
:   Equivalent to `tputs(str, 1, putchar)`; emit the value of a specified
    terminfo capability for the current terminal. Note that the output of [`putp()`](#curses.putp "curses.putp")
    always goes to standard output.

curses.qiflush([*flag*])
:   If *flag* is `False`, the effect is the same as calling [`noqiflush()`](#curses.noqiflush "curses.noqiflush"). If
    *flag* is `True`, or no argument is provided, the queues will be flushed when
    these control characters are read.

curses.raw()
:   Enter raw mode. In raw mode, normal line buffering and processing of
    interrupt, quit, suspend, and flow control keys are turned off; characters are
    presented to curses input functions one by one.

curses.reset\_prog\_mode()
:   Restore the terminal to “program” mode, as previously saved by
    [`def_prog_mode()`](#curses.def_prog_mode "curses.def_prog_mode").

curses.reset\_shell\_mode()
:   Restore the terminal to “shell” mode, as previously saved by
    [`def_shell_mode()`](#curses.def_shell_mode "curses.def_shell_mode").

curses.resetty()
:   Restore the state of the terminal modes to what it was at the last call to
    [`savetty()`](#curses.savetty "curses.savetty").

curses.resize\_term(*nlines*, *ncols*)
:   Backend function used by [`resizeterm()`](#curses.resizeterm "curses.resizeterm"), performing most of the work;
    when resizing the windows, [`resize_term()`](#curses.resize_term "curses.resize_term") blank-fills the areas that are
    extended. The calling application should fill in these areas with
    appropriate data. The `resize_term()` function attempts to resize all
    windows. However, due to the calling convention of pads, it is not possible
    to resize these without additional interaction with the application.

curses.resizeterm(*nlines*, *ncols*)
:   Resize the standard and current windows to the specified dimensions, and
    adjusts other bookkeeping data used by the curses library that record the
    window dimensions (in particular the SIGWINCH handler).

curses.savetty()
:   Save the current state of the terminal modes in a buffer, usable by
    [`resetty()`](#curses.resetty "curses.resetty").

curses.get\_escdelay()
:   Retrieves the value set by [`set_escdelay()`](#curses.set_escdelay "curses.set_escdelay").

curses.set\_escdelay(*ms*)
:   Sets the number of milliseconds to wait after reading an escape character,
    to distinguish between an individual escape character entered on the
    keyboard from escape sequences sent by cursor and function keys.

curses.get\_tabsize()
:   Retrieves the value set by [`set_tabsize()`](#curses.set_tabsize "curses.set_tabsize").

curses.set\_tabsize(*size*)
:   Sets the number of columns used by the curses library when converting a tab
    character to spaces as it adds the tab to a window.

curses.setsyx(*y*, *x*)
:   Set the virtual screen cursor to *y*, *x*. If *y* and *x* are both `-1`, then
    [`leaveok`](#curses.window.leaveok "curses.window.leaveok") is set `True`.

curses.setupterm(*term=None*, *fd=-1*)
:   Initialize the terminal. *term* is a string giving
    the terminal name, or `None`; if omitted or `None`, the value of the
    `TERM` environment variable will be used. *fd* is the
    file descriptor to which any initialization sequences will be sent; if not
    supplied or `-1`, the file descriptor for `sys.stdout` will be used.

curses.start\_color()
:   Must be called if the programmer wants to use colors, and before any other color
    manipulation routine is called. It is good practice to call this routine right
    after [`initscr()`](#curses.initscr "curses.initscr").

    [`start_color()`](#curses.start_color "curses.start_color") initializes eight basic colors (black, red, green, yellow,
    blue, magenta, cyan, and white), and two global variables in the [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)")
    module, [`COLORS`](#curses.COLORS "curses.COLORS") and [`COLOR_PAIRS`](#curses.COLOR_PAIRS "curses.COLOR_PAIRS"), containing the maximum number
    of colors and color-pairs the terminal can support. It also restores the colors
    on the terminal to the values they had when the terminal was just turned on.

curses.termattrs()
:   Return a logical OR of all video attributes supported by the terminal. This
    information is useful when a curses program needs complete control over the
    appearance of the screen.

curses.termname()
:   Return the value of the environment variable `TERM`, as a bytes object,
    truncated to 14 characters.

curses.tigetflag(*capname*)
:   Return the value of the Boolean capability corresponding to the terminfo
    capability name *capname* as an integer. Return the value `-1` if *capname* is not a
    Boolean capability, or `0` if it is canceled or absent from the terminal
    description.

curses.tigetnum(*capname*)
:   Return the value of the numeric capability corresponding to the terminfo
    capability name *capname* as an integer. Return the value `-2` if *capname* is not a
    numeric capability, or `-1` if it is canceled or absent from the terminal
    description.

curses.tigetstr(*capname*)
:   Return the value of the string capability corresponding to the terminfo
    capability name *capname* as a bytes object. Return `None` if *capname*
    is not a terminfo “string capability”, or is canceled or absent from the
    terminal description.

curses.tparm(*str*[, *...*])
:   Instantiate the bytes object *str* with the supplied parameters, where *str* should
    be a parameterized string obtained from the terminfo database. E.g.
    `tparm(tigetstr("cup"), 5, 3)` could result in `b'\033[6;4H'`, the exact
    result depending on terminal type.

curses.typeahead(*fd*)
:   Specify that the file descriptor *fd* be used for typeahead checking. If *fd*
    is `-1`, then no typeahead checking is done.

    The curses library does “line-breakout optimization” by looking for typeahead
    periodically while updating the screen. If input is found, and it is coming
    from a tty, the current update is postponed until refresh or doupdate is called
    again, allowing faster response to commands typed in advance. This function
    allows specifying a different file descriptor for typeahead checking.

curses.unctrl(*ch*)
:   Return a bytes object which is a printable representation of the character *ch*.
    Control characters are represented as a caret followed by the character, for
    example as `b'^C'`. Printing characters are left as they are.

curses.ungetch(*ch*)
:   Push *ch* so the next [`getch()`](#curses.window.getch "curses.window.getch") will return it.

    Note

    Only one *ch* can be pushed before `getch()` is called.

curses.update\_lines\_cols()
:   Update the [`LINES`](#curses.LINES "curses.LINES") and [`COLS`](#curses.COLS "curses.COLS") module variables.
    Useful for detecting manual screen resize.

curses.unget\_wch(*ch*)
:   Push *ch* so the next [`get_wch()`](#curses.window.get_wch "curses.window.get_wch") will return it.

    Note

    Only one *ch* can be pushed before `get_wch()` is called.

curses.ungetmouse(*id*, *x*, *y*, *z*, *bstate*)
:   Push a [`KEY_MOUSE`](#curses.KEY_MOUSE "curses.KEY_MOUSE") event onto the input queue, associating the given
    state data with it.

curses.use\_env(*flag*)
:   If used, this function should be called before [`initscr()`](#curses.initscr "curses.initscr") or newterm are
    called. When *flag* is `False`, the values of lines and columns specified in the
    terminfo database will be used, even if environment variables `LINES`
    and `COLUMNS` (used by default) are set, or if curses is running in a
    window (in which case default behavior would be to use the window size if
    `LINES` and `COLUMNS` are not set).

curses.use\_default\_colors()
:   Allow use of default values for colors on terminals supporting this feature. Use
    this to support transparency in your application. The default color is assigned
    to the color number `-1`. After calling this function, `init_pair(x,
    curses.COLOR_RED, -1)` initializes, for instance, color pair *x* to a red
    foreground color on the default background.

curses.wrapper(*func*, */*, *\*args*, *\*\*kwargs*)
:   Initialize curses and call another callable object, *func*, which should be the
    rest of your curses-using application. If the application raises an exception,
    this function will restore the terminal to a sane state before re-raising the
    exception and generating a traceback. The callable object *func* is then passed
    the main window ‘stdscr’ as its first argument, followed by any other arguments
    passed to `wrapper()`. Before calling *func*, `wrapper()` turns on
    cbreak mode, turns off echo, enables the terminal keypad, and initializes colors
    if the terminal has color support. On exit (whether normally or by exception)
    it restores cooked mode, turns on echo, and disables the terminal keypad.

Window Objects
--------------

Window objects, as returned by [`initscr()`](#curses.initscr "curses.initscr") and [`newwin()`](#curses.newwin "curses.newwin") above, have
the following methods and attributes:

window.addch(*ch*[, *attr*])

window.addch(*y*, *x*, *ch*[, *attr*])
:   Paint character *ch* at `(y, x)` with attributes *attr*, overwriting any
    character previously painted at that location. By default, the character
    position and attributes are the current settings for the window object.

    Note

    Writing outside the window, subwindow, or pad raises a [`curses.error`](#curses.error "curses.error").
    Attempting to write to the lower right corner of a window, subwindow,
    or pad will cause an exception to be raised after the character is printed.

window.addnstr(*str*, *n*[, *attr*])

window.addnstr(*y*, *x*, *str*, *n*[, *attr*])
:   Paint at most *n* characters of the character string *str* at
    `(y, x)` with attributes
    *attr*, overwriting anything previously on the display.

window.addstr(*str*[, *attr*])

window.addstr(*y*, *x*, *str*[, *attr*])
:   Paint the character string *str* at `(y, x)` with attributes
    *attr*, overwriting anything previously on the display.

    Note

    * Writing outside the window, subwindow, or pad raises [`curses.error`](#curses.error "curses.error").
      Attempting to write to the lower right corner of a window, subwindow,
      or pad will cause an exception to be raised after the string is printed.
    * A [bug in ncurses](https://bugs.python.org/issue35924), the backend
      for this Python module, can cause SegFaults when resizing windows. This
      is fixed in ncurses-6.1-20190511. If you are stuck with an earlier
      ncurses, you can avoid triggering this if you do not call [`addstr()`](#curses.window.addstr "curses.window.addstr")
      with a *str* that has embedded newlines. Instead, call [`addstr()`](#curses.window.addstr "curses.window.addstr")
      separately for each line.

window.attroff(*attr*)
:   Remove attribute *attr* from the “background” set applied to all writes to the
    current window.

window.attron(*attr*)
:   Add attribute *attr* from the “background” set applied to all writes to the
    current window.

window.attrset(*attr*)
:   Set the “background” set of attributes to *attr*. This set is initially
    `0` (no attributes).

window.bkgd(*ch*[, *attr*])
:   Set the background property of the window to the character *ch*, with
    attributes *attr*. The change is then applied to every character position in
    that window:

    * The attribute of every character in the window is changed to the new
      background attribute.
    * Wherever the former background character appears, it is changed to the new
      background character.

window.bkgdset(*ch*[, *attr*])
:   Set the window’s background. A window’s background consists of a character and
    any combination of attributes. The attribute part of the background is combined
    (OR’ed) with all non-blank characters that are written into the window. Both
    the character and attribute parts of the background are combined with the blank
    characters. The background becomes a property of the character and moves with
    the character through any scrolling and insert/delete line/character operations.

window.border([*ls*[, *rs*[, *ts*[, *bs*[, *tl*[, *tr*[, *bl*[, *br*]]]]]]]])
:   Draw a border around the edges of the window. Each parameter specifies the
    character to use for a specific part of the border; see the table below for more
    details.

    Note

    A `0` value for any parameter will cause the default character to be used for
    that parameter. Keyword parameters can *not* be used. The defaults are listed
    in this table:

window.box([*vertch*, *horch*])
:   Similar to [`border()`](#curses.window.border "curses.window.border"), but both *ls* and *rs* are *vertch* and both *ts* and
    *bs* are *horch*. The default corner characters are always used by this function.

window.chgat(*attr*)

window.chgat(*num*, *attr*)

window.chgat(*y*, *x*, *attr*)

window.chgat(*y*, *x*, *num*, *attr*)
:   Set the attributes of *num* characters at the current cursor position, or at
    position `(y, x)` if supplied. If *num* is not given or is `-1`,
    the attribute will be set on all the characters to the end of the line. This
    function moves cursor to position `(y, x)` if supplied. The changed line
    will be touched using the [`touchline()`](#curses.window.touchline "curses.window.touchline") method so that the contents will
    be redisplayed by the next window refresh.

window.clear()
:   Like [`erase()`](#curses.window.erase "curses.window.erase"), but also cause the whole window to be repainted upon next
    call to [`refresh()`](#curses.window.refresh "curses.window.refresh").

window.clearok(*flag*)
:   If *flag* is `True`, the next call to [`refresh()`](#curses.window.refresh "curses.window.refresh") will clear the window
    completely.

window.clrtobot()
:   Erase from cursor to the end of the window: all lines below the cursor are
    deleted, and then the equivalent of [`clrtoeol()`](#curses.window.clrtoeol "curses.window.clrtoeol") is performed.

window.clrtoeol()
:   Erase from cursor to the end of the line.

window.cursyncup()
:   Update the current cursor position of all the ancestors of the window to
    reflect the current cursor position of the window.

window.delch([*y*, *x*])
:   Delete any character at `(y, x)`.

window.deleteln()
:   Delete the line under the cursor. All following lines are moved up by one line.

window.derwin(*begin\_y*, *begin\_x*)

window.derwin(*nlines*, *ncols*, *begin\_y*, *begin\_x*)
:   An abbreviation for “derive window”, [`derwin()`](#curses.window.derwin "curses.window.derwin") is the same as calling
    [`subwin()`](#curses.window.subwin "curses.window.subwin"), except that *begin\_y* and *begin\_x* are relative to the origin
    of the window, rather than relative to the entire screen. Return a window
    object for the derived window.

window.echochar(*ch*[, *attr*])
:   Add character *ch* with attribute *attr*, and immediately call [`refresh()`](#curses.window.refresh "curses.window.refresh")
    on the window.

window.enclose(*y*, *x*)
:   Test whether the given pair of screen-relative character-cell coordinates are
    enclosed by the given window, returning `True` or `False`. It is useful for
    determining what subset of the screen windows enclose the location of a mouse
    event.

    Changed in version 3.10: Previously it returned `1` or `0` instead of `True` or `False`.

window.encoding
:   Encoding used to encode method arguments (Unicode strings and characters).
    The encoding attribute is inherited from the parent window when a subwindow
    is created, for example with [`window.subwin()`](#curses.window.subwin "curses.window.subwin").
    By default, current locale encoding is used (see [`locale.getencoding()`](locale.html#locale.getencoding "locale.getencoding")).

window.erase()
:   Clear the window.

window.getbegyx()
:   Return a tuple `(y, x)` of coordinates of upper-left corner.

window.getbkgd()
:   Return the given window’s current background character/attribute pair.

window.getch([*y*, *x*])
:   Get a character. Note that the integer returned does *not* have to be in ASCII
    range: function keys, keypad keys and so on are represented by numbers higher
    than 255. In no-delay mode, return `-1` if there is no input, otherwise
    wait until a key is pressed.

window.get\_wch([*y*, *x*])
:   Get a wide character. Return a character for most keys, or an integer for
    function keys, keypad keys, and other special keys.
    In no-delay mode, raise an exception if there is no input.

window.getkey([*y*, *x*])
:   Get a character, returning a string instead of an integer, as [`getch()`](#curses.window.getch "curses.window.getch")
    does. Function keys, keypad keys and other special keys return a multibyte
    string containing the key name. In no-delay mode, raise an exception if
    there is no input.

window.getmaxyx()
:   Return a tuple `(y, x)` of the height and width of the window.

window.getparyx()
:   Return the beginning coordinates of this window relative to its parent window
    as a tuple `(y, x)`. Return `(-1, -1)` if this window has no
    parent.

window.getstr()

window.getstr(*n*)

window.getstr(*y*, *x*)

window.getstr(*y*, *x*, *n*)
:   Read a bytes object from the user, with primitive line editing capacity.

window.getyx()
:   Return a tuple `(y, x)` of current cursor position relative to the window’s
    upper-left corner.

window.hline(*ch*, *n*)

window.hline(*y*, *x*, *ch*, *n*)
:   Display a horizontal line starting at `(y, x)` with length *n* consisting of
    the character *ch*.

window.idcok(*flag*)
:   If *flag* is `False`, curses no longer considers using the hardware insert/delete
    character feature of the terminal; if *flag* is `True`, use of character insertion
    and deletion is enabled. When curses is first initialized, use of character
    insert/delete is enabled by default.

window.idlok(*flag*)
:   If *flag* is `True`, [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") will try and use hardware line
    editing facilities. Otherwise, line insertion/deletion are disabled.

window.immedok(*flag*)
:   If *flag* is `True`, any change in the window image automatically causes the
    window to be refreshed; you no longer have to call [`refresh()`](#curses.window.refresh "curses.window.refresh") yourself.
    However, it may degrade performance considerably, due to repeated calls to
    wrefresh. This option is disabled by default.

window.inch([*y*, *x*])
:   Return the character at the given position in the window. The bottom 8 bits are
    the character proper, and upper bits are the attributes.

window.insch(*ch*[, *attr*])

window.insch(*y*, *x*, *ch*[, *attr*])
:   Paint character *ch* at `(y, x)` with attributes *attr*, moving the line from
    position *x* right by one character.

window.insdelln(*nlines*)
:   Insert *nlines* lines into the specified window above the current line. The
    *nlines* bottom lines are lost. For negative *nlines*, delete *nlines* lines
    starting with the one under the cursor, and move the remaining lines up. The
    bottom *nlines* lines are cleared. The current cursor position remains the
    same.

window.insertln()
:   Insert a blank line under the cursor. All following lines are moved down by one
    line.

window.insnstr(*str*, *n*[, *attr*])

window.insnstr(*y*, *x*, *str*, *n*[, *attr*])
:   Insert a character string (as many characters as will fit on the line) before
    the character under the cursor, up to *n* characters. If *n* is zero or
    negative, the entire string is inserted. All characters to the right of the
    cursor are shifted right, with the rightmost characters on the line being lost.
    The cursor position does not change (after moving to *y*, *x*, if specified).

window.insstr(*str*[, *attr*])

window.insstr(*y*, *x*, *str*[, *attr*])
:   Insert a character string (as many characters as will fit on the line) before
    the character under the cursor. All characters to the right of the cursor are
    shifted right, with the rightmost characters on the line being lost. The cursor
    position does not change (after moving to *y*, *x*, if specified).

window.instr([*n*])

window.instr(*y*, *x*[, *n*])
:   Return a bytes object of characters, extracted from the window starting at the
    current cursor position, or at *y*, *x* if specified. Attributes are stripped
    from the characters. If *n* is specified, [`instr()`](#curses.window.instr "curses.window.instr") returns a string
    at most *n* characters long (exclusive of the trailing NUL).

window.is\_linetouched(*line*)
:   Return `True` if the specified line was modified since the last call to
    [`refresh()`](#curses.window.refresh "curses.window.refresh"); otherwise return `False`. Raise a [`curses.error`](#curses.error "curses.error")
    exception if *line* is not valid for the given window.

window.is\_wintouched()
:   Return `True` if the specified window was modified since the last call to
    [`refresh()`](#curses.window.refresh "curses.window.refresh"); otherwise return `False`.

window.keypad(*flag*)
:   If *flag* is `True`, escape sequences generated by some keys (keypad, function keys)
    will be interpreted by [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)"). If *flag* is `False`, escape sequences will be
    left as is in the input stream.

window.leaveok(*flag*)
:   If *flag* is `True`, cursor is left where it is on update, instead of being at “cursor
    position.” This reduces cursor movement where possible. If possible the cursor
    will be made invisible.

    If *flag* is `False`, cursor will always be at “cursor position” after an update.

window.move(*new\_y*, *new\_x*)
:   Move cursor to `(new_y, new_x)`.

window.mvderwin(*y*, *x*)
:   Move the window inside its parent window. The screen-relative parameters of
    the window are not changed. This routine is used to display different parts of
    the parent window at the same physical position on the screen.

window.mvwin(*new\_y*, *new\_x*)
:   Move the window so its upper-left corner is at `(new_y, new_x)`.

window.nodelay(*flag*)
:   If *flag* is `True`, [`getch()`](#curses.window.getch "curses.window.getch") will be non-blocking.

window.notimeout(*flag*)
:   If *flag* is `True`, escape sequences will not be timed out.

    If *flag* is `False`, after a few milliseconds, an escape sequence will not be
    interpreted, and will be left in the input stream as is.

window.noutrefresh()
:   Mark for refresh but wait. This function updates the data structure
    representing the desired state of the window, but does not force an update of
    the physical screen. To accomplish that, call [`doupdate()`](#curses.doupdate "curses.doupdate").

window.overlay(*destwin*[, *sminrow*, *smincol*, *dminrow*, *dmincol*, *dmaxrow*, *dmaxcol*])
:   Overlay the window on top of *destwin*. The windows need not be the same size,
    only the overlapping region is copied. This copy is non-destructive, which means
    that the current background character does not overwrite the old contents of
    *destwin*.

    To get fine-grained control over the copied region, the second form of
    [`overlay()`](#curses.window.overlay "curses.window.overlay") can be used. *sminrow* and *smincol* are the upper-left
    coordinates of the source window, and the other variables mark a rectangle in
    the destination window.

window.overwrite(*destwin*[, *sminrow*, *smincol*, *dminrow*, *dmincol*, *dmaxrow*, *dmaxcol*])
:   Overwrite the window on top of *destwin*. The windows need not be the same size,
    in which case only the overlapping region is copied. This copy is destructive,
    which means that the current background character overwrites the old contents of
    *destwin*.

    To get fine-grained control over the copied region, the second form of
    [`overwrite()`](#curses.window.overwrite "curses.window.overwrite") can be used. *sminrow* and *smincol* are the upper-left
    coordinates of the source window, the other variables mark a rectangle in the
    destination window.

window.putwin(*file*)
:   Write all data associated with the window into the provided file object. This
    information can be later retrieved using the [`getwin()`](#curses.getwin "curses.getwin") function.

window.redrawln(*beg*, *num*)
:   Indicate that the *num* screen lines, starting at line *beg*, are corrupted and
    should be completely redrawn on the next [`refresh()`](#curses.window.refresh "curses.window.refresh") call.

window.redrawwin()
:   Touch the entire window, causing it to be completely redrawn on the next
    [`refresh()`](#curses.window.refresh "curses.window.refresh") call.

window.refresh([*pminrow*, *pmincol*, *sminrow*, *smincol*, *smaxrow*, *smaxcol*])
:   Update the display immediately (sync actual screen with previous
    drawing/deleting methods).

    The 6 optional arguments can only be specified when the window is a pad created
    with [`newpad()`](#curses.newpad "curses.newpad"). The additional parameters are needed to indicate what part
    of the pad and screen are involved. *pminrow* and *pmincol* specify the upper
    left-hand corner of the rectangle to be displayed in the pad. *sminrow*,
    *smincol*, *smaxrow*, and *smaxcol* specify the edges of the rectangle to be
    displayed on the screen. The lower right-hand corner of the rectangle to be
    displayed in the pad is calculated from the screen coordinates, since the
    rectangles must be the same size. Both rectangles must be entirely contained
    within their respective structures. Negative values of *pminrow*, *pmincol*,
    *sminrow*, or *smincol* are treated as if they were zero.

window.resize(*nlines*, *ncols*)
:   Reallocate storage for a curses window to adjust its dimensions to the
    specified values. If either dimension is larger than the current values, the
    window’s data is filled with blanks that have the current background
    rendition (as set by [`bkgdset()`](#curses.window.bkgdset "curses.window.bkgdset")) merged into them.

window.scroll([*lines=1*])
:   Scroll the screen or scrolling region upward by *lines* lines.

window.scrollok(*flag*)
:   Control what happens when the cursor of a window is moved off the edge of the
    window or scrolling region, either as a result of a newline action on the bottom
    line, or typing the last character of the last line. If *flag* is `False`, the
    cursor is left on the bottom line. If *flag* is `True`, the window is scrolled up
    one line. Note that in order to get the physical scrolling effect on the
    terminal, it is also necessary to call [`idlok()`](#curses.window.idlok "curses.window.idlok").

window.setscrreg(*top*, *bottom*)
:   Set the scrolling region from line *top* to line *bottom*. All scrolling actions
    will take place in this region.

window.standend()
:   Turn off the standout attribute. On some terminals this has the side effect of
    turning off all attributes.

window.standout()
:   Turn on attribute *A\_STANDOUT*.

window.subpad(*begin\_y*, *begin\_x*)

window.subpad(*nlines*, *ncols*, *begin\_y*, *begin\_x*)
:   Return a sub-window, whose upper-left corner is at `(begin_y, begin_x)`, and
    whose width/height is *ncols*/*nlines*.

window.subwin(*begin\_y*, *begin\_x*)

window.subwin(*nlines*, *ncols*, *begin\_y*, *begin\_x*)
:   Return a sub-window, whose upper-left corner is at `(begin_y, begin_x)`, and
    whose width/height is *ncols*/*nlines*.

    By default, the sub-window will extend from the specified position to the lower
    right corner of the window.

window.syncdown()
:   Touch each location in the window that has been touched in any of its ancestor
    windows. This routine is called by [`refresh()`](#curses.window.refresh "curses.window.refresh"), so it should almost never
    be necessary to call it manually.

window.syncok(*flag*)
:   If *flag* is `True`, then [`syncup()`](#curses.window.syncup "curses.window.syncup") is called automatically
    whenever there is a change in the window.

window.syncup()
:   Touch all locations in ancestors of the window that have been changed in the
    window.

window.timeout(*delay*)
:   Set blocking or non-blocking read behavior for the window. If *delay* is
    negative, blocking read is used (which will wait indefinitely for input). If
    *delay* is zero, then non-blocking read is used, and [`getch()`](#curses.window.getch "curses.window.getch") will
    return `-1` if no input is waiting. If *delay* is positive, then
    [`getch()`](#curses.window.getch "curses.window.getch") will block for *delay* milliseconds, and return `-1` if there is
    still no input at the end of that time.

window.touchline(*start*, *count*[, *changed*])
:   Pretend *count* lines have been changed, starting with line *start*. If
    *changed* is supplied, it specifies whether the affected lines are marked as
    having been changed (*changed*`=True`) or unchanged (*changed*`=False`).

window.touchwin()
:   Pretend the whole window has been changed, for purposes of drawing
    optimizations.

window.untouchwin()
:   Mark all lines in the window as unchanged since the last call to
    [`refresh()`](#curses.window.refresh "curses.window.refresh").

window.vline(*ch*, *n*[, *attr*])

window.vline(*y*, *x*, *ch*, *n*[, *attr*])
:   Display a vertical line starting at `(y, x)` with length *n* consisting of the
    character *ch* with attributes *attr*.

Constants
---------

The [`curses`](#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") module defines the following data members:

curses.ERR
:   Some curses routines that return an integer, such as [`getch()`](#curses.window.getch "curses.window.getch"), return
    [`ERR`](#curses.ERR "curses.ERR") upon failure.

curses.OK
:   Some curses routines that return an integer, such as [`napms()`](#curses.napms "curses.napms"), return
    [`OK`](#curses.OK "curses.OK") upon success.

curses.version

curses.\_\_version\_\_
:   A bytes object representing the current version of the module.

curses.ncurses\_version
:   A named tuple containing the three components of the ncurses library
    version: *major*, *minor*, and *patch*. All values are integers. The
    components can also be accessed by name, so `curses.ncurses_version[0]`
    is equivalent to `curses.ncurses_version.major` and so on.

    Availability: if the ncurses library is used.

curses.COLORS
:   The maximum number of colors the terminal can support.
    It is defined only after the call to [`start_color()`](#curses.start_color "curses.start_color").

curses.COLOR\_PAIRS
:   The maximum number of color pairs the terminal can support.
    It is defined only after the call to [`start_color()`](#curses.start_color "curses.start_color").

curses.COLS
:   The width of the screen, i.e., the number of columns.
    It is defined only after the call to [`initscr()`](#curses.initscr "curses.initscr").
    Updated by [`update_lines_cols()`](#curses.update_lines_cols "curses.update_lines_cols"), [`resizeterm()`](#curses.resizeterm "curses.resizeterm") and
    [`resize_term()`](#curses.resize_term "curses.resize_term").

curses.LINES
:   The height of the screen, i.e., the number of lines.
    It is defined only after the call to [`initscr()`](#curses.initscr "curses.initscr").
    Updated by [`update_lines_cols()`](#curses.update_lines_cols "curses.update_lines_cols"), [`resizeterm()`](#curses.resizeterm "curses.resizeterm") and
    [`resize_term()`](#curses.resize_term "curses.resize_term").

Some constants are available to specify character cell attributes.
The exact constants available are system dependent.

| Attribute | Meaning |
| --- | --- |
| curses.A\_ALTCHARSET | Alternate character set mode |
| curses.A\_BLINK | Blink mode |
| curses.A\_BOLD | Bold mode |
| curses.A\_DIM | Dim mode |
| curses.A\_INVIS | Invisible or blank mode |
| curses.A\_ITALIC | Italic mode |
| curses.A\_NORMAL | Normal attribute |
| curses.A\_PROTECT | Protected mode |
| curses.A\_REVERSE | Reverse background and foreground colors |
| curses.A\_STANDOUT | Standout mode |
| curses.A\_UNDERLINE | Underline mode |
| curses.A\_HORIZONTAL | Horizontal highlight |
| curses.A\_LEFT | Left highlight |
| curses.A\_LOW | Low highlight |
| curses.A\_RIGHT | Right highlight |
| curses.A\_TOP | Top highlight |
| curses.A\_VERTICAL | Vertical highlight |

Added in version 3.7: `A_ITALIC` was added.

Several constants are available to extract corresponding attributes returned
by some methods.

| Bit-mask | Meaning |
| --- | --- |
| curses.A\_ATTRIBUTES | Bit-mask to extract attributes |
| curses.A\_CHARTEXT | Bit-mask to extract a character |
| curses.A\_COLOR | Bit-mask to extract color-pair field information |

Keys are referred to by integer constants with names starting with `KEY_`.
The exact keycaps available are system dependent.

| Key constant | Key |
| --- | --- |
| curses.KEY\_MIN | Minimum key value |
| curses.KEY\_BREAK | Break key (unreliable) |
| curses.KEY\_DOWN | Down-arrow |
| curses.KEY\_UP | Up-arrow |
| curses.KEY\_LEFT | Left-arrow |
| curses.KEY\_RIGHT | Right-arrow |
| curses.KEY\_HOME | Home key (upward+left arrow) |
| curses.KEY\_BACKSPACE | Backspace (unreliable) |
| curses.KEY\_F0 | Function keys. Up to 64 function keys are supported. |
| curses.KEY\_Fn | Value of function key *n* |
| curses.KEY\_DL | Delete line |
| curses.KEY\_IL | Insert line |
| curses.KEY\_DC | Delete character |
| curses.KEY\_IC | Insert char or enter insert mode |
| curses.KEY\_EIC | Exit insert char mode |
| curses.KEY\_CLEAR | Clear screen |
| curses.KEY\_EOS | Clear to end of screen |
| curses.KEY\_EOL | Clear to end of line |
| curses.KEY\_SF | Scroll 1 line forward |
| curses.KEY\_SR | Scroll 1 line backward (reverse) |
| curses.KEY\_NPAGE | Next page |
| curses.KEY\_PPAGE | Previous page |
| curses.KEY\_STAB | Set tab |
| curses.KEY\_CTAB | Clear tab |
| curses.KEY\_CATAB | Clear all tabs |
| curses.KEY\_ENTER | Enter or send (unreliable) |
| curses.KEY\_SRESET | Soft (partial) reset (unreliable) |
| curses.KEY\_RESET | Reset or hard reset (unreliable) |
| curses.KEY\_PRINT | Print |
| curses.KEY\_LL | Home down or bottom (lower left) |
| curses.KEY\_A1 | Upper left of keypad |
| curses.KEY\_A3 | Upper right of keypad |
| curses.KEY\_B2 | Center of keypad |
| curses.KEY\_C1 | Lower left of keypad |
| curses.KEY\_C3 | Lower right of keypad |
| curses.KEY\_BTAB | Back tab |
| curses.KEY\_BEG | Beg (beginning) |
| curses.KEY\_CANCEL | Cancel |
| curses.KEY\_CLOSE | Close |
| curses.KEY\_COMMAND | Cmd (command) |
| curses.KEY\_COPY | Copy |
| curses.KEY\_CREATE | Create |
| curses.KEY\_END | End |
| curses.KEY\_EXIT | Exit |
| curses.KEY\_FIND | Find |
| curses.KEY\_HELP | Help |
| curses.KEY\_MARK | Mark |
| curses.KEY\_MESSAGE | Message |
| curses.KEY\_MOVE | Move |
| curses.KEY\_NEXT | Next |
| curses.KEY\_OPEN | Open |
| curses.KEY\_OPTIONS | Options |
| curses.KEY\_PREVIOUS | Prev (previous) |
| curses.KEY\_REDO | Redo |
| curses.KEY\_REFERENCE | Ref (reference) |
| curses.KEY\_REFRESH | Refresh |
| curses.KEY\_REPLACE | Replace |
| curses.KEY\_RESTART | Restart |
| curses.KEY\_RESUME | Resume |
| curses.KEY\_SAVE | Save |
| curses.KEY\_SBEG | Shifted Beg (beginning) |
| curses.KEY\_SCANCEL | Shifted Cancel |
| curses.KEY\_SCOMMAND | Shifted Command |
| curses.KEY\_SCOPY | Shifted Copy |
| curses.KEY\_SCREATE | Shifted Create |
| curses.KEY\_SDC | Shifted Delete char |
| curses.KEY\_SDL | Shifted Delete line |
| curses.KEY\_SELECT | Select |
| curses.KEY\_SEND | Shifted End |
| curses.KEY\_SEOL | Shifted Clear line |
| curses.KEY\_SEXIT | Shifted Exit |
| curses.KEY\_SFIND | Shifted Find |
| curses.KEY\_SHELP | Shifted Help |
| curses.KEY\_SHOME | Shifted Home |
| curses.KEY\_SIC | Shifted Input |
| curses.KEY\_SLEFT | Shifted Left arrow |
| curses.KEY\_SMESSAGE | Shifted Message |
| curses.KEY\_SMOVE | Shifted Move |
| curses.KEY\_SNEXT | Shifted Next |
| curses.KEY\_SOPTIONS | Shifted Options |
| curses.KEY\_SPREVIOUS | Shifted Prev |
| curses.KEY\_SPRINT | Shifted Print |
| curses.KEY\_SREDO | Shifted Redo |
| curses.KEY\_SREPLACE | Shifted Replace |
| curses.KEY\_SRIGHT | Shifted Right arrow |
| curses.KEY\_SRSUME | Shifted Resume |
| curses.KEY\_SSAVE | Shifted Save |
| curses.KEY\_SSUSPEND | Shifted Suspend |
| curses.KEY\_SUNDO | Shifted Undo |
| curses.KEY\_SUSPEND | Suspend |
| curses.KEY\_UNDO | Undo |
| curses.KEY\_MOUSE | Mouse event has occurred |
| curses.KEY\_RESIZE | Terminal resize event |
| curses.KEY\_MAX | Maximum key value |

On VT100s and their software emulations, such as X terminal emulators, there are
normally at least four function keys ([`KEY_F1`](#curses.KEY_Fn "curses.KEY_Fn"), [`KEY_F2`](#curses.KEY_Fn "curses.KEY_Fn"),
[`KEY_F3`](#curses.KEY_Fn "curses.KEY_Fn"), [`KEY_F4`](#curses.KEY_Fn "curses.KEY_Fn")) available, and the arrow keys mapped to
[`KEY_UP`](#curses.KEY_UP "curses.KEY_UP"), [`KEY_DOWN`](#curses.KEY_DOWN "curses.KEY_DOWN"), [`KEY_LEFT`](#curses.KEY_LEFT "curses.KEY_LEFT") and [`KEY_RIGHT`](#curses.KEY_RIGHT "curses.KEY_RIGHT") in
the obvious way. If your machine has a PC keyboard, it is safe to expect arrow
keys and twelve function keys (older PC keyboards may have only ten function
keys); also, the following keypad mappings are standard:

| Keycap | Constant |
| --- | --- |
| `Insert` | KEY\_IC |
| `Delete` | KEY\_DC |
| `Home` | KEY\_HOME |
| `End` | KEY\_END |
| `Page Up` | KEY\_PPAGE |
| `Page Down` | KEY\_NPAGE |

The following table lists characters from the alternate character set. These are
inherited from the VT100 terminal, and will generally be available on software
emulations such as X terminals. When there is no graphic available, curses
falls back on a crude printable ASCII approximation.

Note

These are available only after [`initscr()`](#curses.initscr "curses.initscr") has been called.

| ACS code | Meaning |
| --- | --- |
| curses.ACS\_BBSS | alternate name for upper right corner |
| curses.ACS\_BLOCK | solid square block |
| curses.ACS\_BOARD | board of squares |
| curses.ACS\_BSBS | alternate name for horizontal line |
| curses.ACS\_BSSB | alternate name for upper left corner |
| curses.ACS\_BSSS | alternate name for top tee |
| curses.ACS\_BTEE | bottom tee |
| curses.ACS\_BULLET | bullet |
| curses.ACS\_CKBOARD | checker board (stipple) |
| curses.ACS\_DARROW | arrow pointing down |
| curses.ACS\_DEGREE | degree symbol |
| curses.ACS\_DIAMOND | diamond |
| curses.ACS\_GEQUAL | greater-than-or-equal-to |
| curses.ACS\_HLINE | horizontal line |
| curses.ACS\_LANTERN | lantern symbol |
| curses.ACS\_LARROW | left arrow |
| curses.ACS\_LEQUAL | less-than-or-equal-to |
| curses.ACS\_LLCORNER | lower left-hand corner |
| curses.ACS\_LRCORNER | lower right-hand corner |
| curses.ACS\_LTEE | left tee |
| curses.ACS\_NEQUAL | not-equal sign |
| curses.ACS\_PI | letter pi |
| curses.ACS\_PLMINUS | plus-or-minus sign |
| curses.ACS\_PLUS | big plus sign |
| curses.ACS\_RARROW | right arrow |
| curses.ACS\_RTEE | right tee |
| curses.ACS\_S1 | scan line 1 |
| curses.ACS\_S3 | scan line 3 |
| curses.ACS\_S7 | scan line 7 |
| curses.ACS\_S9 | scan line 9 |
| curses.ACS\_SBBS | alternate name for lower right corner |
| curses.ACS\_SBSB | alternate name for vertical line |
| curses.ACS\_SBSS | alternate name for right tee |
| curses.ACS\_SSBB | alternate name for lower left corner |
| curses.ACS\_SSBS | alternate name for bottom tee |
| curses.ACS\_SSSB | alternate name for left tee |
| curses.ACS\_SSSS | alternate name for crossover or big plus |
| curses.ACS\_STERLING | pound sterling |
| curses.ACS\_TTEE | top tee |
| curses.ACS\_UARROW | up arrow |
| curses.ACS\_ULCORNER | upper left corner |
| curses.ACS\_URCORNER | upper right corner |
| curses.ACS\_VLINE | vertical line |

The following table lists mouse button constants used by [`getmouse()`](#curses.getmouse "curses.getmouse"):

| Mouse button constant | Meaning |
| --- | --- |
| curses.BUTTONn\_PRESSED | Mouse button *n* pressed |
| curses.BUTTONn\_RELEASED | Mouse button *n* released |
| curses.BUTTONn\_CLICKED | Mouse button *n* clicked |
| curses.BUTTONn\_DOUBLE\_CLICKED | Mouse button *n* double clicked |
| curses.BUTTONn\_TRIPLE\_CLICKED | Mouse button *n* triple clicked |
| curses.BUTTON\_SHIFT | Shift was down during button state change |
| curses.BUTTON\_CTRL | Control was down during button state change |
| curses.BUTTON\_ALT | Control was down during button state change |

Changed in version 3.10: The `BUTTON5_*` constants are now exposed if they are provided by the
underlying curses library.

The following table lists the predefined colors:

| Constant | Color |
| --- | --- |
| curses.COLOR\_BLACK | Black |
| curses.COLOR\_BLUE | Blue |
| curses.COLOR\_CYAN | Cyan (light greenish blue) |
| curses.COLOR\_GREEN | Green |
| curses.COLOR\_MAGENTA | Magenta (purplish red) |
| curses.COLOR\_RED | Red |
| curses.COLOR\_WHITE | White |
| curses.COLOR\_YELLOW | Yellow |

[`curses.textpad`](#module-curses.textpad "curses.textpad: Emacs-like input editing in a curses window.") — Text input widget for curses programs
=================================================================================================================================================

The [`curses.textpad`](#module-curses.textpad "curses.textpad: Emacs-like input editing in a curses window.") module provides a [`Textbox`](#curses.textpad.Textbox "curses.textpad.Textbox") class that handles
elementary text editing in a curses window, supporting a set of keybindings
resembling those of Emacs (thus, also of Netscape Navigator, BBedit 6.x,
FrameMaker, and many other programs). The module also provides a
rectangle-drawing function useful for framing text boxes or for other purposes.

The module [`curses.textpad`](#module-curses.textpad "curses.textpad: Emacs-like input editing in a curses window.") defines the following function:

curses.textpad.rectangle(*win*, *uly*, *ulx*, *lry*, *lrx*)
:   Draw a rectangle. The first argument must be a window object; the remaining
    arguments are coordinates relative to that window. The second and third
    arguments are the y and x coordinates of the upper left hand corner of the
    rectangle to be drawn; the fourth and fifth arguments are the y and x
    coordinates of the lower right hand corner. The rectangle will be drawn using
    VT100/IBM PC forms characters on terminals that make this possible (including
    xterm and most other software terminal emulators). Otherwise it will be drawn
    with ASCII dashes, vertical bars, and plus signs.

Textbox objects
---------------

You can instantiate a [`Textbox`](#curses.textpad.Textbox "curses.textpad.Textbox") object as follows:

*class* curses.textpad.Textbox(*win*)
:   Return a textbox widget object. The *win* argument should be a curses
    [window](#curses-window-objects) object in which the textbox is to
    be contained. The edit cursor of the textbox is initially located at the
    upper left hand corner of the containing window, with coordinates `(0, 0)`.
    The instance’s [`stripspaces`](#curses.textpad.Textbox.stripspaces "curses.textpad.Textbox.stripspaces") flag is initially on.

    [`Textbox`](#curses.textpad.Textbox "curses.textpad.Textbox") objects have the following methods:

    edit([*validator*])
    :   This is the entry point you will normally use. It accepts editing
        keystrokes until one of the termination keystrokes is entered. If
        *validator* is supplied, it must be a function. It will be called for
        each keystroke entered with the keystroke as a parameter; command dispatch
        is done on the result. This method returns the window contents as a
        string; whether blanks in the window are included is affected by the
        [`stripspaces`](#curses.textpad.Textbox.stripspaces "curses.textpad.Textbox.stripspaces") attribute.

    do\_command(*ch*)
    :   Process a single command keystroke. Here are the supported special
        keystrokes:

        | Keystroke | Action |
        | --- | --- |
        | `Control`-`A` | Go to left edge of window. |
        | `Control`-`B` | Cursor left, wrapping to previous line if appropriate. |
        | `Control`-`D` | Delete character under cursor. |
        | `Control`-`E` | Go to right edge (stripspaces off) or end of line (stripspaces on). |
        | `Control`-`F` | Cursor right, wrapping to next line when appropriate. |
        | `Control`-`G` | Terminate, returning the window contents. |
        | `Control`-`H` | Delete character backward. |
        | `Control`-`J` | Terminate if the window is 1 line, otherwise insert newline. |
        | `Control`-`K` | If line is blank, delete it, otherwise clear to end of line. |
        | `Control`-`L` | Refresh screen. |
        | `Control`-`N` | Cursor down; move down one line. |
        | `Control`-`O` | Insert a blank line at cursor location. |
        | `Control`-`P` | Cursor up; move up one line. |

        Move operations do nothing if the cursor is at an edge where the movement
        is not possible. The following synonyms are supported where possible:

        All other keystrokes are treated as a command to insert the given
        character and move right (with line wrapping).

    gather()
    :   Return the window contents as a string; whether blanks in the
        window are included is affected by the [`stripspaces`](#curses.textpad.Textbox.stripspaces "curses.textpad.Textbox.stripspaces") member.

    stripspaces
    :   This attribute is a flag which controls the interpretation of blanks in
        the window. When it is on, trailing blanks on each line are ignored; any
        cursor motion that would land the cursor on a trailing blank goes to the
        end of that line instead, and trailing blanks are stripped when the window
        contents are gathered.