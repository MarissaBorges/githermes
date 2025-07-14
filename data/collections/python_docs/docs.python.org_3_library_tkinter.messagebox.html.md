`tkinter.messagebox` — Tkinter message prompts
==============================================

**Source code:** [Lib/tkinter/messagebox.py](https://github.com/python/cpython/tree/3.13/Lib/tkinter/messagebox.py)

---

The [`tkinter.messagebox`](#module-tkinter.messagebox "tkinter.messagebox: Various types of alert dialogs (Tk)") module provides a template base class as well as
a variety of convenience methods for commonly used configurations. The message
boxes are modal and will return a subset of (`True`, `False`, `None`,
[`OK`](#tkinter.messagebox.OK "tkinter.messagebox.OK"), [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL"), [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES"), [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO")) based on
the user’s selection. Common message box styles and layouts include but are not
limited to:

![../_images/tk_msg.png](../_images/tk_msg.png)

*class* tkinter.messagebox.Message(*master=None*, *\*\*options*)
:   Create a message window with an application-specified message, an icon
    and a set of buttons.
    Each of the buttons in the message window is identified by a unique symbolic name (see the *type* options).

    The following options are supported:

    > *command*
    > :   Specifies the function to invoke when the user closes the dialog.
    >     The name of the button clicked by the user to close the dialog is
    >     passed as argument.
    >     This is only available on macOS.
    >
    > *default*
    > :   Gives the [symbolic name](#messagebox-buttons) of the default button
    >     for this message window ([`OK`](#tkinter.messagebox.OK "tkinter.messagebox.OK"), [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL"), and so on).
    >     If this option is not specified, the first button in the dialog will
    >     be made the default.
    >
    > *detail*
    > :   Specifies an auxiliary message to the main message given by the
    >     *message* option.
    >     The message detail will be presented beneath the main message and,
    >     where supported by the OS, in a less emphasized font than the main
    >     message.
    >
    > *icon*
    > :   Specifies an [icon](#messagebox-icons) to display.
    >     If this option is not specified, then the [`INFO`](#tkinter.messagebox.INFO "tkinter.messagebox.INFO") icon will be
    >     displayed.
    >
    > *message*
    > :   Specifies the message to display in this message box.
    >     The default value is an empty string.
    >
    > *parent*
    > :   Makes the specified window the logical parent of the message box.
    >     The message box is displayed on top of its parent window.
    >
    > *title*
    > :   Specifies a string to display as the title of the message box.
    >     This option is ignored on macOS, where platform guidelines forbid
    >     the use of a title on this kind of dialog.
    >
    > *type*
    > :   Arranges for a [predefined set of buttons](#messagebox-types)
    >     to be displayed.

    show(*\*\*options*)
    :   Display a message window and wait for the user to select one of the buttons. Then return the symbolic name of the selected button.
        Keyword arguments can override options specified in the constructor.

**Information message box**

tkinter.messagebox.showinfo(*title=None*, *message=None*, *\*\*options*)
:   Creates and displays an information message box with the specified title
    and message.

**Warning message boxes**

tkinter.messagebox.showwarning(*title=None*, *message=None*, *\*\*options*)
:   Creates and displays a warning message box with the specified title
    and message.

tkinter.messagebox.showerror(*title=None*, *message=None*, *\*\*options*)
:   Creates and displays an error message box with the specified title
    and message.

**Question message boxes**

tkinter.messagebox.askquestion(*title=None*, *message=None*, *\**, *type=YESNO*, *\*\*options*)
:   Ask a question. By default shows buttons [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES") and [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO").
    Returns the symbolic name of the selected button.

tkinter.messagebox.askokcancel(*title=None*, *message=None*, *\*\*options*)
:   Ask if operation should proceed. Shows buttons [`OK`](#tkinter.messagebox.OK "tkinter.messagebox.OK") and [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").
    Returns `True` if the answer is ok and `False` otherwise.

tkinter.messagebox.askretrycancel(*title=None*, *message=None*, *\*\*options*)
:   Ask if operation should be retried. Shows buttons [`RETRY`](#tkinter.messagebox.RETRY "tkinter.messagebox.RETRY") and [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").
    Return `True` if the answer is yes and `False` otherwise.

tkinter.messagebox.askyesno(*title=None*, *message=None*, *\*\*options*)
:   Ask a question. Shows buttons [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES") and [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO").
    Returns `True` if the answer is yes and `False` otherwise.

tkinter.messagebox.askyesnocancel(*title=None*, *message=None*, *\*\*options*)
:   Ask a question. Shows buttons [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES"), [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO") and [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").
    Return `True` if the answer is yes, `None` if cancelled, and `False`
    otherwise.

Symbolic names of buttons:

tkinter.messagebox.ABORT *= 'abort'*

tkinter.messagebox.RETRY *= 'retry'*

tkinter.messagebox.IGNORE *= 'ignore'*

tkinter.messagebox.OK *= 'ok'*

tkinter.messagebox.CANCEL *= 'cancel'*

tkinter.messagebox.YES *= 'yes'*

tkinter.messagebox.NO *= 'no'*

Predefined sets of buttons:

tkinter.messagebox.ABORTRETRYIGNORE *= 'abortretryignore'*
:   Displays three buttons whose symbolic names are [`ABORT`](#tkinter.messagebox.ABORT "tkinter.messagebox.ABORT"),
    [`RETRY`](#tkinter.messagebox.RETRY "tkinter.messagebox.RETRY") and [`IGNORE`](#tkinter.messagebox.IGNORE "tkinter.messagebox.IGNORE").

tkinter.messagebox.OK *= 'ok'*
:   Displays one button whose symbolic name is [`OK`](#tkinter.messagebox.OK "tkinter.messagebox.OK").

tkinter.messagebox.OKCANCEL *= 'okcancel'*
:   Displays two buttons whose symbolic names are [`OK`](#tkinter.messagebox.OK "tkinter.messagebox.OK") and
    [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").

tkinter.messagebox.RETRYCANCEL *= 'retrycancel'*
:   Displays two buttons whose symbolic names are [`RETRY`](#tkinter.messagebox.RETRY "tkinter.messagebox.RETRY") and
    [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").

tkinter.messagebox.YESNO *= 'yesno'*
:   Displays two buttons whose symbolic names are [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES") and
    [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO").

tkinter.messagebox.YESNOCANCEL *= 'yesnocancel'*
:   Displays three buttons whose symbolic names are [`YES`](#tkinter.messagebox.YES "tkinter.messagebox.YES"),
    [`NO`](#tkinter.messagebox.NO "tkinter.messagebox.NO") and [`CANCEL`](#tkinter.messagebox.CANCEL "tkinter.messagebox.CANCEL").

Icon images:

tkinter.messagebox.ERROR *= 'error'*

tkinter.messagebox.INFO *= 'info'*

tkinter.messagebox.QUESTION *= 'question'*

tkinter.messagebox.WARNING *= 'warning'*