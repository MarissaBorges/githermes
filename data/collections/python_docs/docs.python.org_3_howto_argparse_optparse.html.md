Migrating `optparse` code to `argparse`
=======================================

The [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library.") module offers several higher level features not natively
provided by the [`optparse`](../library/optparse.html#module-optparse "optparse: Command-line option parsing library.") module, including:

* Handling positional arguments.
* Supporting subcommands.
* Allowing alternative option prefixes like `+` and `/`.
* Handling zero-or-more and one-or-more style arguments.
* Producing more informative usage messages.
* Providing a much simpler interface for custom `type` and `action`.

Originally, the [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library.") module attempted to maintain compatibility
with [`optparse`](../library/optparse.html#module-optparse "optparse: Command-line option parsing library."). However, the fundamental design differences between
supporting declarative command line option processing (while leaving positional
argument processing to application code), and supporting both named options
and positional arguments in the declarative interface mean that the
API has diverged from that of `optparse` over time.

As described in [Choosing an argument parsing library](../library/optparse.html#choosing-an-argument-parser), applications that are
currently using [`optparse`](../library/optparse.html#module-optparse "optparse: Command-line option parsing library.") and are happy with the way it works can
just continue to use `optparse`.

Application developers that are considering migrating should also review
the list of intrinsic behavioural differences described in that section
before deciding whether or not migration is desirable.

For applications that do choose to migrate from [`optparse`](../library/optparse.html#module-optparse "optparse: Command-line option parsing library.") to [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library."),
the following suggestions should be helpful: