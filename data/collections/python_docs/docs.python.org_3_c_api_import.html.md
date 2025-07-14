:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable).*

    Given a module name (possibly of the form `package.module`) and a code object
    read from a Python bytecode file or obtained from the built-in function
    [`compile()`](../library/functions.html#compile "compile"), load the module. Return a new reference to the module object,
    or `NULL` with an exception set if an error occurred. *name*
    is removed from [`sys.modules`](../library/sys.html#sys.modules "sys.modules") in error cases, even if *name* was already
    in [`sys.modules`](../library/sys.html#sys.modules "sys.modules") on entry to [`PyImport_ExecCodeModule()`](#c.PyImport_ExecCodeModule "PyImport_ExecCodeModule"). Leaving
    incompletely initialized modules in [`sys.modules`](../library/sys.html#sys.modules "sys.modules") is dangerous, as imports of
    such modules have no way to know that the module object is an unknown (and
    probably damaged with respect to the module author’s intents) state.

    The module’s [`__spec__`](../reference/datamodel.html#module.__spec__ "module.__spec__") and [`__loader__`](../reference/datamodel.html#module.__loader__ "module.__loader__") will be
    set, if not set already, with the appropriate values. The spec’s loader
    will be set to the module’s `__loader__` (if set) and to an instance
    of [`SourceFileLoader`](../library/importlib.html#importlib.machinery.SourceFileLoader "importlib.machinery.SourceFileLoader") otherwise.

    The module’s [`__file__`](../reference/datamodel.html#module.__file__ "module.__file__") attribute will be set to the code
    object’s [`co_filename`](../reference/datamodel.html#codeobject.co_filename "codeobject.co_filename"). If applicable,
    [`__cached__`](../reference/datamodel.html#module.__cached__ "module.__cached__") will also be set.

    This function will reload the module if it was already imported. See
    [`PyImport_ReloadModule()`](#c.PyImport_ReloadModule "PyImport_ReloadModule") for the intended way to reload a module.

    If *name* points to a dotted name of the form `package.module`, any package
    structures not already created will still not be created.

    See also [`PyImport_ExecCodeModuleEx()`](#c.PyImport_ExecCodeModuleEx "PyImport_ExecCodeModuleEx") and
    [`PyImport_ExecCodeModuleWithPathnames()`](#c.PyImport_ExecCodeModuleWithPathnames "PyImport_ExecCodeModuleWithPathnames").