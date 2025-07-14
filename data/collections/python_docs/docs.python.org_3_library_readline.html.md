`readline` — GNU readline interface
===================================

---

The [`readline`](#module-readline "readline: GNU readline support for Python. (Unix)") module defines a number of functions to facilitate
completion and reading/writing of history files from the Python interpreter.
This module can be used directly, or via the [`rlcompleter`](rlcompleter.html#module-rlcompleter "rlcompleter: Python identifier completion, suitable for the GNU readline library.") module, which
supports completion of Python identifiers at the interactive prompt. Settings
made using this module affect the behaviour of both the interpreter’s
interactive prompt and the prompts offered by the built-in [`input()`](functions.html#input "input")
function.

Readline keybindings may be configured via an initialization file, typically
`.inputrc` in your home directory. See [Readline Init File](https://tiswww.cwru.edu/php/chet/readline/rluserman.html#Readline-Init-File)
in the GNU Readline manual for information about the format and
allowable constructs of that file, and the capabilities of the
Readline library in general.

Note

The underlying Readline library API may be implemented by
the `editline` (`libedit`) library instead of GNU readline.
On macOS the [`readline`](#module-readline "readline: GNU readline support for Python. (Unix)") module detects which library is being used
at run time.

The configuration file for `editline` is different from that
of GNU readline. If you programmatically load configuration strings
you can use [`backend`](#readline.backend "readline.backend") to determine which library is being used.

If you use `editline`/`libedit` readline emulation on macOS, the
initialization file located in your home directory is named
`.editrc`. For example, the following content in `~/.editrc` will
turn ON *vi* keybindings and TAB completion:

Copy

```
python:bind -v
python:bind ^I rl_complete

```

Also note that different libraries may use different history file formats.
When switching the underlying library, existing history files may become
unusable.

readline.backend
:   The name of the underlying Readline library being used, either
    `"readline"` or `"editline"`.

Init file
---------

The following functions relate to the init file and user configuration:

readline.parse\_and\_bind(*string*)
:   Execute the init line provided in the *string* argument. This calls
    `rl_parse_and_bind()` in the underlying library.

readline.read\_init\_file([*filename*])
:   Execute a readline initialization file. The default filename is the last filename
    used. This calls `rl_read_init_file()` in the underlying library.

Line buffer
-----------

The following functions operate on the line buffer:

readline.get\_line\_buffer()
:   Return the current contents of the line buffer (`rl_line_buffer`
    in the underlying library).

readline.insert\_text(*string*)
:   Insert text into the line buffer at the cursor position. This calls
    `rl_insert_text()` in the underlying library, but ignores
    the return value.

readline.redisplay()
:   Change what’s displayed on the screen to reflect the current contents of the
    line buffer. This calls `rl_redisplay()` in the underlying library.

History file
------------

The following functions operate on a history file:

readline.read\_history\_file([*filename*])
:   Load a readline history file, and append it to the history list.
    The default filename is `~/.history`. This calls
    `read_history()` in the underlying library.

readline.write\_history\_file([*filename*])
:   Save the history list to a readline history file, overwriting any
    existing file. The default filename is `~/.history`. This calls
    `write_history()` in the underlying library.

readline.append\_history\_file(*nelements*[, *filename*])
:   Append the last *nelements* items of history to a file. The default filename is
    `~/.history`. The file must already exist. This calls
    `append_history()` in the underlying library. This function
    only exists if Python was compiled for a version of the library
    that supports it.

readline.get\_history\_length()

readline.set\_history\_length(*length*)
:   Set or return the desired number of lines to save in the history file.
    The [`write_history_file()`](#readline.write_history_file "readline.write_history_file") function uses this value to truncate
    the history file, by calling `history_truncate_file()` in
    the underlying library. Negative values imply
    unlimited history file size.

History list
------------

The following functions operate on a global history list:

readline.clear\_history()
:   Clear the current history. This calls `clear_history()` in the
    underlying library. The Python function only exists if Python was
    compiled for a version of the library that supports it.

readline.get\_current\_history\_length()
:   Return the number of items currently in the history. (This is different from
    [`get_history_length()`](#readline.get_history_length "readline.get_history_length"), which returns the maximum number of lines that will
    be written to a history file.)

readline.get\_history\_item(*index*)
:   Return the current contents of history item at *index*. The item index
    is one-based. This calls `history_get()` in the underlying library.

readline.remove\_history\_item(*pos*)
:   Remove history item specified by its position from the history.
    The position is zero-based. This calls `remove_history()` in
    the underlying library.

readline.replace\_history\_item(*pos*, *line*)
:   Replace history item specified by its position with *line*.
    The position is zero-based. This calls `replace_history_entry()`
    in the underlying library.

readline.add\_history(*line*)
:   Append *line* to the history buffer, as if it was the last line typed.
    This calls `add_history()` in the underlying library.

readline.set\_auto\_history(*enabled*)
:   Enable or disable automatic calls to `add_history()` when reading
    input via readline. The *enabled* argument should be a Boolean value
    that when true, enables auto history, and that when false, disables
    auto history.

    **CPython implementation detail:** Auto history is enabled by default, and changes to this do not persist
    across multiple sessions.

Startup hooks
-------------

readline.set\_startup\_hook([*function*])
:   Set or remove the function invoked by the `rl_startup_hook`
    callback of the underlying library. If *function* is specified, it will
    be used as the new hook function; if omitted or `None`, any function
    already installed is removed. The hook is called with no
    arguments just before readline prints the first prompt.

readline.set\_pre\_input\_hook([*function*])
:   Set or remove the function invoked by the `rl_pre_input_hook`
    callback of the underlying library. If *function* is specified, it will
    be used as the new hook function; if omitted or `None`, any
    function already installed is removed. The hook is called
    with no arguments after the first prompt has been printed and just before
    readline starts reading input characters. This function only exists
    if Python was compiled for a version of the library that supports it.

Completion
----------

The following functions relate to implementing a custom word completion
function. This is typically operated by the Tab key, and can suggest and
automatically complete a word being typed. By default, Readline is set up
to be used by [`rlcompleter`](rlcompleter.html#module-rlcompleter "rlcompleter: Python identifier completion, suitable for the GNU readline library.") to complete Python identifiers for
the interactive interpreter. If the [`readline`](#module-readline "readline: GNU readline support for Python. (Unix)") module is to be used
with a custom completer, a different set of word delimiters should be set.

readline.set\_completer([*function*])
:   Set or remove the completer function. If *function* is specified, it will be
    used as the new completer function; if omitted or `None`, any completer
    function already installed is removed. The completer function is called as
    `function(text, state)`, for *state* in `0`, `1`, `2`, …, until it
    returns a non-string value. It should return the next possible completion
    starting with *text*.

    The installed completer function is invoked by the *entry\_func* callback
    passed to `rl_completion_matches()` in the underlying library.
    The *text* string comes from the first parameter to the
    `rl_attempted_completion_function` callback of the
    underlying library.

readline.get\_completer()
:   Get the completer function, or `None` if no completer function has been set.

readline.get\_completion\_type()
:   Get the type of completion being attempted. This returns the
    `rl_completion_type` variable in the underlying library as
    an integer.

readline.get\_begidx()

readline.get\_endidx()
:   Get the beginning or ending index of the completion scope.
    These indexes are the *start* and *end* arguments passed to the
    `rl_attempted_completion_function` callback of the
    underlying library. The values may be different in the same
    input editing scenario based on the underlying C readline implementation.
    Ex: libedit is known to behave differently than libreadline.

readline.set\_completer\_delims(*string*)

readline.get\_completer\_delims()
:   Set or get the word delimiters for completion. These determine the
    start of the word to be considered for completion (the completion scope).
    These functions access the `rl_completer_word_break_characters`
    variable in the underlying library.

readline.set\_completion\_display\_matches\_hook([*function*])
:   Set or remove the completion display function. If *function* is
    specified, it will be used as the new completion display function;
    if omitted or `None`, any completion display function already
    installed is removed. This sets or clears the
    `rl_completion_display_matches_hook` callback in the
    underlying library. The completion display function is called as
    `function(substitution, [matches], longest_match_length)` once
    each time matches need to be displayed.

Example
-------

The following example demonstrates how to use the [`readline`](#module-readline "readline: GNU readline support for Python. (Unix)") module’s
history reading and writing functions to automatically load and save a history
file named `.python_history` from the user’s home directory. The code
below would normally be executed automatically during interactive sessions
from the user’s [`PYTHONSTARTUP`](../using/cmdline.html#envvar-PYTHONSTARTUP) file.

Copy

```
import atexit
import os
import readline

histfile = os.path.join(os.path.expanduser("~"), ".python_history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

```

This code is actually automatically run when Python is run in
[interactive mode](../tutorial/interpreter.html#tut-interactive) (see [Readline configuration](site.html#rlcompleter-config)).

The following example achieves the same goal but supports concurrent interactive
sessions, by only appending the new history.

Copy

```
import atexit
import os
import readline
histfile = os.path.join(os.path.expanduser("~"), ".python_history")

try:
    readline.read_history_file(histfile)
    h_len = readline.get_current_history_length()
except FileNotFoundError:
    open(histfile, 'wb').close()
    h_len = 0

def save(prev_h_len, histfile):
    new_h_len = readline.get_current_history_length()
    readline.set_history_length(1000)
    readline.append_history_file(new_h_len - prev_h_len, histfile)
atexit.register(save, h_len, histfile)

```

The following example extends the [`code.InteractiveConsole`](code.html#code.InteractiveConsole "code.InteractiveConsole") class to
support history save/restore.

Copy

```
import atexit
import code
import os
import readline

class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.set_history_length(1000)
        readline.write_history_file(histfile)

```