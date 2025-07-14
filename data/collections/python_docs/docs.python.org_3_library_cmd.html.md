:   Repeatedly issue a prompt, accept input, parse an initial prefix off the
    received input, and dispatch to action methods, passing them the remainder of
    the line as argument.

    The optional argument is a banner or intro string to be issued before the first
    prompt (this overrides the [`intro`](#cmd.Cmd.intro "cmd.Cmd.intro") class attribute).

    If the [`readline`](readline.html#module-readline "readline: GNU readline support for Python. (Unix)") module is loaded, input will automatically inherit
    **bash**-like history-list editing (e.g. `Control`-`P` scrolls back
    to the last command, `Control`-`N` forward to the next one, `Control`-`F`
    moves the cursor to the right non-destructively, `Control`-`B` moves the
    cursor to the left non-destructively, etc.).

    An end-of-file on input is passed back as the string `'EOF'`.

    An interpreter instance will recognize a command name `foo` if and only if it
    has a method `do_foo()`. As a special case, a line beginning with the
    character `'?'` is dispatched to the method [`do_help()`](#cmd.Cmd.do_help "cmd.Cmd.do_help"). As another
    special case, a line beginning with the character `'!'` is dispatched to the
    method `do_shell()` (if such a method is defined).

    This method will return when the [`postcmd()`](#cmd.Cmd.postcmd "cmd.Cmd.postcmd") method returns a true value.
    The *stop* argument to [`postcmd()`](#cmd.Cmd.postcmd "cmd.Cmd.postcmd") is the return value from the command’s
    corresponding `do_*()` method.

    If completion is enabled, completing commands will be done automatically, and
    completing of commands args is done by calling `complete_foo()` with
    arguments *text*, *line*, *begidx*, and *endidx*. *text* is the string prefix
    we are attempting to match: all returned matches must begin with it. *line* is
    the current input line with leading whitespace removed, *begidx* and *endidx*
    are the beginning and ending indexes of the prefix text, which could be used to
    provide different completion depending upon which position the argument is in.