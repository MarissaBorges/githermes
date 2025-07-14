:   Open *file* and return a corresponding [file object](../glossary.html#term-file-object). If the file
    cannot be opened, an [`OSError`](exceptions.html#OSError "OSError") is raised. See
    [Reading and Writing Files](../tutorial/inputoutput.html#tut-files) for more examples of how to use this function.

    *file* is a [path-like object](../glossary.html#term-path-like-object) giving the pathname (absolute or
    relative to the current working directory) of the file to be opened or an
    integer file descriptor of the file to be wrapped. (If a file descriptor is
    given, it is closed when the returned I/O object is closed unless *closefd*
    is set to `False`.)

    *mode* is an optional string that specifies the mode in which the file is
    opened. It defaults to `'r'` which means open for reading in text mode.
    Other common values are `'w'` for writing (truncating the file if it
    already exists), `'x'` for exclusive creation, and `'a'` for appending
    (which on *some* Unix systems, means that *all* writes append to the end of
    the file regardless of the current seek position). In text mode, if
    *encoding* is not specified the encoding used is platform-dependent:
    [`locale.getencoding()`](locale.html#locale.getencoding "locale.getencoding") is called to get the current locale encoding.
    (For reading and writing raw bytes use binary mode and leave
    *encoding* unspecified.) The available modes are:

    | Character | Meaning |
    | --- | --- |
    | `'r'` | open for reading (default) |
    | `'w'` | open for writing, truncating the file first |
    | `'x'` | open for exclusive creation, failing if the file already exists |
    | `'a'` | open for writing, appending to the end of file if it exists |
    | `'b'` | binary mode |
    | `'t'` | text mode (default) |
    | `'+'` | open for updating (reading and writing) |

    The default mode is `'r'` (open for reading text, a synonym of `'rt'`).
    Modes `'w+'` and `'w+b'` open and truncate the file. Modes `'r+'`
    and `'r+b'` open the file with no truncation.

    As mentioned in the [Overview](io.html#io-overview), Python distinguishes between binary
    and text I/O. Files opened in binary mode (including `'b'` in the *mode*
    argument) return contents as [`bytes`](stdtypes.html#bytes "bytes") objects without any decoding. In
    text mode (the default, or when `'t'` is included in the *mode* argument),
    the contents of the file are returned as [`str`](stdtypes.html#str "str"), the bytes having been
    first decoded using a platform-dependent encoding or using the specified
    *encoding* if given.

    Note

    Python doesn’t depend on the underlying operating system’s notion of text
    files; all the processing is done by Python itself, and is therefore
    platform-independent.

    *buffering* is an optional integer used to set the buffering policy. Pass 0
    to switch buffering off (only allowed in binary mode), 1 to select line
    buffering (only usable when writing in text mode), and an integer > 1 to indicate the size
    in bytes of a fixed-size chunk buffer. Note that specifying a buffer size this
    way applies for binary buffered I/O, but `TextIOWrapper` (i.e., files opened
    with `mode='r+'`) would have another buffering. To disable buffering in
    `TextIOWrapper`, consider using the `write_through` flag for
    [`io.TextIOWrapper.reconfigure()`](io.html#io.TextIOWrapper.reconfigure "io.TextIOWrapper.reconfigure"). When no *buffering* argument is
    given, the default buffering policy works as follows:

    * Binary files are buffered in fixed-size chunks; the size of the buffer is
      chosen using a heuristic trying to determine the underlying device’s “block
      size” and falling back on [`io.DEFAULT_BUFFER_SIZE`](io.html#io.DEFAULT_BUFFER_SIZE "io.DEFAULT_BUFFER_SIZE"). On many systems,
      the buffer will typically be 4096 or 8192 bytes long.
    * “Interactive” text files (files for which [`isatty()`](io.html#io.IOBase.isatty "io.IOBase.isatty")
      returns `True`) use line buffering. Other text files use the policy
      described above for binary files.

    *encoding* is the name of the encoding used to decode or encode the file.
    This should only be used in text mode. The default encoding is platform
    dependent (whatever [`locale.getencoding()`](locale.html#locale.getencoding "locale.getencoding") returns), but any
    [text encoding](../glossary.html#term-text-encoding) supported by Python can be used.
    See the [`codecs`](codecs.html#module-codecs "codecs: Encode and decode data and streams.") module for the list of supported encodings.

    *errors* is an optional string that specifies how encoding and decoding
    errors are to be handled—this cannot be used in binary mode.
    A variety of standard error handlers are available
    (listed under [Error Handlers](codecs.html#error-handlers)), though any
    error handling name that has been registered with
    [`codecs.register_error()`](codecs.html#codecs.register_error "codecs.register_error") is also valid. The standard names
    include:

    * `'strict'` to raise a [`ValueError`](exceptions.html#ValueError "ValueError") exception if there is
      an encoding error. The default value of `None` has the same
      effect.
    * `'ignore'` ignores errors. Note that ignoring encoding errors
      can lead to data loss.
    * `'replace'` causes a replacement marker (such as `'?'`) to be inserted
      where there is malformed data.
    * `'surrogateescape'` will represent any incorrect bytes as low
      surrogate code units ranging from U+DC80 to U+DCFF.
      These surrogate code units will then be turned back into
      the same bytes when the `surrogateescape` error handler is used
      when writing data. This is useful for processing files in an
      unknown encoding.
    * `'xmlcharrefreplace'` is only supported when writing to a file.
      Characters not supported by the encoding are replaced with the
      appropriate XML character reference `&#nnn;`.
    * `'backslashreplace'` replaces malformed data by Python’s backslashed
      escape sequences.
    * `'namereplace'` (also only supported when writing)
      replaces unsupported characters with `\N{...}` escape sequences.

    *newline* determines how to parse newline characters from the stream.
    It can be `None`, `''`, `'\n'`, `'\r'`, and
    `'\r\n'`. It works as follows:

    * When reading input from the stream, if *newline* is `None`, universal
      newlines mode is enabled. Lines in the input can end in `'\n'`,
      `'\r'`, or `'\r\n'`, and these are translated into `'\n'` before
      being returned to the caller. If it is `''`, universal newlines mode is
      enabled, but line endings are returned to the caller untranslated. If it
      has any of the other legal values, input lines are only terminated by the
      given string, and the line ending is returned to the caller untranslated.
    * When writing output to the stream, if *newline* is `None`, any `'\n'`
      characters written are translated to the system default line separator,
      [`os.linesep`](os.html#os.linesep "os.linesep"). If *newline* is `''` or `'\n'`, no translation
      takes place. If *newline* is any of the other legal values, any `'\n'`
      characters written are translated to the given string.

    If *closefd* is `False` and a file descriptor rather than a filename was
    given, the underlying file descriptor will be kept open when the file is
    closed. If a filename is given *closefd* must be `True` (the default);
    otherwise, an error will be raised.

    A custom opener can be used by passing a callable as *opener*. The underlying
    file descriptor for the file object is then obtained by calling *opener* with
    (*file*, *flags*). *opener* must return an open file descriptor (passing
    [`os.open`](os.html#os.open "os.open") as *opener* results in functionality similar to passing
    `None`).

    The newly created file is [non-inheritable](os.html#fd-inheritance).

    The following example uses the [dir\_fd](os.html#dir-fd) parameter of the
    [`os.open()`](os.html#os.open "os.open") function to open a file relative to a given directory:

    Copy

    ```
    >>> import os
    >>> dir_fd = os.open('somedir', os.O_RDONLY)
    >>> def opener(path, flags):
    ...     return os.open(path, flags, dir_fd=dir_fd)
    ...
    >>> with open('spamspam.txt', 'w', opener=opener) as f:
    ...     print('This will be written to somedir/spamspam.txt', file=f)
    ...
    >>> os.close(dir_fd)  # don't leak a file descriptor

    ```

    The type of [file object](../glossary.html#term-file-object) returned by the [`open()`](#open "open") function
    depends on the mode. When [`open()`](#open "open") is used to open a file in a text
    mode (`'w'`, `'r'`, `'wt'`, `'rt'`, etc.), it returns a subclass of
    [`io.TextIOBase`](io.html#io.TextIOBase "io.TextIOBase") (specifically [`io.TextIOWrapper`](io.html#io.TextIOWrapper "io.TextIOWrapper")). When used
    to open a file in a binary mode with buffering, the returned class is a
    subclass of [`io.BufferedIOBase`](io.html#io.BufferedIOBase "io.BufferedIOBase"). The exact class varies: in read
    binary mode, it returns an [`io.BufferedReader`](io.html#io.BufferedReader "io.BufferedReader"); in write binary and
    append binary modes, it returns an [`io.BufferedWriter`](io.html#io.BufferedWriter "io.BufferedWriter"), and in
    read/write mode, it returns an [`io.BufferedRandom`](io.html#io.BufferedRandom "io.BufferedRandom"). When buffering is
    disabled, the raw stream, a subclass of [`io.RawIOBase`](io.html#io.RawIOBase "io.RawIOBase"),
    [`io.FileIO`](io.html#io.FileIO "io.FileIO"), is returned.

    See also the file handling modules, such as [`fileinput`](fileinput.html#module-fileinput "fileinput: Loop over standard input or a list of files."), [`io`](io.html#module-io "io: Core tools for working with streams.")
    (where [`open()`](#open "open") is declared), [`os`](os.html#module-os "os: Miscellaneous operating system interfaces."), [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames."), [`tempfile`](tempfile.html#module-tempfile "tempfile: Generate temporary files and directories."),
    and [`shutil`](shutil.html#module-shutil "shutil: High-level file operations, including copying.").

    Raises an [auditing event](sys.html#auditing) `open` with arguments `path`, `mode`, `flags`.

    The `mode` and `flags` arguments may have been modified or inferred from
    the original call.

    Changed in version 3.3:

    * The *opener* parameter was added.
    * The `'x'` mode was added.
    * [`IOError`](exceptions.html#IOError "IOError") used to be raised, it is now an alias of [`OSError`](exceptions.html#OSError "OSError").
    * [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is now raised if the file opened in exclusive
      creation mode (`'x'`) already exists.

    Changed in version 3.5:

    * If the system call is interrupted and the signal handler does not raise an
      exception, the function now retries the system call instead of raising an
      [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).
    * The `'namereplace'` error handler was added.

    Changed in version 3.11: The `'U'` mode has been removed.