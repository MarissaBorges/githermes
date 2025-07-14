### Native Load/Save Dialogs

The following classes and functions provide file dialog windows that combine a
native look-and-feel with configuration options to customize behaviour.
The following keyword arguments are applicable to the classes and functions
listed below:

> *parent* - the window to place the dialog on top of
>
> *title* - the title of the window
>
> *initialdir* - the directory that the dialog starts in
>
> *initialfile* - the file selected upon opening of the dialog
>
> *filetypes* - a sequence of (label, pattern) tuples, ‘\*’ wildcard is allowed
>
> *defaultextension* - default extension to append to file (save dialogs)
>
> *multiple* - when true, selection of multiple items is allowed

**Static factory functions**

The below functions when called create a modal, native look-and-feel dialog,
wait for the user’s selection, then return the selected value(s) or `None` to the
caller.

tkinter.filedialog.askopenfile(*mode='r'*, *\*\*options*)

tkinter.filedialog.askopenfiles(*mode='r'*, *\*\*options*)
:   The above two functions create an [`Open`](#tkinter.filedialog.Open "tkinter.filedialog.Open") dialog and return the opened
    file object(s) in read-only mode.

tkinter.filedialog.asksaveasfile(*mode='w'*, *\*\*options*)
:   Create a [`SaveAs`](#tkinter.filedialog.SaveAs "tkinter.filedialog.SaveAs") dialog and return a file object opened in write-only mode.

tkinter.filedialog.askopenfilename(*\*\*options*)

tkinter.filedialog.askopenfilenames(*\*\*options*)
:   The above two functions create an [`Open`](#tkinter.filedialog.Open "tkinter.filedialog.Open") dialog and return the
    selected filename(s) that correspond to existing file(s).

tkinter.filedialog.asksaveasfilename(*\*\*options*)
:   Create a [`SaveAs`](#tkinter.filedialog.SaveAs "tkinter.filedialog.SaveAs") dialog and return the selected filename.

tkinter.filedialog.askdirectory(*\*\*options*)
:   Prompt user to select a directory.

    Additional keyword option:

    *mustexist* - determines if selection must be an existing directory.

*class* tkinter.filedialog.Open(*master=None*, *\*\*options*)

*class* tkinter.filedialog.SaveAs(*master=None*, *\*\*options*)
:   The above two classes provide native dialog windows for saving and loading
    files.

**Convenience classes**

The below classes are used for creating file/directory windows from scratch.
These do not emulate the native look-and-feel of the platform.

*class* tkinter.filedialog.Directory(*master=None*, *\*\*options*)
:   Create a dialog prompting the user to select a directory.

Note

The *FileDialog* class should be subclassed for custom event
handling and behaviour.

*class* tkinter.filedialog.FileDialog(*master*, *title=None*)
:   Create a basic file selection dialog.

    cancel\_command(*event=None*)
    :   Trigger the termination of the dialog window.

    dirs\_double\_event(*event*)
    :   Event handler for double-click event on directory.

    dirs\_select\_event(*event*)
    :   Event handler for click event on directory.

    files\_double\_event(*event*)
    :   Event handler for double-click event on file.

    files\_select\_event(*event*)
    :   Event handler for single-click event on file.

    filter\_command(*event=None*)
    :   Filter the files by directory.

    get\_filter()
    :   Retrieve the file filter currently in use.

    get\_selection()
    :   Retrieve the currently selected item.

    go(*dir\_or\_file=os.curdir*, *pattern='\*'*, *default=''*, *key=None*)
    :   Render dialog and start event loop.

    ok\_event(*event*)
    :   Exit dialog returning current selection.

    quit(*how=None*)
    :   Exit dialog returning filename, if any.

    set\_filter(*dir*, *pat*)
    :   Set the file filter.

    set\_selection(*file*)
    :   Update the current file selection to *file*.

*class* tkinter.filedialog.LoadFileDialog(*master*, *title=None*)
:   A subclass of FileDialog that creates a dialog window for selecting an
    existing file.

    ok\_command()
    :   Test that a file is provided and that the selection indicates an
        already existing file.

*class* tkinter.filedialog.SaveFileDialog(*master*, *title=None*)
:   A subclass of FileDialog that creates a dialog window for selecting a
    destination file.

    ok\_command()
    :   Test whether or not the selection points to a valid file that is not a
        directory. Confirmation is required if an already existing file is
        selected.