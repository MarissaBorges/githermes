Tkinter supports a range of Tcl/Tk versions, built either with or
without thread support. The official Python binary release bundles Tcl/Tk 8.6
threaded. See the source code for the [`_tkinter`](#module-_tkinter "_tkinter: A binary module that contains the low-level interface to Tcl/Tk.") module
for more information about supported versions.

Tkinter is not a thin wrapper, but adds a fair amount of its own logic to
make the experience more pythonic. This documentation will concentrate on these
additions and changes, and refer to the official Tcl/Tk documentation for
details that are unchanged.

Architecture
------------

Tcl/Tk is not a single library but rather consists of a few distinct
modules, each with separate functionality and its own official
documentation. Python’s binary releases also ship an add-on module
together with it.

Tcl
:   Tcl is a dynamic interpreted programming language, just like Python. Though
    it can be used on its own as a general-purpose programming language, it is
    most commonly embedded into C applications as a scripting engine or an
    interface to the Tk toolkit. The Tcl library has a C interface to
    create and manage one or more instances of a Tcl interpreter, run Tcl
    commands and scripts in those instances, and add custom commands
    implemented in either Tcl or C. Each interpreter has an event queue,
    and there are facilities to send events to it and process them.
    Unlike Python, Tcl’s execution model is designed around cooperative
    multitasking, and Tkinter bridges this difference
    (see [Threading model](#threading-model) for details).

Tk
:   Tk is a [Tcl package](https://wiki.tcl-lang.org/37432) implemented in C
    that adds custom commands to create and manipulate GUI widgets. Each
    [`Tk`](#tkinter.Tk "tkinter.Tk") object embeds its own Tcl interpreter instance with Tk loaded into
    it. Tk’s widgets are very customizable, though at the cost of a dated appearance.
    Tk uses Tcl’s event queue to generate and process GUI events.

Ttk
:   Themed Tk (Ttk) is a newer family of Tk widgets that provide a much better
    appearance on different platforms than many of the classic Tk widgets.
    Ttk is distributed as part of Tk, starting with Tk version 8.5. Python
    bindings are provided in a separate module, [`tkinter.ttk`](tkinter.ttk.html#module-tkinter.ttk "tkinter.ttk: Tk themed widget set").

Internally, Tk and Ttk use facilities of the underlying operating system,
i.e., Xlib on Unix/X11, Cocoa on macOS, GDI on Windows.

When your Python application uses a class in Tkinter, e.g., to create a widget,
the [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") module first assembles a Tcl/Tk command string. It passes that
Tcl command string to an internal [`_tkinter`](#module-_tkinter "_tkinter: A binary module that contains the low-level interface to Tcl/Tk.") binary module, which then
calls the Tcl interpreter to evaluate it. The Tcl interpreter will then call into the
Tk and/or Ttk packages, which will in turn make calls to Xlib, Cocoa, or GDI.

Tkinter Life Preserver
----------------------

This section is not designed to be an exhaustive tutorial on either Tk or
Tkinter. For that, refer to one of the external resources noted earlier.
Instead, this section provides a very quick orientation to what a Tkinter
application looks like, identifies foundational Tk concepts, and
explains how the Tkinter wrapper is structured.

The remainder of this section will help you to identify the classes,
methods, and options you’ll need in your Tkinter application, and where to
find more detailed documentation on them, including in the official Tcl/Tk
reference manual.

### A Hello World Program

We’ll start by walking through a “Hello World” application in Tkinter. This
isn’t the smallest one we could write, but has enough to illustrate some
key concepts you’ll need to know.

Copy

```
from tkinter import *
from tkinter import ttk
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()

```

After the imports, the next line creates an instance of the `Tk` class,
which initializes Tk and creates its associated Tcl interpreter. It also
creates a toplevel window, known as the root window, which serves as the main
window of the application.

The following line creates a frame widget, which in this case will contain
a label and a button we’ll create next. The frame is fit inside the root
window.

The next line creates a label widget holding a static text string. The
`grid()` method is used to specify the relative layout (position) of the
label within its containing frame widget, similar to how tables in HTML work.

A button widget is then created, and placed to the right of the label. When
pressed, it will call the `destroy()` method of the root window.

Finally, the `mainloop()` method puts everything on the display, and
responds to user input until the program terminates.

### Important Tk Concepts

Even this simple program illustrates the following key Tk concepts:

widgets
:   A Tkinter user interface is made up of individual *widgets*. Each widget is
    represented as a Python object, instantiated from classes like
    `ttk.Frame`, `ttk.Label`, and `ttk.Button`.

widget hierarchy
:   Widgets are arranged in a *hierarchy*. The label and button were contained
    within a frame, which in turn was contained within the root window. When
    creating each *child* widget, its *parent* widget is passed as the first
    argument to the widget constructor.

configuration options
:   Widgets have *configuration options*, which modify their appearance and
    behavior, such as the text to display in a label or button. Different
    classes of widgets will have different sets of options.

geometry management
:   Widgets aren’t automatically added to the user interface when they are
    created. A *geometry manager* like `grid` controls where in the
    user interface they are placed.

event loop
:   Tkinter reacts to user input, changes from your program, and even refreshes
    the display only when actively running an *event loop*. If your program
    isn’t running the event loop, your user interface won’t update.

### Understanding How Tkinter Wraps Tcl/Tk

When your application uses Tkinter’s classes and methods, internally Tkinter
is assembling strings representing Tcl/Tk commands, and executing those
commands in the Tcl interpreter attached to your application’s `Tk`
instance.

Whether it’s trying to navigate reference documentation, trying to find
the right method or option, adapting some existing code, or debugging your
Tkinter application, there are times that it will be useful to understand
what those underlying Tcl/Tk commands look like.

To illustrate, here is the Tcl/Tk equivalent of the main part of the Tkinter
script above.

Copy

```
ttk::frame .frm -padding 10
grid .frm
grid [ttk::label .frm.lbl -text "Hello World!"] -column 0 -row 0
grid [ttk::button .frm.btn -text "Quit" -command "destroy ."] -column 1 -row 0

```

Tcl’s syntax is similar to many shell languages, where the first word is the
command to be executed, with arguments to that command following it, separated
by spaces. Without getting into too many details, notice the following:

* The commands used to create widgets (like `ttk::frame`) correspond to
  widget classes in Tkinter.
* Tcl widget options (like `-text`) correspond to keyword arguments in
  Tkinter.
* Widgets are referred to by a *pathname* in Tcl (like `.frm.btn`),
  whereas Tkinter doesn’t use names but object references.
* A widget’s place in the widget hierarchy is encoded in its (hierarchical)
  pathname, which uses a `.` (dot) as a path separator. The pathname for
  the root window is just `.` (dot). In Tkinter, the hierarchy is defined
  not by pathname but by specifying the parent widget when creating each
  child widget.
* Operations which are implemented as separate *commands* in Tcl (like
  `grid` or `destroy`) are represented as *methods* on Tkinter widget
  objects. As you’ll see shortly, at other times Tcl uses what appear to be
  method calls on widget objects, which more closely mirror what would is
  used in Tkinter.

### How do I…? What option does…?

If you’re not sure how to do something in Tkinter, and you can’t immediately
find it in the tutorial or reference documentation you’re using, there are a
few strategies that can be helpful.

First, remember that the details of how individual widgets work may vary
across different versions of both Tkinter and Tcl/Tk. If you’re searching
documentation, make sure it corresponds to the Python and Tcl/Tk versions
installed on your system.

When searching for how to use an API, it helps to know the exact name of the
class, option, or method that you’re using. Introspection, either in an
interactive Python shell or with [`print()`](functions.html#print "print"), can help you identify what
you need.

To find out what configuration options are available on any widget, call its
`configure()` method, which returns a dictionary containing a variety of
information about each object, including its default and current values. Use
`keys()` to get just the names of each option.

Copy

```
btn = ttk.Button(frm, ...)
print(btn.configure().keys())

```

As most widgets have many configuration options in common, it can be useful
to find out which are specific to a particular widget class. Comparing the
list of options to that of a simpler widget, like a frame, is one way to
do that.

Copy

```
print(set(btn.configure().keys()) - set(frm.configure().keys()))

```

Similarly, you can find the available methods for a widget object using the
standard [`dir()`](functions.html#dir "dir") function. If you try it, you’ll see there are over 200
common widget methods, so again identifying those specific to a widget class
is helpful.

Copy

```
print(dir(btn))
print(set(dir(btn)) - set(dir(frm)))

```

### Navigating the Tcl/Tk Reference Manual

As noted, the official [Tk commands](https://www.tcl.tk/man/tcl8.6/TkCmd/contents.htm)
reference manual (man pages) is often the most accurate description of what
specific operations on widgets do. Even when you know the name of the option
or method that you need, you may still have a few places to look.

While all operations in Tkinter are implemented as method calls on widget
objects, you’ve seen that many Tcl/Tk operations appear as commands that
take a widget pathname as its first parameter, followed by optional
parameters, e.g.

Copy

```
destroy .
grid .frm.btn -column 0 -row 0

```

Others, however, look more like methods called on a widget object (in fact,
when you create a widget in Tcl/Tk, it creates a Tcl command with the name
of the widget pathname, with the first parameter to that command being the
name of a method to call).

Copy

```
.frm.btn invoke
.frm.lbl configure -text "Goodbye"

```

In the official Tcl/Tk reference documentation, you’ll find most operations
that look like method calls on the man page for a specific widget (e.g.,
you’ll find the `invoke()` method on the
[ttk::button](https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_button.htm)
man page), while functions that take a widget as a parameter often have
their own man page (e.g.,
[grid](https://www.tcl.tk/man/tcl8.6/TkCmd/grid.htm)).

You’ll find many common options and methods in the
[options](https://www.tcl.tk/man/tcl8.6/TkCmd/options.htm) or
[ttk::widget](https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_widget.htm) man
pages, while others are found in the man page for a specific widget class.

You’ll also find that many Tkinter methods have compound names, e.g.,
`winfo_x()`, `winfo_height()`, `winfo_viewable()`. You’d find
documentation for all of these in the
[winfo](https://www.tcl.tk/man/tcl8.6/TkCmd/winfo.htm) man page.

Note

Somewhat confusingly, there are also methods on all Tkinter widgets
that don’t actually operate on the widget, but operate at a global
scope, independent of any widget. Examples are methods for accessing
the clipboard or the system bell. (They happen to be implemented as
methods in the base `Widget` class that all Tkinter widgets
inherit from).

Threading model
---------------

Python and Tcl/Tk have very different threading models, which [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces")
tries to bridge. If you use threads, you may need to be aware of this.

A Python interpreter may have many threads associated with it. In Tcl, multiple
threads can be created, but each thread has a separate Tcl interpreter instance
associated with it. Threads can also create more than one interpreter instance,
though each interpreter instance can be used only by the one thread that created it.

Each `Tk` object created by [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") contains a Tcl interpreter.
It also keeps track of which thread created that interpreter. Calls to
[`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") can be made from any Python thread. Internally, if a call comes
from a thread other than the one that created the `Tk` object, an event
is posted to the interpreter’s event queue, and when executed, the result is
returned to the calling Python thread.

Tcl/Tk applications are normally event-driven, meaning that after initialization,
the interpreter runs an event loop (i.e. `Tk.mainloop()`) and responds to events.
Because it is single-threaded, event handlers must respond quickly, otherwise they
will block other events from being processed. To avoid this, any long-running
computations should not run in an event handler, but are either broken into smaller
pieces using timers, or run in another thread. This is different from many GUI
toolkits where the GUI runs in a completely separate thread from all application
code including event handlers.

If the Tcl interpreter is not running the event loop and processing events, any
[`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") calls made from threads other than the one running the Tcl
interpreter will fail.

A number of special cases exist:

* Tcl/Tk libraries can be built so they are not thread-aware. In this case,
  [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") calls the library from the originating Python thread, even
  if this is different than the thread that created the Tcl interpreter. A global
  lock ensures only one call occurs at a time.
* While [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") allows you to create more than one instance of a `Tk`
  object (with its own interpreter), all interpreters that are part of the same
  thread share a common event queue, which gets ugly fast. In practice, don’t create
  more than one instance of `Tk` at a time. Otherwise, it’s best to create
  them in separate threads and ensure you’re running a thread-aware Tcl/Tk build.
* Blocking event handlers are not the only way to prevent the Tcl interpreter from
  reentering the event loop. It is even possible to run multiple nested event loops
  or abandon the event loop entirely. If you’re doing anything tricky when it comes
  to events or threads, be aware of these possibilities.
* There are a few select [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") functions that presently work only when
  called from the thread that created the Tcl interpreter.

Handy Reference
---------------

### Setting Options

Options control things like the color and border width of a widget. Options can
be set in three ways:

At object creation time, using keyword arguments
:   Copy

    ```
    fred = Button(self, fg="red", bg="blue")

    ```

After object creation, treating the option name like a dictionary index
:   Copy

    ```
    fred["fg"] = "red"
    fred["bg"] = "blue"

    ```

Use the config() method to update multiple attrs subsequent to object creation
:   Copy

    ```
    fred.config(fg="red", bg="blue")

    ```

For a complete explanation of a given option and its behavior, see the Tk man
pages for the widget in question.

Note that the man pages list “STANDARD OPTIONS” and “WIDGET SPECIFIC OPTIONS”
for each widget. The former is a list of options that are common to many
widgets, the latter are the options that are idiosyncratic to that particular
widget. The Standard Options are documented on the *[options(3)](https://manpages.debian.org/options(3))* man
page.

No distinction between standard and widget-specific options is made in this
document. Some options don’t apply to some kinds of widgets. Whether a given
widget responds to a particular option depends on the class of the widget;
buttons have a `command` option, labels do not.

The options supported by a given widget are listed in that widget’s man page, or
can be queried at runtime by calling the `config()` method without
arguments, or by calling the `keys()` method on that widget. The return
value of these calls is a dictionary whose key is the name of the option as a
string (for example, `'relief'`) and whose values are 5-tuples.

Some options, like `bg` are synonyms for common options with long names
(`bg` is shorthand for “background”). Passing the `config()` method the name
of a shorthand option will return a 2-tuple, not 5-tuple. The 2-tuple passed
back will contain the name of the synonym and the “real” option (such as
`('bg', 'background')`).

| Index | Meaning | Example |
| --- | --- | --- |
| 0 | option name | `'relief'` |
| 1 | option name for database lookup | `'relief'` |
| 2 | option class for database lookup | `'Relief'` |
| 3 | default value | `'raised'` |
| 4 | current value | `'groove'` |

Example:

Copy

```
>>> print(fred.config())
{'relief': ('relief', 'relief', 'Relief', 'raised', 'groove')}

```

Of course, the dictionary printed will include all the options available and
their values. This is meant only as an example.

### The Packer

The packer is one of Tk’s geometry-management mechanisms. Geometry managers
are used to specify the relative positioning of widgets within their container -
their mutual *master*. In contrast to the more cumbersome *placer* (which is
used less commonly, and we do not cover here), the packer takes qualitative
relationship specification - *above*, *to the left of*, *filling*, etc - and
works everything out to determine the exact placement coordinates for you.

The size of any *master* widget is determined by the size of the “slave widgets”
inside. The packer is used to control where slave widgets appear inside the
master into which they are packed. You can pack widgets into frames, and frames
into other frames, in order to achieve the kind of layout you desire.
Additionally, the arrangement is dynamically adjusted to accommodate incremental
changes to the configuration, once it is packed.

Note that widgets do not appear until they have had their geometry specified
with a geometry manager. It’s a common early mistake to leave out the geometry
specification, and then be surprised when the widget is created but nothing
appears. A widget will appear only after it has had, for example, the packer’s
`pack()` method applied to it.

The pack() method can be called with keyword-option/value pairs that control
where the widget is to appear within its container, and how it is to behave when
the main application window is resized. Here are some examples:

Copy

```
fred.pack()                     # defaults to side = "top"
fred.pack(side="left")
fred.pack(expand=1)

```

### Packer Options

For more extensive information on the packer and the options that it can take,
see the man pages and page 183 of John Ousterhout’s book.

anchor
:   Anchor type. Denotes where the packer is to place each slave in its parcel.

expand
:   Boolean, `0` or `1`.

fill
:   Legal values: `'x'`, `'y'`, `'both'`, `'none'`.

ipadx and ipady
:   A distance - designating internal padding on each side of the slave widget.

padx and pady
:   A distance - designating external padding on each side of the slave widget.

side
:   Legal values are: `'left'`, `'right'`, `'top'`, `'bottom'`.

### The Window Manager

In Tk, there is a utility command, `wm`, for interacting with the window
manager. Options to the `wm` command allow you to control things like titles,
placement, icon bitmaps, and the like. In [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces"), these commands have
been implemented as methods on the `Wm` class. Toplevel widgets are
subclassed from the `Wm` class, and so can call the `Wm` methods
directly.

To get at the toplevel window that contains a given widget, you can often just
refer to the widget’s master. Of course if the widget has been packed inside of
a frame, the master won’t represent a toplevel window. To get at the toplevel
window that contains an arbitrary widget, you can call the `_root()` method.
This method begins with an underscore to denote the fact that this function is
part of the implementation, and not an interface to Tk functionality.

Here are some examples of typical usage:

Copy

```
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()

```

### Tk Option Data Types

anchor
:   Legal values are points of the compass: `"n"`, `"ne"`, `"e"`, `"se"`,
    `"s"`, `"sw"`, `"w"`, `"nw"`, and also `"center"`.

bitmap
:   There are eight built-in, named bitmaps: `'error'`, `'gray25'`,
    `'gray50'`, `'hourglass'`, `'info'`, `'questhead'`, `'question'`,
    `'warning'`. To specify an X bitmap filename, give the full path to the file,
    preceded with an `@`, as in `"@/usr/contrib/bitmap/gumby.bit"`.

boolean
:   You can pass integers 0 or 1 or the strings `"yes"` or `"no"`.

callback
:   This is any Python function that takes no arguments. For example:

    Copy

    ```
    def print_it():
        print("hi there")
    fred["command"] = print_it

    ```

color
:   Colors can be given as the names of X colors in the rgb.txt file, or as strings
    representing RGB values in 4 bit: `"#RGB"`, 8 bit: `"#RRGGBB"`, 12 bit:
    `"#RRRGGGBBB"`, or 16 bit: `"#RRRRGGGGBBBB"` ranges, where R,G,B here
    represent any legal hex digit. See page 160 of Ousterhout’s book for details.

cursor
:   The standard X cursor names from `cursorfont.h` can be used, without the
    `XC_` prefix. For example to get a hand cursor (`XC_hand2`), use the
    string `"hand2"`. You can also specify a bitmap and mask file of your own.
    See page 179 of Ousterhout’s book.

distance
:   Screen distances can be specified in either pixels or absolute distances.
    Pixels are given as numbers and absolute distances as strings, with the trailing
    character denoting units: `c` for centimetres, `i` for inches, `m` for
    millimetres, `p` for printer’s points. For example, 3.5 inches is expressed
    as `"3.5i"`.

font
:   Tk uses a list font name format, such as `{courier 10 bold}`. Font sizes with
    positive numbers are measured in points; sizes with negative numbers are
    measured in pixels.

geometry
:   This is a string of the form `widthxheight`, where width and height are
    measured in pixels for most widgets (in characters for widgets displaying text).
    For example: `fred["geometry"] = "200x100"`.

justify
:   Legal values are the strings: `"left"`, `"center"`, `"right"`, and
    `"fill"`.

region
:   This is a string with four space-delimited elements, each of which is a legal
    distance (see above). For example: `"2 3 4 5"` and `"3i 2i 4.5i 2i"` and
    `"3c 2c 4c 10.43c"` are all legal regions.

relief
:   Determines what the border style of a widget will be. Legal values are:
    `"raised"`, `"sunken"`, `"flat"`, `"groove"`, and `"ridge"`.

scrollcommand
:   This is almost always the `set()` method of some scrollbar widget, but can
    be any widget method that takes a single argument.

wrap
:   Must be one of: `"none"`, `"char"`, or `"word"`.

### Bindings and Events

The bind method from the widget command allows you to watch for certain events
and to have a callback function trigger when that event type occurs. The form
of the bind method is:

Copy

```
def bind(self, sequence, func, add=''):

```

where:

sequence
:   is a string that denotes the target kind of event. (See the
    *[bind(3tk)](https://manpages.debian.org/bind(3tk))* man page, and page 201 of John Ousterhout’s book,
    Tcl and the Tk Toolkit (2nd edition), for details).

func
:   is a Python function, taking one argument, to be invoked when the event occurs.
    An Event instance will be passed as the argument. (Functions deployed this way
    are commonly known as *callbacks*.)

add
:   is optional, either `''` or `'+'`. Passing an empty string denotes that
    this binding is to replace any other bindings that this event is associated
    with. Passing a `'+'` means that this function is to be added to the list
    of functions bound to this event type.

For example:

Copy

```
def turn_red(self, event):
    event.widget["activeforeground"] = "red"

self.button.bind("<Enter>", self.turn_red)

```

Notice how the widget field of the event is being accessed in the
`turn_red()` callback. This field contains the widget that caught the X
event. The following table lists the other event fields you can access, and how
they are denoted in Tk, which can be useful when referring to the Tk man pages.

| Tk | Tkinter Event Field | Tk | Tkinter Event Field |
| --- | --- | --- | --- |
| %f | focus | %A | char |
| %h | height | %E | send\_event |
| %k | keycode | %K | keysym |
| %s | state | %N | keysym\_num |
| %t | time | %T | type |
| %w | width | %W | widget |
| %x | x | %X | x\_root |
| %y | y | %Y | y\_root |

### The index Parameter

A number of widgets require “index” parameters to be passed. These are used to
point at a specific place in a Text widget, or to particular characters in an
Entry widget, or to particular menu items in a Menu widget.

Entry widget indexes (index, view index, etc.)
:   Entry widgets have options that refer to character positions in the text being
    displayed. You can use these [`tkinter`](#module-tkinter "tkinter: Interface to Tcl/Tk for graphical user interfaces") functions to access these special
    points in text widgets:

Text widget indexes
:   The index notation for Text widgets is very rich and is best described in the Tk
    man pages.

Menu indexes (menu.invoke(), menu.entryconfig(), etc.)
:   Some options and methods for menus manipulate specific menu entries. Anytime a
    menu index is needed for an option or a parameter, you may pass in:

    * an integer which refers to the numeric position of the entry in the widget,
      counted from the top, starting with 0;
    * the string `"active"`, which refers to the menu position that is currently
      under the cursor;
    * the string `"last"` which refers to the last menu item;
    * An integer preceded by `@`, as in `@6`, where the integer is interpreted
      as a y pixel coordinate in the menu’s coordinate system;
    * the string `"none"`, which indicates no menu entry at all, most often used
      with menu.activate() to deactivate all entries, and finally,
    * a text string that is pattern matched against the label of the menu entry, as
      scanned from the top of the menu to the bottom. Note that this index type is
      considered after all the others, which means that matches for menu items
      labelled `last`, `active`, or `none` may be interpreted as the above
      literals, instead.

### Images

Images of different formats can be created through the corresponding subclass
of `tkinter.Image`:

* `BitmapImage` for images in XBM format.
* `PhotoImage` for images in PGM, PPM, GIF and PNG formats. The latter
  is supported starting with Tk 8.6.

Either type of image is created through either the `file` or the `data`
option (other options are available as well).

Changed in version 3.13: Added the `PhotoImage` method `copy_replace()` to copy a region
from one image to other image, possibly with pixel zooming and/or
subsampling.
Add *from\_coords* parameter to `PhotoImage` methods `copy()`,
`zoom()` and `subsample()`.
Add *zoom* and *subsample* parameters to `PhotoImage` method
`copy()`.

The image object can then be used wherever an `image` option is supported by
some widget (e.g. labels, buttons, menus). In these cases, Tk will not keep a
reference to the image. When the last Python reference to the image object is
deleted, the image data is deleted as well, and Tk will display an empty box
wherever the image was used.

See also

The [Pillow](https://python-pillow.org/) package adds support for
formats such as BMP, JPEG, TIFF, and WebP, among others.