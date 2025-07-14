ArgumentParser objects
----------------------

*class* argparse.ArgumentParser(*prog=None*, *usage=None*, *description=None*, *epilog=None*, *parents=[]*, *formatter\_class=argparse.HelpFormatter*, *prefix\_chars='-'*, *fromfile\_prefix\_chars=None*, *argument\_default=None*, *conflict\_handler='error'*, *add\_help=True*, *allow\_abbrev=True*, *exit\_on\_error=True*)
:   Create a new [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") object. All parameters should be passed
    as keyword arguments. Each parameter has its own more detailed description
    below, but in short they are:

    * [prog](#prog) - The name of the program (default:
      `os.path.basename(sys.argv[0])`)
    * [usage](#usage) - The string describing the program usage (default: generated from
      arguments added to parser)
    * [description](#description) - Text to display before the argument help
      (by default, no text)
    * [epilog](#epilog) - Text to display after the argument help (by default, no text)
    * [parents](#parents) - A list of [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects whose arguments should
      also be included
    * [formatter\_class](#formatter-class) - A class for customizing the help output
    * [prefix\_chars](#prefix-chars) - The set of characters that prefix optional arguments
      (default: ‘-‘)
    * [fromfile\_prefix\_chars](#fromfile-prefix-chars) - The set of characters that prefix files from
      which additional arguments should be read (default: `None`)
    * [argument\_default](#argument-default) - The global default value for arguments
      (default: `None`)
    * [conflict\_handler](#conflict-handler) - The strategy for resolving conflicting optionals
      (usually unnecessary)
    * [add\_help](#add-help) - Add a `-h/--help` option to the parser (default: `True`)
    * [allow\_abbrev](#allow-abbrev) - Allows long options to be abbreviated if the
      abbreviation is unambiguous. (default: `True`)
    * [exit\_on\_error](#exit-on-error) - Determines whether or not `ArgumentParser` exits with
      error info when an error occurs. (default: `True`)

    Changed in version 3.5: *allow\_abbrev* parameter was added.

    Changed in version 3.8: In previous versions, *allow\_abbrev* also disabled grouping of short
    flags such as `-vv` to mean `-v -v`.

    Changed in version 3.9: *exit\_on\_error* parameter was added.

The following sections describe how each of these are used.

### prog

By default, [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") calculates the name of the program
to display in help messages depending on the way the Python interpreter was run:

* The [`base name`](os.path.html#os.path.basename "os.path.basename") of `sys.argv[0]` if a file was
  passed as argument.
* The Python interpreter name followed by `sys.argv[0]` if a directory or
  a zipfile was passed as argument.
* The Python interpreter name followed by `-m` followed by the
  module or package name if the [`-m`](../using/cmdline.html#cmdoption-m) option was used.

This default is almost always desirable because it will make the help messages
match the string that was used to invoke the program on the command line.
However, to change this default behavior, another value can be supplied using
the `prog=` argument to [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"):

Copy

```
>>> parser = argparse.ArgumentParser(prog='myprogram')
>>> parser.print_help()
usage: myprogram [-h]

options:
 -h, --help  show this help message and exit

```

Note that the program name, whether determined from `sys.argv[0]` or from the
`prog=` argument, is available to help messages using the `%(prog)s` format
specifier.

Copy

```
>>> parser = argparse.ArgumentParser(prog='myprogram')
>>> parser.add_argument('--foo', help='foo of the %(prog)s program')
>>> parser.print_help()
usage: myprogram [-h] [--foo FOO]

options:
 -h, --help  show this help message and exit
 --foo FOO   foo of the myprogram program

```

### usage

By default, [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") calculates the usage message from the
arguments it contains. The default message can be overridden with the
`usage=` keyword argument:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
>>> parser.add_argument('--foo', nargs='?', help='foo help')
>>> parser.add_argument('bar', nargs='+', help='bar help')
>>> parser.print_help()
usage: PROG [options]

positional arguments:
 bar          bar help

options:
 -h, --help   show this help message and exit
 --foo [FOO]  foo help

```

The `%(prog)s` format specifier is available to fill in the program name in
your usage messages.

### description

Most calls to the [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") constructor will use the
`description=` keyword argument. This argument gives a brief description of
what the program does and how it works. In help messages, the description is
displayed between the command-line usage string and the help messages for the
various arguments.

By default, the description will be line-wrapped so that it fits within the
given space. To change this behavior, see the [formatter\_class](#formatter-class) argument.

### epilog

Some programs like to display additional description of the program after the
description of the arguments. Such text can be specified using the `epilog=`
argument to [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"):

Copy

```
>>> parser = argparse.ArgumentParser(
...     description='A foo that bars',
...     epilog="And that's how you'd foo a bar")
>>> parser.print_help()
usage: argparse.py [-h]

A foo that bars

options:
 -h, --help  show this help message and exit

And that's how you'd foo a bar

```

As with the [description](#description) argument, the `epilog=` text is by default
line-wrapped, but this behavior can be adjusted with the [formatter\_class](#formatter-class)
argument to [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser").

### parents

Sometimes, several parsers share a common set of arguments. Rather than
repeating the definitions of these arguments, a single parser with all the
shared arguments and passed to `parents=` argument to [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser")
can be used. The `parents=` argument takes a list of [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser")
objects, collects all the positional and optional actions from them, and adds
these actions to the [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") object being constructed:

Copy

```
>>> parent_parser = argparse.ArgumentParser(add_help=False)
>>> parent_parser.add_argument('--parent', type=int)

>>> foo_parser = argparse.ArgumentParser(parents=[parent_parser])
>>> foo_parser.add_argument('foo')
>>> foo_parser.parse_args(['--parent', '2', 'XXX'])
Namespace(foo='XXX', parent=2)

>>> bar_parser = argparse.ArgumentParser(parents=[parent_parser])
>>> bar_parser.add_argument('--bar')
>>> bar_parser.parse_args(['--bar', 'YYY'])
Namespace(bar='YYY', parent=None)

```

Note that most parent parsers will specify `add_help=False`. Otherwise, the
[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") will see two `-h/--help` options (one in the parent
and one in the child) and raise an error.

Note

You must fully initialize the parsers before passing them via `parents=`.
If you change the parent parsers after the child parser, those changes will
not be reflected in the child.

### formatter\_class

[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects allow the help formatting to be customized by
specifying an alternate formatting class. Currently, there are four such
classes:

*class* argparse.RawDescriptionHelpFormatter

*class* argparse.RawTextHelpFormatter

*class* argparse.ArgumentDefaultsHelpFormatter

*class* argparse.MetavarTypeHelpFormatter

[`RawDescriptionHelpFormatter`](#argparse.RawDescriptionHelpFormatter "argparse.RawDescriptionHelpFormatter") and [`RawTextHelpFormatter`](#argparse.RawTextHelpFormatter "argparse.RawTextHelpFormatter") give
more control over how textual descriptions are displayed.
By default, [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects line-wrap the [description](#description) and
[epilog](#epilog) texts in command-line help messages:

Copy

```
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     description='''this description
...         was indented weird
...             but that is okay''',
...     epilog='''
...             likewise for this epilog whose whitespace will
...         be cleaned up and whose words will be wrapped
...         across a couple lines''')
>>> parser.print_help()
usage: PROG [-h]

this description was indented weird but that is okay

options:
 -h, --help  show this help message and exit

likewise for this epilog whose whitespace will be cleaned up and whose words
will be wrapped across a couple lines

```

Passing [`RawDescriptionHelpFormatter`](#argparse.RawDescriptionHelpFormatter "argparse.RawDescriptionHelpFormatter") as `formatter_class=`
indicates that [description](#description) and [epilog](#epilog) are already correctly formatted and
should not be line-wrapped:

Copy

```
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.RawDescriptionHelpFormatter,
...     description=textwrap.dedent('''\
...         Please do not mess up this text!
...         --------------------------------
...             I have indented it
...             exactly the way
...             I want it
...         '''))
>>> parser.print_help()
usage: PROG [-h]

Please do not mess up this text!
--------------------------------
   I have indented it
   exactly the way
   I want it

options:
 -h, --help  show this help message and exit

```

[`RawTextHelpFormatter`](#argparse.RawTextHelpFormatter "argparse.RawTextHelpFormatter") maintains whitespace for all sorts of help text,
including argument descriptions. However, multiple newlines are replaced with
one. If you wish to preserve multiple blank lines, add spaces between the
newlines.

[`ArgumentDefaultsHelpFormatter`](#argparse.ArgumentDefaultsHelpFormatter "argparse.ArgumentDefaultsHelpFormatter") automatically adds information about
default values to each of the argument help messages:

Copy

```
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
>>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
>>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
>>> parser.print_help()
usage: PROG [-h] [--foo FOO] [bar ...]

positional arguments:
 bar         BAR! (default: [1, 2, 3])

options:
 -h, --help  show this help message and exit
 --foo FOO   FOO! (default: 42)

```

[`MetavarTypeHelpFormatter`](#argparse.MetavarTypeHelpFormatter "argparse.MetavarTypeHelpFormatter") uses the name of the [type](#type) argument for each
argument as the display name for its values (rather than using the [dest](#dest)
as the regular formatter does):

Copy

```
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.MetavarTypeHelpFormatter)
>>> parser.add_argument('--foo', type=int)
>>> parser.add_argument('bar', type=float)
>>> parser.print_help()
usage: PROG [-h] [--foo int] float

positional arguments:
  float

options:
  -h, --help  show this help message and exit
  --foo int

```

### prefix\_chars

Most command-line options will use `-` as the prefix, e.g. `-f/--foo`.
Parsers that need to support different or additional prefix
characters, e.g. for options
like `+f` or `/foo`, may specify them using the `prefix_chars=` argument
to the [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") constructor:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
>>> parser.add_argument('+f')
>>> parser.add_argument('++bar')
>>> parser.parse_args('+f X ++bar Y'.split())
Namespace(bar='Y', f='X')

```

The `prefix_chars=` argument defaults to `'-'`. Supplying a set of
characters that does not include `-` will cause `-f/--foo` options to be
disallowed.

### fromfile\_prefix\_chars

Sometimes, when dealing with a particularly long argument list, it
may make sense to keep the list of arguments in a file rather than typing it out
at the command line. If the `fromfile_prefix_chars=` argument is given to the
[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") constructor, then arguments that start with any of the
specified characters will be treated as files, and will be replaced by the
arguments they contain. For example:

Copy

```
>>> with open('args.txt', 'w', encoding=sys.getfilesystemencoding()) as fp:
...     fp.write('-f\nbar')
...
>>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
>>> parser.add_argument('-f')
>>> parser.parse_args(['-f', 'foo', '@args.txt'])
Namespace(f='bar')

```

Arguments read from a file must by default be one per line (but see also
[`convert_arg_line_to_args()`](#argparse.ArgumentParser.convert_arg_line_to_args "argparse.ArgumentParser.convert_arg_line_to_args")) and are treated as if they
were in the same place as the original file referencing argument on the command
line. So in the example above, the expression `['-f', 'foo', '@args.txt']`
is considered equivalent to the expression `['-f', 'foo', '-f', 'bar']`.

[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") uses [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler)
to read the file containing arguments.

The `fromfile_prefix_chars=` argument defaults to `None`, meaning that
arguments will never be treated as file references.

### argument\_default

Generally, argument defaults are specified either by passing a default to
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") or by calling the
[`set_defaults()`](#argparse.ArgumentParser.set_defaults "argparse.ArgumentParser.set_defaults") methods with a specific set of name-value
pairs. Sometimes however, it may be useful to specify a single parser-wide
default for arguments. This can be accomplished by passing the
`argument_default=` keyword argument to [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"). For example,
to globally suppress attribute creation on [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args")
calls, we supply `argument_default=SUPPRESS`:

Copy

```
>>> parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
>>> parser.add_argument('--foo')
>>> parser.add_argument('bar', nargs='?')
>>> parser.parse_args(['--foo', '1', 'BAR'])
Namespace(bar='BAR', foo='1')
>>> parser.parse_args([])
Namespace()

```

### allow\_abbrev

Normally, when you pass an argument list to the
[`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") method of an [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"),
it [recognizes abbreviations](#prefix-matching) of long options.

This feature can be disabled by setting `allow_abbrev` to `False`:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', allow_abbrev=False)
>>> parser.add_argument('--foobar', action='store_true')
>>> parser.add_argument('--foonley', action='store_false')
>>> parser.parse_args(['--foon'])
usage: PROG [-h] [--foobar] [--foonley]
PROG: error: unrecognized arguments: --foon

```

### conflict\_handler

[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects do not allow two actions with the same option
string. By default, [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects raise an exception if an
attempt is made to create an argument with an option string that is already in
use:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo', help='old foo help')
>>> parser.add_argument('--foo', help='new foo help')
Traceback (most recent call last):
 ..
ArgumentError: argument --foo: conflicting option string(s): --foo

```

Sometimes (e.g. when using [parents](#parents)) it may be useful to simply override any
older arguments with the same option string. To get this behavior, the value
`'resolve'` can be supplied to the `conflict_handler=` argument of
[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"):

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
>>> parser.add_argument('-f', '--foo', help='old foo help')
>>> parser.add_argument('--foo', help='new foo help')
>>> parser.print_help()
usage: PROG [-h] [-f FOO] [--foo FOO]

options:
 -h, --help  show this help message and exit
 -f FOO      old foo help
 --foo FOO   new foo help

```

Note that [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects only remove an action if all of its
option strings are overridden. So, in the example above, the old `-f/--foo`
action is retained as the `-f` action, because only the `--foo` option
string was overridden.

### add\_help

By default, [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects add an option which simply displays
the parser’s help message. If `-h` or `--help` is supplied at the command
line, the `ArgumentParser` help will be printed.

Occasionally, it may be useful to disable the addition of this help option.
This can be achieved by passing `False` as the `add_help=` argument to
[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"):

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
>>> parser.add_argument('--foo', help='foo help')
>>> parser.print_help()
usage: PROG [--foo FOO]

options:
 --foo FOO  foo help

```

The help option is typically `-h/--help`. The exception to this is
if the `prefix_chars=` is specified and does not include `-`, in
which case `-h` and `--help` are not valid options. In
this case, the first character in `prefix_chars` is used to prefix
the help options:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='+/')
>>> parser.print_help()
usage: PROG [+h]

options:
  +h, ++help  show this help message and exit

```

### exit\_on\_error

Normally, when you pass an invalid argument list to the [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args")
method of an [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser"), it will print a *message* to [`sys.stderr`](sys.html#sys.stderr "sys.stderr") and exit with a status
code of 2.

If the user would like to catch errors manually, the feature can be enabled by setting
`exit_on_error` to `False`:

Copy

```
>>> parser = argparse.ArgumentParser(exit_on_error=False)
>>> parser.add_argument('--integers', type=int)
_StoreAction(option_strings=['--integers'], dest='integers', nargs=None, const=None, default=None, type=<class 'int'>, choices=None, help=None, metavar=None)
>>> try:
...     parser.parse_args('--integers a'.split())
... except argparse.ArgumentError:
...     print('Catching an argumentError')
...
Catching an argumentError

```

The add\_argument() method
--------------------------

ArgumentParser.add\_argument(*name or flags...*, *\**[, *action*][, *nargs*][, *const*][, *default*][, *type*][, *choices*][, *required*][, *help*][, *metavar*][, *dest*][, *deprecated*])
:   Define how a single command-line argument should be parsed. Each parameter
    has its own more detailed description below, but in short they are:

    * [name or flags](#name-or-flags) - Either a name or a list of option strings, e.g. `'foo'`
      or `'-f', '--foo'`.
    * [action](#action) - The basic type of action to be taken when this argument is
      encountered at the command line.
    * [nargs](#nargs) - The number of command-line arguments that should be consumed.
    * [const](#const) - A constant value required by some [action](#action) and [nargs](#nargs) selections.
    * [default](#default) - The value produced if the argument is absent from the
      command line and if it is absent from the namespace object.
    * [type](#type) - The type to which the command-line argument should be converted.
    * [choices](#choices) - A sequence of the allowable values for the argument.
    * [required](#required) - Whether or not the command-line option may be omitted
      (optionals only).
    * [help](#help) - A brief description of what the argument does.
    * [metavar](#metavar) - A name for the argument in usage messages.
    * [dest](#dest) - The name of the attribute to be added to the object returned by
      [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args").
    * [deprecated](#deprecated) - Whether or not use of the argument is deprecated.

The following sections describe how each of these are used.

### name or flags

The [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") method must know whether an optional
argument, like `-f` or `--foo`, or a positional argument, like a list of
filenames, is expected. The first arguments passed to
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") must therefore be either a series of
flags, or a simple argument name.

For example, an optional argument could be created like:

Copy

```
>>> parser.add_argument('-f', '--foo')

```

while a positional argument could be created like:

Copy

```
>>> parser.add_argument('bar')

```

When [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") is called, optional arguments will be
identified by the `-` prefix, and the remaining arguments will be assumed to
be positional:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo')
>>> parser.add_argument('bar')
>>> parser.parse_args(['BAR'])
Namespace(bar='BAR', foo=None)
>>> parser.parse_args(['BAR', '--foo', 'FOO'])
Namespace(bar='BAR', foo='FOO')
>>> parser.parse_args(['--foo', 'FOO'])
usage: PROG [-h] [-f FOO] bar
PROG: error: the following arguments are required: bar

```

### action

[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects associate command-line arguments with actions. These
actions can do just about anything with the command-line arguments associated with
them, though most actions simply add an attribute to the object returned by
[`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args"). The `action` keyword argument specifies
how the command-line arguments should be handled. The supplied actions are:

* `'store'` - This just stores the argument’s value. This is the default
  action.
* `'store_const'` - This stores the value specified by the [const](#const) keyword
  argument; note that the [const](#const) keyword argument defaults to `None`. The
  `'store_const'` action is most commonly used with optional arguments that
  specify some sort of flag. For example:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', action='store_const', const=42)
  >>> parser.parse_args(['--foo'])
  Namespace(foo=42)

  ```
* `'store_true'` and `'store_false'` - These are special cases of
  `'store_const'` used for storing the values `True` and `False`
  respectively. In addition, they create default values of `False` and
  `True` respectively:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', action='store_true')
  >>> parser.add_argument('--bar', action='store_false')
  >>> parser.add_argument('--baz', action='store_false')
  >>> parser.parse_args('--foo --bar'.split())
  Namespace(foo=True, bar=False, baz=True)

  ```
* `'append'` - This stores a list, and appends each argument value to the
  list. It is useful to allow an option to be specified multiple times.
  If the default value is non-empty, the default elements will be present
  in the parsed value for the option, with any values from the
  command line appended after those default values. Example usage:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', action='append')
  >>> parser.parse_args('--foo 1 --foo 2'.split())
  Namespace(foo=['1', '2'])

  ```
* `'append_const'` - This stores a list, and appends the value specified by
  the [const](#const) keyword argument to the list; note that the [const](#const) keyword
  argument defaults to `None`. The `'append_const'` action is typically
  useful when multiple arguments need to store constants to the same list. For
  example:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
  >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
  >>> parser.parse_args('--str --int'.split())
  Namespace(types=[<class 'str'>, <class 'int'>])

  ```
* `'extend'` - This stores a list and appends each item from the multi-value
  argument list to it.
  The `'extend'` action is typically used with the [nargs](#nargs) keyword argument
  value `'+'` or `'*'`.
  Note that when [nargs](#nargs) is `None` (the default) or `'?'`, each
  character of the argument string will be appended to the list.
  Example usage:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument("--foo", action="extend", nargs="+", type=str)
  >>> parser.parse_args(["--foo", "f1", "--foo", "f2", "f3", "f4"])
  Namespace(foo=['f1', 'f2', 'f3', 'f4'])

  ```
* `'count'` - This counts the number of times a keyword argument occurs. For
  example, this is useful for increasing verbosity levels:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--verbose', '-v', action='count', default=0)
  >>> parser.parse_args(['-vvv'])
  Namespace(verbose=3)

  ```

  Note, the *default* will be `None` unless explicitly set to *0*.
* `'help'` - This prints a complete help message for all the options in the
  current parser and then exits. By default a help action is automatically
  added to the parser. See [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") for details of how the
  output is created.
* `'version'` - This expects a `version=` keyword argument in the
  [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") call, and prints version information
  and exits when invoked:

  Copy

  ```
  >>> import argparse
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
  >>> parser.parse_args(['--version'])
  PROG 2.0

  ```

You may also specify an arbitrary action by passing an [`Action`](#argparse.Action "argparse.Action") subclass
(e.g. [`BooleanOptionalAction`](#argparse.BooleanOptionalAction "argparse.BooleanOptionalAction")) or other object that implements the same
interface. Only actions that consume command-line arguments (e.g. `'store'`,
`'append'`, `'extend'`, or custom actions with non-zero `nargs`) can be used
with positional arguments.

The recommended way to create a custom action is to extend [`Action`](#argparse.Action "argparse.Action"),
overriding the `__call__()` method and optionally the `__init__()` and
`format_usage()` methods. You can also register custom actions using the
[`register()`](#argparse.ArgumentParser.register "argparse.ArgumentParser.register") method and reference them by their registered name.

An example of a custom action:

Copy

```
>>> class FooAction(argparse.Action):
...     def __init__(self, option_strings, dest, nargs=None, **kwargs):
...         if nargs is not None:
...             raise ValueError("nargs not allowed")
...         super().__init__(option_strings, dest, **kwargs)
...     def __call__(self, parser, namespace, values, option_string=None):
...         print('%r %r %r' % (namespace, values, option_string))
...         setattr(namespace, self.dest, values)
...
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', action=FooAction)
>>> parser.add_argument('bar', action=FooAction)
>>> args = parser.parse_args('1 --foo 2'.split())
Namespace(bar=None, foo=None) '1' None
Namespace(bar='1', foo=None) '2' '--foo'
>>> args
Namespace(bar='1', foo='2')

```

For more details, see [`Action`](#argparse.Action "argparse.Action").

### nargs

[`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") objects usually associate a single command-line argument with a
single action to be taken. The `nargs` keyword argument associates a
different number of command-line arguments with a single action.
See also [Specifying ambiguous arguments](../howto/argparse.html#specifying-ambiguous-arguments). The supported values are:

* `N` (an integer). `N` arguments from the command line will be gathered
  together into a list. For example:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', nargs=2)
  >>> parser.add_argument('bar', nargs=1)
  >>> parser.parse_args('c --foo a b'.split())
  Namespace(bar=['c'], foo=['a', 'b'])

  ```

  Note that `nargs=1` produces a list of one item. This is different from
  the default, in which the item is produced by itself.

* `'?'`. One argument will be consumed from the command line if possible, and
  produced as a single item. If no command-line argument is present, the value from
  [default](#default) will be produced. Note that for optional arguments, there is an
  additional case - the option string is present but not followed by a
  command-line argument. In this case the value from [const](#const) will be produced. Some
  examples to illustrate this:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
  >>> parser.add_argument('bar', nargs='?', default='d')
  >>> parser.parse_args(['XX', '--foo', 'YY'])
  Namespace(bar='XX', foo='YY')
  >>> parser.parse_args(['XX', '--foo'])
  Namespace(bar='XX', foo='c')
  >>> parser.parse_args([])
  Namespace(bar='d', foo='d')

  ```

  One of the more common uses of `nargs='?'` is to allow optional input and
  output files:

  Copy

  ```
  >>> parser = argparse.ArgumentParser()
  >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
  ...                     default=sys.stdin)
  >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
  ...                     default=sys.stdout)
  >>> parser.parse_args(['input.txt', 'output.txt'])
  Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
            outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
  >>> parser.parse_args([])
  Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
            outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)

  ```

* `'+'`. Just like `'*'`, all command-line arguments present are gathered into a
  list. Additionally, an error message will be generated if there wasn’t at
  least one command-line argument present. For example:

  Copy

  ```
  >>> parser = argparse.ArgumentParser(prog='PROG')
  >>> parser.add_argument('foo', nargs='+')
  >>> parser.parse_args(['a', 'b'])
  Namespace(foo=['a', 'b'])
  >>> parser.parse_args([])
  usage: PROG [-h] foo [foo ...]
  PROG: error: the following arguments are required: foo

  ```

If the `nargs` keyword argument is not provided, the number of arguments consumed
is determined by the [action](#action). Generally this means a single command-line argument
will be consumed and a single item (not a list) will be produced.
Actions that do not consume command-line arguments (e.g.
`'store_const'`) set `nargs=0`.

### const

The `const` argument of [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") is used to hold
constant values that are not read from the command line but are required for
the various [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") actions. The two most common uses of it are:

* When [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") is called with
  `action='store_const'` or `action='append_const'`. These actions add the
  `const` value to one of the attributes of the object returned by
  [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args"). See the [action](#action) description for examples.
  If `const` is not provided to [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"), it will
  receive a default value of `None`.
* When [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") is called with option strings
  (like `-f` or `--foo`) and `nargs='?'`. This creates an optional
  argument that can be followed by zero or one command-line arguments.
  When parsing the command line, if the option string is encountered with no
  command-line argument following it, the value of `const` will be assumed to
  be `None` instead. See the [nargs](#nargs) description for examples.

Changed in version 3.11: `const=None` by default, including when `action='append_const'` or
`action='store_const'`.

### default

All optional arguments and some positional arguments may be omitted at the
command line. The `default` keyword argument of
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"), whose value defaults to `None`,
specifies what value should be used if the command-line argument is not present.
For optional arguments, the `default` value is used when the option string
was not present at the command line:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', default=42)
>>> parser.parse_args(['--foo', '2'])
Namespace(foo='2')
>>> parser.parse_args([])
Namespace(foo=42)

```

If the target namespace already has an attribute set, the action *default*
will not overwrite it:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', default=42)
>>> parser.parse_args([], namespace=argparse.Namespace(foo=101))
Namespace(foo=101)

```

If the `default` value is a string, the parser parses the value as if it
were a command-line argument. In particular, the parser applies any [type](#type)
conversion argument, if provided, before setting the attribute on the
[`Namespace`](#argparse.Namespace "argparse.Namespace") return value. Otherwise, the parser uses the value as is:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--length', default='10', type=int)
>>> parser.add_argument('--width', default=10.5, type=int)
>>> parser.parse_args()
Namespace(length=10, width=10.5)

```

For positional arguments with [nargs](#nargs) equal to `?` or `*`, the `default` value
is used when no command-line argument was present:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('foo', nargs='?', default=42)
>>> parser.parse_args(['a'])
Namespace(foo='a')
>>> parser.parse_args([])
Namespace(foo=42)

```

For [required](#required) arguments, the `default` value is ignored. For example, this
applies to positional arguments with [nargs](#nargs) values other than `?` or `*`,
or optional arguments marked as `required=True`.

Providing `default=argparse.SUPPRESS` causes no attribute to be added if the
command-line argument was not present:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', default=argparse.SUPPRESS)
>>> parser.parse_args([])
Namespace()
>>> parser.parse_args(['--foo', '1'])
Namespace(foo='1')

```

### type

By default, the parser reads command-line arguments in as simple
strings. However, quite often the command-line string should instead be
interpreted as another type, such as a [`float`](functions.html#float "float") or [`int`](functions.html#int "int"). The
`type` keyword for [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") allows any
necessary type-checking and type conversions to be performed.

If the [type](#type) keyword is used with the [default](#default) keyword, the type converter
is only applied if the default is a string.

The argument to `type` can be a callable that accepts a single string or
the name of a registered type (see [`register()`](#argparse.ArgumentParser.register "argparse.ArgumentParser.register"))
If the function raises [`ArgumentTypeError`](#argparse.ArgumentTypeError "argparse.ArgumentTypeError"), [`TypeError`](exceptions.html#TypeError "TypeError"), or
[`ValueError`](exceptions.html#ValueError "ValueError"), the exception is caught and a nicely formatted error
message is displayed. Other exception types are not handled.

Common built-in types and functions can be used as type converters:

Copy

```
import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int)
parser.add_argument('distance', type=float)
parser.add_argument('street', type=ascii)
parser.add_argument('code_point', type=ord)
parser.add_argument('dest_file', type=argparse.FileType('w', encoding='latin-1'))
parser.add_argument('datapath', type=pathlib.Path)

```

User defined functions can be used as well:

Copy

```
>>> def hyphenated(string):
...     return '-'.join([word[:4] for word in string.casefold().split()])
...
>>> parser = argparse.ArgumentParser()
>>> _ = parser.add_argument('short_title', type=hyphenated)
>>> parser.parse_args(['"The Tale of Two Cities"'])
Namespace(short_title='"the-tale-of-two-citi')

```

The [`bool()`](functions.html#bool "bool") function is not recommended as a type converter. All it does
is convert empty strings to `False` and non-empty strings to `True`.
This is usually not what is desired.

In general, the `type` keyword is a convenience that should only be used for
simple conversions that can only raise one of the three supported exceptions.
Anything with more interesting error-handling or resource management should be
done downstream after the arguments are parsed.

For example, JSON or YAML conversions have complex error cases that require
better reporting than can be given by the `type` keyword. A
[`JSONDecodeError`](json.html#json.JSONDecodeError "json.JSONDecodeError") would not be well formatted and a
[`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") exception would not be handled at all.

Even [`FileType`](#argparse.FileType "argparse.FileType") has its limitations for use with the `type`
keyword. If one argument uses [`FileType`](#argparse.FileType "argparse.FileType") and then a
subsequent argument fails, an error is reported but the file is not
automatically closed. In this case, it would be better to wait until after
the parser has run and then use the [`with`](../reference/compound_stmts.html#with)-statement to manage the
files.

For type checkers that simply check against a fixed set of values, consider
using the [choices](#choices) keyword instead.

### choices

Some command-line arguments should be selected from a restricted set of values.
These can be handled by passing a sequence object as the *choices* keyword
argument to [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"). When the command line is
parsed, argument values will be checked, and an error message will be displayed
if the argument was not one of the acceptable values:

Copy

```
>>> parser = argparse.ArgumentParser(prog='game.py')
>>> parser.add_argument('move', choices=['rock', 'paper', 'scissors'])
>>> parser.parse_args(['rock'])
Namespace(move='rock')
>>> parser.parse_args(['fire'])
usage: game.py [-h] {rock,paper,scissors}
game.py: error: argument move: invalid choice: 'fire' (choose from 'rock',
'paper', 'scissors')

```

Note that inclusion in the *choices* sequence is checked after any [type](#type)
conversions have been performed, so the type of the objects in the *choices*
sequence should match the [type](#type) specified.

Any sequence can be passed as the *choices* value, so [`list`](stdtypes.html#list "list") objects,
[`tuple`](stdtypes.html#tuple "tuple") objects, and custom sequences are all supported.

Use of [`enum.Enum`](enum.html#enum.Enum "enum.Enum") is not recommended because it is difficult to
control its appearance in usage, help, and error messages.

Formatted choices override the default *metavar* which is normally derived
from *dest*. This is usually what you want because the user never sees the
*dest* parameter. If this display isn’t desirable (perhaps because there are
many choices), just specify an explicit [metavar](#metavar).

### required

In general, the `argparse` module assumes that flags like `-f` and `--bar`
indicate *optional* arguments, which can always be omitted at the command line.
To make an option *required*, `True` can be specified for the `required=`
keyword argument to [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"):

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', required=True)
>>> parser.parse_args(['--foo', 'BAR'])
Namespace(foo='BAR')
>>> parser.parse_args([])
usage: [-h] --foo FOO
: error: the following arguments are required: --foo

```

As the example shows, if an option is marked as `required`,
[`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") will report an error if that option is not
present at the command line.

Note

Required options are generally considered bad form because users expect
*options* to be *optional*, and thus they should be avoided when possible.

### help

The `help` value is a string containing a brief description of the argument.
When a user requests help (usually by using `-h` or `--help` at the
command line), these `help` descriptions will be displayed with each
argument.

The `help` strings can include various format specifiers to avoid repetition
of things like the program name or the argument [default](#default). The available
specifiers include the program name, `%(prog)s` and most keyword arguments to
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"), e.g. `%(default)s`, `%(type)s`, etc.:

Copy

```
>>> parser = argparse.ArgumentParser(prog='frobble')
>>> parser.add_argument('bar', nargs='?', type=int, default=42,
...                     help='the bar to %(prog)s (default: %(default)s)')
>>> parser.print_help()
usage: frobble [-h] [bar]

positional arguments:
 bar     the bar to frobble (default: 42)

options:
 -h, --help  show this help message and exit

```

As the help string supports %-formatting, if you want a literal `%` to appear
in the help string, you must escape it as `%%`.

`argparse` supports silencing the help entry for certain options, by
setting the `help` value to `argparse.SUPPRESS`:

Copy

```
>>> parser = argparse.ArgumentParser(prog='frobble')
>>> parser.add_argument('--foo', help=argparse.SUPPRESS)
>>> parser.print_help()
usage: frobble [-h]

options:
  -h, --help  show this help message and exit

```

### dest

Most [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") actions add some value as an attribute of the
object returned by [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args"). The name of this
attribute is determined by the `dest` keyword argument of
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"). For positional argument actions,
`dest` is normally supplied as the first argument to
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"):

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('bar')
>>> parser.parse_args(['XXX'])
Namespace(bar='XXX')

```

For optional argument actions, the value of `dest` is normally inferred from
the option strings. [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") generates the value of `dest` by
taking the first long option string and stripping away the initial `--`
string. If no long option strings were supplied, `dest` will be derived from
the first short option string by stripping the initial `-` character. Any
internal `-` characters will be converted to `_` characters to make sure
the string is a valid attribute name. The examples below illustrate this
behavior:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('-f', '--foo-bar', '--foo')
>>> parser.add_argument('-x', '-y')
>>> parser.parse_args('-f 1 -x 2'.split())
Namespace(foo_bar='1', x='2')
>>> parser.parse_args('--foo 1 -y 2'.split())
Namespace(foo_bar='1', x='2')

```

`dest` allows a custom attribute name to be provided:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', dest='bar')
>>> parser.parse_args('--foo XXX'.split())
Namespace(bar='XXX')

```

### deprecated

During a project’s lifetime, some arguments may need to be removed from the
command line. Before removing them, you should inform
your users that the arguments are deprecated and will be removed.
The `deprecated` keyword argument of
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument"), which defaults to `False`,
specifies if the argument is deprecated and will be removed
in the future.
For arguments, if `deprecated` is `True`, then a warning will be
printed to [`sys.stderr`](sys.html#sys.stderr "sys.stderr") when the argument is used:

Copy

```
>>> import argparse
>>> parser = argparse.ArgumentParser(prog='snake.py')
>>> parser.add_argument('--legs', default=0, type=int, deprecated=True)
>>> parser.parse_args([])
Namespace(legs=0)
>>> parser.parse_args(['--legs', '4'])
snake.py: warning: option '--legs' is deprecated
Namespace(legs=4)

```

### Action classes

`Action` classes implement the Action API, a callable which returns a callable
which processes arguments from the command-line. Any object which follows
this API may be passed as the `action` parameter to
[`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument").

*class* argparse.Action(*option\_strings*, *dest*, *nargs=None*, *const=None*, *default=None*, *type=None*, *choices=None*, *required=False*, *help=None*, *metavar=None*)
:   `Action` objects are used by an [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") to represent the information
    needed to parse a single argument from one or more strings from the
    command line. The `Action` class must accept the two positional arguments
    plus any keyword arguments passed to [`ArgumentParser.add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument")
    except for the `action` itself.

    Instances of `Action` (or return value of any callable to the
    `action` parameter) should have attributes `dest`,
    `option_strings`, `default`, `type`, `required`,
    `help`, etc. defined. The easiest way to ensure these attributes
    are defined is to call `Action.__init__()`.

    \_\_call\_\_(*parser*, *namespace*, *values*, *option\_string=None*)
    :   `Action` instances should be callable, so subclasses must override the
        `__call__()` method, which should accept four parameters:

        * *parser* - The [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") object which contains this action.
        * *namespace* - The [`Namespace`](#argparse.Namespace "argparse.Namespace") object that will be returned by
          [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args"). Most actions add an attribute to this
          object using [`setattr()`](functions.html#setattr "setattr").
        * *values* - The associated command-line arguments, with any type conversions
          applied. Type conversions are specified with the [type](#type) keyword argument to
          [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument").
        * *option\_string* - The option string that was used to invoke this action.
          The `option_string` argument is optional, and will be absent if the action
          is associated with a positional argument.

        The `__call__()` method may perform arbitrary actions, but will typically set
        attributes on the `namespace` based on `dest` and `values`.

    format\_usage()
    :   `Action` subclasses can define a `format_usage()` method that takes no argument
        and return a string which will be used when printing the usage of the program.
        If such method is not provided, a sensible default will be used.

*class* argparse.BooleanOptionalAction
:   A subclass of [`Action`](#argparse.Action "argparse.Action") for handling boolean flags with positive
    and negative options. Adding a single argument such as `--foo` automatically
    creates both `--foo` and `--no-foo` options, storing `True` and `False`
    respectively:

    Copy

    ```
    >>> import argparse
    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action=argparse.BooleanOptionalAction)
    >>> parser.parse_args(['--no-foo'])
    Namespace(foo=False)

    ```

The parse\_args() method
------------------------

ArgumentParser.parse\_args(*args=None*, *namespace=None*)
:   Convert argument strings to objects and assign them as attributes of the
    namespace. Return the populated namespace.

    Previous calls to [`add_argument()`](#argparse.ArgumentParser.add_argument "argparse.ArgumentParser.add_argument") determine exactly what objects are
    created and how they are assigned. See the documentation for
    `add_argument()` for details.

### Option value syntax

The [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") method supports several ways of
specifying the value of an option (if it takes one). In the simplest case, the
option and its value are passed as two separate arguments:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-x')
>>> parser.add_argument('--foo')
>>> parser.parse_args(['-x', 'X'])
Namespace(foo=None, x='X')
>>> parser.parse_args(['--foo', 'FOO'])
Namespace(foo='FOO', x=None)

```

For long options (options with names longer than a single character), the option
and value can also be passed as a single command-line argument, using `=` to
separate them:

Copy

```
>>> parser.parse_args(['--foo=FOO'])
Namespace(foo='FOO', x=None)

```

For short options (options only one character long), the option and its value
can be concatenated:

Copy

```
>>> parser.parse_args(['-xX'])
Namespace(foo=None, x='X')

```

Several short options can be joined together, using only a single `-` prefix,
as long as only the last option (or none of them) requires a value:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-x', action='store_true')
>>> parser.add_argument('-y', action='store_true')
>>> parser.add_argument('-z')
>>> parser.parse_args(['-xyzZ'])
Namespace(x=True, y=True, z='Z')

```

### Invalid arguments

While parsing the command line, [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") checks for a
variety of errors, including ambiguous options, invalid types, invalid options,
wrong number of positional arguments, etc. When it encounters such an error,
it exits and prints the error along with a usage message:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo', type=int)
>>> parser.add_argument('bar', nargs='?')

>>> # invalid type
>>> parser.parse_args(['--foo', 'spam'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: argument --foo: invalid int value: 'spam'

>>> # invalid option
>>> parser.parse_args(['--bar'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: no such option: --bar

>>> # wrong number of arguments
>>> parser.parse_args(['spam', 'badger'])
usage: PROG [-h] [--foo FOO] [bar]
PROG: error: extra arguments found: badger

```

### Arguments containing `-`

The [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") method attempts to give errors whenever
the user has clearly made a mistake, but some situations are inherently
ambiguous. For example, the command-line argument `-1` could either be an
attempt to specify an option or an attempt to provide a positional argument.
The [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") method is cautious here: positional
arguments may only begin with `-` if they look like negative numbers and
there are no options in the parser that look like negative numbers:

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-x')
>>> parser.add_argument('foo', nargs='?')

>>> # no negative number options, so -1 is a positional argument
>>> parser.parse_args(['-x', '-1'])
Namespace(foo=None, x='-1')

>>> # no negative number options, so -1 and -5 are positional arguments
>>> parser.parse_args(['-x', '-1', '-5'])
Namespace(foo='-5', x='-1')

>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-1', dest='one')
>>> parser.add_argument('foo', nargs='?')

>>> # negative number options present, so -1 is an option
>>> parser.parse_args(['-1', 'X'])
Namespace(foo=None, one='X')

>>> # negative number options present, so -2 is an option
>>> parser.parse_args(['-2'])
usage: PROG [-h] [-1 ONE] [foo]
PROG: error: no such option: -2

>>> # negative number options present, so both -1s are options
>>> parser.parse_args(['-1', '-1'])
usage: PROG [-h] [-1 ONE] [foo]
PROG: error: argument -1: expected one argument

```

If you have positional arguments that must begin with `-` and don’t look
like negative numbers, you can insert the pseudo-argument `'--'` which tells
[`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") that everything after that is a positional
argument:

Copy

```
>>> parser.parse_args(['--', '-f'])
Namespace(foo='-f', one=None)

```

See also [the argparse howto on ambiguous arguments](../howto/argparse.html#specifying-ambiguous-arguments)
for more details.

### Argument abbreviations (prefix matching)

The [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") method [by default](#allow-abbrev)
allows long options to be abbreviated to a prefix, if the abbreviation is
unambiguous (the prefix matches a unique option):

Copy

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-bacon')
>>> parser.add_argument('-badger')
>>> parser.parse_args('-bac MMM'.split())
Namespace(bacon='MMM', badger=None)
>>> parser.parse_args('-bad WOOD'.split())
Namespace(bacon=None, badger='WOOD')
>>> parser.parse_args('-ba BA'.split())
usage: PROG [-h] [-bacon BACON] [-badger BADGER]
PROG: error: ambiguous option: -ba could match -badger, -bacon

```

An error is produced for arguments that could produce more than one options.
This feature can be disabled by setting [allow\_abbrev](#allow-abbrev) to `False`.

### Beyond `sys.argv`

Sometimes it may be useful to have an [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") parse arguments other than those
of [`sys.argv`](sys.html#sys.argv "sys.argv"). This can be accomplished by passing a list of strings to
[`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args"). This is useful for testing at the
interactive prompt:

Copy

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument(
...     'integers', metavar='int', type=int, choices=range(10),
...     nargs='+', help='an integer in the range 0..9')
>>> parser.add_argument(
...     '--sum', dest='accumulate', action='store_const', const=sum,
...     default=max, help='sum the integers (default: find the max)')
>>> parser.parse_args(['1', '2', '3', '4'])
Namespace(accumulate=<built-in function max>, integers=[1, 2, 3, 4])
>>> parser.parse_args(['1', '2', '3', '4', '--sum'])
Namespace(accumulate=<built-in function sum>, integers=[1, 2, 3, 4])

```

### The Namespace object

*class* argparse.Namespace
:   Simple class used by default by [`parse_args()`](#argparse.ArgumentParser.parse_args "argparse.ArgumentParser.parse_args") to create
    an object holding attributes and return it.

    This class is deliberately simple, just an [`object`](functions.html#object "object") subclass with a
    readable string representation. If you prefer to have dict-like view of the
    attributes, you can use the standard Python idiom, [`vars()`](functions.html#vars "vars"):

    Copy

    ```
    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo')
    >>> args = parser.parse_args(['--foo', 'BAR'])
    >>> vars(args)
    {'foo': 'BAR'}

    ```

    It may also be useful to have an [`ArgumentParser`](#argparse.ArgumentParser "argparse.ArgumentParser") assign attributes to an
    already existing object, rather than a new [`Namespace`](#argparse.Namespace "argparse.Namespace") object. This can
    be achieved by specifying the `namespace=` keyword argument:

    Copy

    ```
    >>> class C:
    ...     pass
    ...
    >>> c = C()
    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo')
    >>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
    >>> c.foo
    'BAR'

    ```