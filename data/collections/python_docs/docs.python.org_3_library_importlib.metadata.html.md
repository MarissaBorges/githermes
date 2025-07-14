This package provides the following functionality via its public API.

### Entry points

importlib.metadata.entry\_points(*\*\*select\_params*)
:   Returns a [`EntryPoints`](#importlib.metadata.EntryPoints "importlib.metadata.EntryPoints") instance describing entry points for the
    current environment. Any given keyword parameters are passed to the
    `select()` method for comparison to the attributes of
    the individual entry point definitions.

    Note: it is not currently possible to query for entry points based on
    their `EntryPoint.dist` attribute (as different `Distribution`
    instances do not currently compare equal, even if they have the same attributes)

*class* importlib.metadata.EntryPoints
:   Details of a collection of installed entry points.

    Also provides a `.groups` attribute that reports all identified entry
    point groups, and a `.names` attribute that reports all identified entry
    point names.

*class* importlib.metadata.EntryPoint
:   Details of an installed entry point.

    Each `EntryPoint` instance has `.name`, `.group`, and `.value`
    attributes and a `.load()` method to resolve the value. There are also
    `.module`, `.attr`, and `.extras` attributes for getting the
    components of the `.value` attribute, and `.dist` for obtaining
    information regarding the distribution package that provides the entry point.

Query all entry points:

Copy

```
>>> eps = entry_points()

```

The `entry_points()` function returns a `EntryPoints` object,
a collection of all `EntryPoint` objects with `names` and `groups`
attributes for convenience:

Copy

```
>>> sorted(eps.groups)
['console_scripts', 'distutils.commands', 'distutils.setup_keywords', 'egg_info.writers', 'setuptools.installation']

```

`EntryPoints` has a `select()` method to select entry points
matching specific properties. Select entry points in the
`console_scripts` group:

Copy

```
>>> scripts = eps.select(group='console_scripts')

```

Equivalently, since `entry_points()` passes keyword arguments
through to select:

Copy

```
>>> scripts = entry_points(group='console_scripts')

```

Pick out a specific script named “wheel” (found in the wheel project):

Copy

```
>>> 'wheel' in scripts.names
True
>>> wheel = scripts['wheel']

```

Equivalently, query for that entry point during selection:

Copy

```
>>> (wheel,) = entry_points(group='console_scripts', name='wheel')
>>> (wheel,) = entry_points().select(group='console_scripts', name='wheel')

```

Inspect the resolved entry point:

Copy

```
>>> wheel
EntryPoint(name='wheel', value='wheel.cli:main', group='console_scripts')
>>> wheel.module
'wheel.cli'
>>> wheel.attr
'main'
>>> wheel.extras
[]
>>> main = wheel.load()
>>> main
<function main at 0x103528488>

```

The `group` and `name` are arbitrary values defined by the package author
and usually a client will wish to resolve all entry points for a particular
group. Read [the setuptools docs](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
for more information on entry points, their definition, and usage.

Changed in version 3.12: The “selectable” entry points were introduced in `importlib_metadata`
3.6 and Python 3.10. Prior to those changes, `entry_points` accepted
no parameters and always returned a dictionary of entry points, keyed
by group. With `importlib_metadata` 5.0 and Python 3.12,
`entry_points` always returns an `EntryPoints` object. See
[backports.entry\_points\_selectable](https://pypi.org/project/backports.entry_points_selectable/)
for compatibility options.

Changed in version 3.13: `EntryPoint` objects no longer present a tuple-like interface
([`__getitem__()`](../reference/datamodel.html#object.__getitem__ "object.__getitem__")).

### Distribution files

importlib.metadata.files(*distribution\_name*)
:   Return the full set of files contained within the named
    distribution package.

    Raises [`PackageNotFoundError`](#importlib.metadata.PackageNotFoundError "importlib.metadata.PackageNotFoundError") if the named distribution
    package is not installed in the current Python environment.

    Returns [`None`](constants.html#None "None") if the distribution is found but the installation
    database records reporting the files associated with the distribuion package
    are missing.

*class* importlib.metadata.PackagePath
:   A [`pathlib.PurePath`](pathlib.html#pathlib.PurePath "pathlib.PurePath") derived object with additional `dist`,
    `size`, and `hash` properties corresponding to the distribution
    package’s installation metadata for that file.

The `files()` function takes a
[Distribution Package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)
name and returns all of the files installed by this distribution. Each file is reported
as a [`PackagePath`](#importlib.metadata.PackagePath "importlib.metadata.PackagePath") instance. For example:

Copy

```
>>> util = [p for p in files('wheel') if 'util.py' in str(p)][0]
>>> util
PackagePath('wheel/util.py')
>>> util.size
859
>>> util.dist
<importlib.metadata._hooks.PathDistribution object at 0x101e0cef0>
>>> util.hash
<FileHash mode: sha256 value: bYkw5oMccfazVCoYQwKkkemoVyMAFoR34mmKBx8R1NI>

```

Once you have the file, you can also read its contents:

Copy

```
>>> print(util.read_text())
import base64
import sys
...
def as_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s

```

You can also use the `locate()` method to get the absolute
path to the file:

Copy

```
>>> util.locate()
PosixPath('/home/gustav/example/lib/site-packages/wheel/util.py')

```

In the case where the metadata file listing files
(`RECORD` or `SOURCES.txt`) is missing, `files()` will
return [`None`](constants.html#None "None"). The caller may wish to wrap calls to
`files()` in [always\_iterable](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.always_iterable)
or otherwise guard against this condition if the target
distribution is not known to have the metadata present.