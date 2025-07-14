:   The [`Bdb`](#bdb.Bdb "bdb.Bdb") class acts as a generic Python debugger base class.

    This class takes care of the details of the trace facility; a derived class
    should implement user interaction. The standard debugger class
    ([`pdb.Pdb`](pdb.html#pdb.Pdb "pdb.Pdb")) is an example.

    The *skip* argument, if given, must be an iterable of glob-style
    module name patterns. The debugger will not step into frames that
    originate in a module that matches one of these patterns. Whether a
    frame is considered to originate in a certain module is determined
    by the `__name__` in the frame globals.

    Changed in version 3.1: Added the *skip* parameter.

    The following methods of [`Bdb`](#bdb.Bdb "bdb.Bdb") normally don’t need to be overridden.

    canonic(*filename*)
    :   Return canonical form of *filename*.

        For real file names, the canonical form is an operating-system-dependent,
        [`case-normalized`](os.path.html#os.path.normcase "os.path.normcase") [`absolute path`](os.path.html#os.path.abspath "os.path.abspath"). A *filename* with angle brackets, such as `"<stdin>"`
        generated in interactive mode, is returned unchanged.

    reset()
    :   Set the `botframe`, `stopframe`, `returnframe` and
        [`quitting`](#bdb.Bdb.set_quit "bdb.Bdb.set_quit") attributes with values ready to start debugging.

    trace\_dispatch(*frame*, *event*, *arg*)
    :   This function is installed as the trace function of debugged frames. Its
        return value is the new trace function (in most cases, that is, itself).

        The default implementation decides how to dispatch a frame, depending on
        the type of event (passed as a string) that is about to be executed.
        *event* can be one of the following:

        * `"line"`: A new line of code is going to be executed.
        * `"call"`: A function is about to be called, or another code block
          entered.
        * `"return"`: A function or other code block is about to return.
        * `"exception"`: An exception has occurred.
        * `"c_call"`: A C function is about to be called.
        * `"c_return"`: A C function has returned.
        * `"c_exception"`: A C function has raised an exception.

        For the Python events, specialized functions (see below) are called. For
        the C events, no action is taken.

        The *arg* parameter depends on the previous event.

        See the documentation for [`sys.settrace()`](sys.html#sys.settrace "sys.settrace") for more information on the
        trace function. For more information on code and frame objects, refer to
        [The standard type hierarchy](../reference/datamodel.html#types).

    dispatch\_line(*frame*)
    :   If the debugger should stop on the current line, invoke the
        [`user_line()`](#bdb.Bdb.user_line "bdb.Bdb.user_line") method (which should be overridden in subclasses).
        Raise a [`BdbQuit`](#bdb.BdbQuit "bdb.BdbQuit") exception if the [`quitting`](#bdb.Bdb.set_quit "bdb.Bdb.set_quit") flag is set
        (which can be set from [`user_line()`](#bdb.Bdb.user_line "bdb.Bdb.user_line")). Return a reference to the
        [`trace_dispatch()`](#bdb.Bdb.trace_dispatch "bdb.Bdb.trace_dispatch") method for further tracing in that scope.

    dispatch\_call(*frame*, *arg*)
    :   If the debugger should stop on this function call, invoke the
        [`user_call()`](#bdb.Bdb.user_call "bdb.Bdb.user_call") method (which should be overridden in subclasses).
        Raise a [`BdbQuit`](#bdb.BdbQuit "bdb.BdbQuit") exception if the [`quitting`](#bdb.Bdb.set_quit "bdb.Bdb.set_quit") flag is set
        (which can be set from [`user_call()`](#bdb.Bdb.user_call "bdb.Bdb.user_call")). Return a reference to the
        [`trace_dispatch()`](#bdb.Bdb.trace_dispatch "bdb.Bdb.trace_dispatch") method for further tracing in that scope.

    dispatch\_return(*frame*, *arg*)
    :   If the debugger should stop on this function return, invoke the
        [`user_return()`](#bdb.Bdb.user_return "bdb.Bdb.user_return") method (which should be overridden in subclasses).
        Raise a [`BdbQuit`](#bdb.BdbQuit "bdb.BdbQuit") exception if the [`quitting`](#bdb.Bdb.set_quit "bdb.Bdb.set_quit") flag is set
        (which can be set from [`user_return()`](#bdb.Bdb.user_return "bdb.Bdb.user_return")). Return a reference to the
        [`trace_dispatch()`](#bdb.Bdb.trace_dispatch "bdb.Bdb.trace_dispatch") method for further tracing in that scope.

    dispatch\_exception(*frame*, *arg*)
    :   If the debugger should stop at this exception, invokes the
        [`user_exception()`](#bdb.Bdb.user_exception "bdb.Bdb.user_exception") method (which should be overridden in subclasses).
        Raise a [`BdbQuit`](#bdb.BdbQuit "bdb.BdbQuit") exception if the [`quitting`](#bdb.Bdb.set_quit "bdb.Bdb.set_quit") flag is set
        (which can be set from [`user_exception()`](#bdb.Bdb.user_exception "bdb.Bdb.user_exception")). Return a reference to the
        [`trace_dispatch()`](#bdb.Bdb.trace_dispatch "bdb.Bdb.trace_dispatch") method for further tracing in that scope.

    Normally derived classes don’t override the following methods, but they may
    if they want to redefine the definition of stopping and breakpoints.

    is\_skipped\_line(*module\_name*)
    :   Return `True` if *module\_name* matches any skip pattern.

    stop\_here(*frame*)
    :   Return `True` if *frame* is below the starting frame in the stack.

    break\_here(*frame*)
    :   Return `True` if there is an effective breakpoint for this line.

        Check whether a line or function breakpoint exists and is in effect. Delete temporary
        breakpoints based on information from [`effective()`](#bdb.effective "bdb.effective").

    break\_anywhere(*frame*)
    :   Return `True` if any breakpoint exists for *frame*’s filename.

    Derived classes should override these methods to gain control over debugger
    operation.

    user\_call(*frame*, *argument\_list*)
    :   Called from [`dispatch_call()`](#bdb.Bdb.dispatch_call "bdb.Bdb.dispatch_call") if a break might stop inside the
        called function.

        *argument\_list* is not used anymore and will always be `None`.
        The argument is kept for backwards compatibility.

    user\_line(*frame*)
    :   Called from [`dispatch_line()`](#bdb.Bdb.dispatch_line "bdb.Bdb.dispatch_line") when either [`stop_here()`](#bdb.Bdb.stop_here "bdb.Bdb.stop_here") or
        [`break_here()`](#bdb.Bdb.break_here "bdb.Bdb.break_here") returns `True`.

    user\_return(*frame*, *return\_value*)
    :   Called from [`dispatch_return()`](#bdb.Bdb.dispatch_return "bdb.Bdb.dispatch_return") when [`stop_here()`](#bdb.Bdb.stop_here "bdb.Bdb.stop_here") returns `True`.

    user\_exception(*frame*, *exc\_info*)
    :   Called from [`dispatch_exception()`](#bdb.Bdb.dispatch_exception "bdb.Bdb.dispatch_exception") when [`stop_here()`](#bdb.Bdb.stop_here "bdb.Bdb.stop_here")
        returns `True`.

    do\_clear(*arg*)
    :   Handle how a breakpoint must be removed when it is a temporary one.

        This method must be implemented by derived classes.

    Derived classes and clients can call the following methods to affect the
    stepping state.

    set\_step()
    :   Stop after one line of code.

    set\_next(*frame*)
    :   Stop on the next line in or below the given frame.

    set\_return(*frame*)
    :   Stop when returning from the given frame.

    set\_until(*frame*, *lineno=None*)
    :   Stop when the line with the *lineno* greater than the current one is
        reached or when returning from current frame.

    set\_trace([*frame*])
    :   Start debugging from *frame*. If *frame* is not specified, debugging
        starts from caller’s frame.

        Changed in version 3.13: [`set_trace()`](#bdb.set_trace "bdb.set_trace") will enter the debugger immediately, rather than
        on the next line of code to be executed.

    set\_continue()
    :   Stop only at breakpoints or when finished. If there are no breakpoints,
        set the system trace function to `None`.

    set\_quit()
    :   Set the `quitting` attribute to `True`. This raises [`BdbQuit`](#bdb.BdbQuit "bdb.BdbQuit") in
        the next call to one of the `dispatch_*()` methods.

    Derived classes and clients can call the following methods to manipulate
    breakpoints. These methods return a string containing an error message if
    something went wrong, or `None` if all is well.

    set\_break(*filename*, *lineno*, *temporary=False*, *cond=None*, *funcname=None*)
    :   Set a new breakpoint. If the *lineno* line doesn’t exist for the
        *filename* passed as argument, return an error message. The *filename*
        should be in canonical form, as described in the [`canonic()`](#bdb.Bdb.canonic "bdb.Bdb.canonic") method.

    clear\_break(*filename*, *lineno*)
    :   Delete the breakpoints in *filename* and *lineno*. If none were set,
        return an error message.

    clear\_bpbynumber(*arg*)
    :   Delete the breakpoint which has the index *arg* in the
        [`Breakpoint.bpbynumber`](#bdb.Breakpoint.bpbynumber "bdb.Breakpoint.bpbynumber"). If *arg* is not numeric or out of range,
        return an error message.

    clear\_all\_file\_breaks(*filename*)
    :   Delete all breakpoints in *filename*. If none were set, return an error
        message.

    clear\_all\_breaks()
    :   Delete all existing breakpoints. If none were set, return an error
        message.

    get\_bpbynumber(*arg*)
    :   Return a breakpoint specified by the given number. If *arg* is a string,
        it will be converted to a number. If *arg* is a non-numeric string, if
        the given breakpoint never existed or has been deleted, a
        [`ValueError`](exceptions.html#ValueError "ValueError") is raised.

    get\_break(*filename*, *lineno*)
    :   Return `True` if there is a breakpoint for *lineno* in *filename*.

    get\_breaks(*filename*, *lineno*)
    :   Return all breakpoints for *lineno* in *filename*, or an empty list if
        none are set.

    get\_file\_breaks(*filename*)
    :   Return all breakpoints in *filename*, or an empty list if none are set.

    get\_all\_breaks()
    :   Return all breakpoints that are set.

    Derived classes and clients can call the following methods to get a data
    structure representing a stack trace.

    get\_stack(*f*, *t*)
    :   Return a list of (frame, lineno) tuples in a stack trace, and a size.

        The most recently called frame is last in the list. The size is the number
        of frames below the frame where the debugger was invoked.

    format\_stack\_entry(*frame\_lineno*, *lprefix=': '*)
    :   Return a string with information about a stack entry, which is a
        `(frame, lineno)` tuple. The return string contains:

        * The canonical filename which contains the frame.
        * The function name or `"<lambda>"`.
        * The input arguments.
        * The return value.
        * The line of code (if it exists).

    The following two methods can be called by clients to use a debugger to debug
    a [statement](../glossary.html#term-statement), given as a string.

    run(*cmd*, *globals=None*, *locals=None*)
    :   Debug a statement executed via the [`exec()`](functions.html#exec "exec") function. *globals*
        defaults to `__main__.__dict__`, *locals* defaults to *globals*.

    runeval(*expr*, *globals=None*, *locals=None*)
    :   Debug an expression executed via the [`eval()`](functions.html#eval "eval") function. *globals* and
        *locals* have the same meaning as in [`run()`](#bdb.Bdb.run "bdb.Bdb.run").

    runctx(*cmd*, *globals*, *locals*)
    :   For backwards compatibility. Calls the [`run()`](#bdb.Bdb.run "bdb.Bdb.run") method.

    runcall(*func*, */*, *\*args*, *\*\*kwds*)
    :   Debug a single function call, and return its result.