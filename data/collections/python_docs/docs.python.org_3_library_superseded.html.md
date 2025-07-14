Superseded Modules
==================

The modules described in this chapter have been superseded by other modules
for most use cases, and are retained primarily to preserve backwards compatibility.

Modules may appear in this chapter because they only cover a limited subset of
a problem space, and a more generally applicable solution is available elsewhere
in the standard library (for example, [`getopt`](getopt.html#module-getopt "getopt: Portable parser for command line options; support both short and long option names.") covers the very specific
task of “mimic the C `getopt()` API in Python”, rather than the broader
command line option parsing and argument parsing capabilities offered by
[`optparse`](optparse.html#module-optparse "optparse: Command-line option parsing library.") and [`argparse`](argparse.html#module-argparse "argparse: Command-line option and argument parsing library.")).

Alternatively, modules may appear in this chapter because they are deprecated
outright, and awaiting removal in a future release, or they are
[soft deprecated](../glossary.html#term-soft-deprecated) and their use is actively discouraged in new projects.
With the removal of various obsolete modules through [**PEP 594**](https://peps.python.org/pep-0594/), there are
currently no modules in this latter category.