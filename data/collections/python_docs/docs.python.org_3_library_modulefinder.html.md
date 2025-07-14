`modulefinder` — Find modules used by a script
==============================================

**Source code:** [Lib/modulefinder.py](https://github.com/python/cpython/tree/3.13/Lib/modulefinder.py)

---

This module provides a [`ModuleFinder`](#modulefinder.ModuleFinder "modulefinder.ModuleFinder") class that can be used to determine
the set of modules imported by a script. `modulefinder.py` can also be run as
a script, giving the filename of a Python script as its argument, after which a
report of the imported modules will be printed.

modulefinder.AddPackagePath(*pkg\_name*, *path*)
:   Record that the package named *pkg\_name* can be found in the specified *path*.

modulefinder.ReplacePackage(*oldname*, *newname*)
:   Allows specifying that the module named *oldname* is in fact the package named
    *newname*.

*class* modulefinder.ModuleFinder(*path=None*, *debug=0*, *excludes=[]*, *replace\_paths=[]*)
:   This class provides [`run_script()`](#modulefinder.ModuleFinder.run_script "modulefinder.ModuleFinder.run_script") and [`report()`](#modulefinder.ModuleFinder.report "modulefinder.ModuleFinder.report") methods to determine
    the set of modules imported by a script. *path* can be a list of directories to
    search for modules; if not specified, `sys.path` is used. *debug* sets the
    debugging level; higher values make the class print debugging messages about
    what it’s doing. *excludes* is a list of module names to exclude from the
    analysis. *replace\_paths* is a list of `(oldpath, newpath)` tuples that will
    be replaced in module paths.

    report()
    :   Print a report to standard output that lists the modules imported by the
        script and their paths, as well as modules that are missing or seem to be
        missing.

    run\_script(*pathname*)
    :   Analyze the contents of the *pathname* file, which must contain Python
        code.

    modules
    :   A dictionary mapping module names to modules. See
        [Example usage of ModuleFinder](#modulefinder-example).

The script that is going to get analyzed later on (bacon.py):

Copy

```
import re, itertools

try:
    import baconhameggs
except ImportError:
    pass

try:
    import guido.python.ham
except ImportError:
    pass

```

The script that will output the report of bacon.py:

Copy

```
from modulefinder import ModuleFinder

finder = ModuleFinder()
finder.run_script('bacon.py')

print('Loaded modules:')
for name, mod in finder.modules.items():
    print('%s: ' % name, end='')
    print(','.join(list(mod.globalnames.keys())[:3]))

print('-'*50)
print('Modules not imported:')
print('\n'.join(finder.badmodules.keys()))

```

Sample output (may vary depending on the architecture):

Copy

```
Loaded modules:
_types:
copyreg:  _inverted_registry,_slotnames,__all__
re._compiler:  isstring,_sre,_optimize_unicode
_sre:
re._constants:  REPEAT_ONE,makedict,AT_END_LINE
sys:
re:  __module__,finditer,_expand
itertools:
__main__:  re,itertools,baconhameggs
re._parser:  _PATTERNENDERS,SRE_FLAG_UNICODE
array:
types:  __module__,IntType,TypeType
---------------------------------------------------
Modules not imported:
guido.python.ham
baconhameggs

```