|  |  |  |
| --- | --- | --- |
| class | \_\_doc\_\_ | documentation string |
|  | \_\_name\_\_ | name with which this class was defined |
|  | \_\_qualname\_\_ | qualified name |
|  | \_\_module\_\_ | name of module in which this class was defined |
|  | \_\_type\_params\_\_ | A tuple containing the [type parameters](../reference/compound_stmts.html#type-params) of a generic class |
| method | \_\_doc\_\_ | documentation string |
|  | \_\_name\_\_ | name with which this method was defined |
|  | \_\_qualname\_\_ | qualified name |
|  | \_\_func\_\_ | function object containing implementation of method |
|  | \_\_self\_\_ | instance to which this method is bound, or `None` |
|  | \_\_module\_\_ | name of module in which this method was defined |
| function | \_\_doc\_\_ | documentation string |
|  | \_\_name\_\_ | name with which this function was defined |
|  | \_\_qualname\_\_ | qualified name |
|  | \_\_code\_\_ | code object containing compiled function [bytecode](../glossary.html#term-bytecode) |
|  | \_\_defaults\_\_ | tuple of any default values for positional or keyword parameters |
|  | \_\_kwdefaults\_\_ | mapping of any default values for keyword-only parameters |
|  | \_\_globals\_\_ | global namespace in which this function was defined |
|  | \_\_builtins\_\_ | builtins namespace |
|  | \_\_annotations\_\_ | mapping of parameters names to annotations; `"return"` key is reserved for return annotations. |
|  | \_\_type\_params\_\_ | A tuple containing the [type parameters](../reference/compound_stmts.html#type-params) of a generic function |
|  | \_\_module\_\_ | name of module in which this function was defined |
| traceback | tb\_frame | frame object at this level |
|  | tb\_lasti | index of last attempted instruction in bytecode |
|  | tb\_lineno | current line number in Python source code |
|  | tb\_next | next inner traceback object (called by this level) |
| frame | f\_back | next outer frame object (this frame’s caller) |
|  | f\_builtins | builtins namespace seen by this frame |
|  | f\_code | code object being executed in this frame |
|  | f\_globals | global namespace seen by this frame |
|  | f\_lasti | index of last attempted instruction in bytecode |
|  | f\_lineno | current line number in Python source code |
|  | f\_locals | local namespace seen by this frame |
|  | f\_trace | tracing function for this frame, or `None` |
| code | co\_argcount | number of arguments (not including keyword only arguments, \* or \*\* args) |
|  | co\_code | string of raw compiled bytecode |
|  | co\_cellvars | tuple of names of cell variables (referenced by containing scopes) |
|  | co\_consts | tuple of constants used in the bytecode |
|  | co\_filename | name of file in which this code object was created |
|  | co\_firstlineno | number of first line in Python source code |
|  | co\_flags | bitmap of `CO_*` flags, read more [here](#inspect-module-co-flags) |
|  | co\_lnotab | encoded mapping of line numbers to bytecode indices |
|  | co\_freevars | tuple of names of free variables (referenced via a function’s closure) |
|  | co\_posonlyargcount | number of positional only arguments |
|  | co\_kwonlyargcount | number of keyword only arguments (not including \*\* arg) |
|  | co\_name | name with which this code object was defined |
|  | co\_qualname | fully qualified name with which this code object was defined |
|  | co\_names | tuple of names other than arguments and function locals |
|  | co\_nlocals | number of local variables |
|  | co\_stacksize | virtual machine stack space required |
|  | co\_varnames | tuple of names of arguments and local variables |
| generator | \_\_name\_\_ | name |
|  | \_\_qualname\_\_ | qualified name |
|  | gi\_frame | frame |
|  | gi\_running | is the generator running? |
|  | gi\_code | code |
|  | gi\_yieldfrom | object being iterated by `yield from`, or `None` |
| async generator | \_\_name\_\_ | name |
|  | \_\_qualname\_\_ | qualified name |
|  | ag\_await | object being awaited on, or `None` |
|  | ag\_frame | frame |
|  | ag\_running | is the generator running? |
|  | ag\_code | code |
| coroutine | \_\_name\_\_ | name |
|  | \_\_qualname\_\_ | qualified name |
|  | cr\_await | object being awaited on, or `None` |
|  | cr\_frame | frame |
|  | cr\_running | is the coroutine running? |
|  | cr\_code | code |
|  | cr\_origin | where coroutine was created, or `None`. See [`sys.set_coroutine_origin_tracking_depth()`](sys.html#sys.set_coroutine_origin_tracking_depth "sys.set_coroutine_origin_tracking_depth") |
| builtin | \_\_doc\_\_ | documentation string |
|  | \_\_name\_\_ | original name of this function or method |
|  | \_\_qualname\_\_ | qualified name |
|  | \_\_self\_\_ | instance to which a method is bound, or `None` |