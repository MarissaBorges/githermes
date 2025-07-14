:   Warning control. Python’s warning machinery by default prints warning
    messages to [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr").

    The simplest settings apply a particular action unconditionally to all
    warnings emitted by a process (even those that are otherwise ignored by
    default):

    ```
    -Wdefault  # Warn once per call location
    -Werror    # Convert to exceptions
    -Walways   # Warn every time
    -Wall      # Same as -Walways
    -Wmodule   # Warn once per calling module
    -Wonce     # Warn once per Python process
    -Wignore   # Never warn

    ```

    The action names can be abbreviated as desired and the interpreter will
    resolve them to the appropriate action name. For example, `-Wi` is the
    same as `-Wignore`.

    The full form of argument is:

    ```
    action:message:category:module:lineno

    ```

    Empty fields match all values; trailing empty fields may be omitted. For
    example `-W ignore::DeprecationWarning` ignores all DeprecationWarning
    warnings.

    The *action* field is as explained above but only applies to warnings that
    match the remaining fields.

    The *message* field must match the whole warning message; this match is
    case-insensitive.

    The *category* field matches the warning category
    (ex: `DeprecationWarning`). This must be a class name; the match test
    whether the actual warning category of the message is a subclass of the
    specified warning category.

    The *module* field matches the (fully qualified) module name; this match is
    case-sensitive.

    The *lineno* field matches the line number, where zero matches all line
    numbers and is thus equivalent to an omitted line number.

    Multiple [`-W`](#cmdoption-W) options can be given; when a warning matches more than
    one option, the action for the last matching option is performed. Invalid
    [`-W`](#cmdoption-W) options are ignored (though, a warning message is printed about
    invalid options when the first warning is issued).

    Warnings can also be controlled using the [`PYTHONWARNINGS`](#envvar-PYTHONWARNINGS)
    environment variable and from within a Python program using the
    [`warnings`](../library/warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module. For example, the [`warnings.filterwarnings()`](../library/warnings.html#warnings.filterwarnings "warnings.filterwarnings")
    function can be used to use a regular expression on the warning message.

    See [The Warnings Filter](../library/warnings.html#warning-filter) and [Describing Warning Filters](../library/warnings.html#describing-warning-filters) for more
    details.