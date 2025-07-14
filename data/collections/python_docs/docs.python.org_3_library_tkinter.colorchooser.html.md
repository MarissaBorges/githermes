`tkinter.colorchooser` — Color choosing dialog
==============================================

**Source code:** [Lib/tkinter/colorchooser.py](https://github.com/python/cpython/tree/3.13/Lib/tkinter/colorchooser.py)

---

The [`tkinter.colorchooser`](#module-tkinter.colorchooser "tkinter.colorchooser: Color choosing dialog (Tk)") module provides the [`Chooser`](#tkinter.colorchooser.Chooser "tkinter.colorchooser.Chooser") class
as an interface to the native color picker dialog. `Chooser` implements
a modal color choosing dialog window. The `Chooser` class inherits from
the [`Dialog`](dialog.html#tkinter.commondialog.Dialog "tkinter.commondialog.Dialog") class.

*class* tkinter.colorchooser.Chooser(*master=None*, *\*\*options*)

tkinter.colorchooser.askcolor(*color=None*, *\*\*options*)
:   Create a color choosing dialog. A call to this method will show the window,
    wait for the user to make a selection, and return the selected color (or
    `None`) to the caller.