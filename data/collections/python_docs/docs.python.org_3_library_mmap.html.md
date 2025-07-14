:   **(Unix version)** Maps *length* bytes from the file specified by the file
    descriptor *fileno*, and returns a mmap object. If *length* is `0`, the
    maximum length of the map will be the current size of the file when
    [`mmap`](#mmap.mmap "mmap.mmap") is called.

    *flags* specifies the nature of the mapping. [`MAP_PRIVATE`](#mmap.MAP_PRIVATE "mmap.MAP_PRIVATE") creates a
    private copy-on-write mapping, so changes to the contents of the mmap
    object will be private to this process, and [`MAP_SHARED`](#mmap.MAP_SHARED "mmap.MAP_SHARED") creates a
    mapping that’s shared with all other processes mapping the same areas of
    the file. The default value is [`MAP_SHARED`](#mmap.MAP_SHARED "mmap.MAP_SHARED"). Some systems have
    additional possible flags with the full list specified in
    [MAP\_\* constants](#map-constants).

    *prot*, if specified, gives the desired memory protection; the two most
    useful values are `PROT_READ` and `PROT_WRITE`, to specify
    that the pages may be read or written. *prot* defaults to
    `PROT_READ | PROT_WRITE`.

    *access* may be specified in lieu of *flags* and *prot* as an optional
    keyword parameter. It is an error to specify both *flags*, *prot* and
    *access*. See the description of *access* above for information on how to
    use this parameter.

    *offset* may be specified as a non-negative integer offset. mmap references
    will be relative to the offset from the beginning of the file. *offset*
    defaults to 0. *offset* must be a multiple of `ALLOCATIONGRANULARITY`
    which is equal to `PAGESIZE` on Unix systems.

    If *trackfd* is `False`, the file descriptor specified by *fileno* will
    not be duplicated, and the resulting `mmap` object will not
    be associated with the map’s underlying file.
    This means that the [`size()`](#mmap.mmap.size "mmap.mmap.size") and [`resize()`](#mmap.mmap.resize "mmap.mmap.resize")
    methods will fail.
    This mode is useful to limit the number of open file descriptors.

    To ensure validity of the created memory mapping the file specified
    by the descriptor *fileno* is internally automatically synchronized
    with the physical backing store on macOS.

    Changed in version 3.13: The *trackfd* parameter was added.

    This example shows a simple way of using [`mmap`](#mmap.mmap "mmap.mmap"):

    Copy

    ```
    import mmap

    # write a simple example file
    with open("hello.txt", "wb") as f:
        f.write(b"Hello Python!\n")

    with open("hello.txt", "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        print(mm.readline())  # prints b"Hello Python!\n"
        # read content via slice notation
        print(mm[:5])  # prints b"Hello"
        # update content using slice notation;
        # note that new content must have same size
        mm[6:] = b" world!\n"
        # ... and read again using standard file methods
        mm.seek(0)
        print(mm.readline())  # prints b"Hello  world!\n"
        # close the map
        mm.close()

    ```

    [`mmap`](#mmap.mmap "mmap.mmap") can also be used as a context manager in a [`with`](../reference/compound_stmts.html#with)
    statement:

    Copy

    ```
    import mmap

    with mmap.mmap(-1, 13) as mm:
        mm.write(b"Hello world!")

    ```

    Added in version 3.2: Context manager support.

    The next example demonstrates how to create an anonymous map and exchange
    data between the parent and child processes:

    Copy

    ```
    import mmap
    import os

    mm = mmap.mmap(-1, 13)
    mm.write(b"Hello world!")

    pid = os.fork()

    if pid == 0:  # In a child process
        mm.seek(0)
        print(mm.readline())

        mm.close()

    ```

    Raises an [auditing event](sys.html#auditing) `mmap.__new__` with arguments `fileno`, `length`, `access`, `offset`.

    Memory-mapped file objects support the following methods:

    close()
    :   Closes the mmap. Subsequent calls to other methods of the object will
        result in a ValueError exception being raised. This will not close
        the open file.

    closed
    :   `True` if the file is closed.

    find(*sub*[, *start*[, *end*]])
    :   Returns the lowest index in the object where the subsequence *sub* is
        found, such that *sub* is contained in the range [*start*, *end*].
        Optional arguments *start* and *end* are interpreted as in slice notation.
        Returns `-1` on failure.

    flush([*offset*[, *size*]])
    :   Flushes changes made to the in-memory copy of a file back to disk. Without
        use of this call there is no guarantee that changes are written back before
        the object is destroyed. If *offset* and *size* are specified, only
        changes to the given range of bytes will be flushed to disk; otherwise, the
        whole extent of the mapping is flushed. *offset* must be a multiple of the
        `PAGESIZE` or `ALLOCATIONGRANULARITY`.

        `None` is returned to indicate success. An exception is raised when the
        call failed.

        Changed in version 3.8: Previously, a nonzero value was returned on success; zero was returned
        on error under Windows. A zero value was returned on success; an
        exception was raised on error under Unix.

    madvise(*option*[, *start*[, *length*]])
    :   Send advice *option* to the kernel about the memory region beginning at
        *start* and extending *length* bytes. *option* must be one of the
        [MADV\_\* constants](#madvise-constants) available on the system. If
        *start* and *length* are omitted, the entire mapping is spanned. On
        some systems (including Linux), *start* must be a multiple of the
        `PAGESIZE`.

        Availability: Systems with the `madvise()` system call.

    move(*dest*, *src*, *count*)
    :   Copy the *count* bytes starting at offset *src* to the destination index
        *dest*. If the mmap was created with `ACCESS_READ`, then calls to
        move will raise a [`TypeError`](exceptions.html#TypeError "TypeError") exception.

    read([*n*])
    :   Return a [`bytes`](stdtypes.html#bytes "bytes") containing up to *n* bytes starting from the
        current file position. If the argument is omitted, `None` or negative,
        return all bytes from the current file position to the end of the
        mapping. The file position is updated to point after the bytes that were
        returned.

        Changed in version 3.3: Argument can be omitted or `None`.

    read\_byte()
    :   Returns a byte at the current file position as an integer, and advances
        the file position by 1.

    readline()
    :   Returns a single line, starting at the current file position and up to the
        next newline. The file position is updated to point after the bytes that were
        returned.

    resize(*newsize*)
    :   Resizes the map and the underlying file, if any.

        Resizing a map created with *access* of `ACCESS_READ` or
        `ACCESS_COPY`, will raise a [`TypeError`](exceptions.html#TypeError "TypeError") exception.
        Resizing a map created with *trackfd* set to `False`,
        will raise a [`ValueError`](exceptions.html#ValueError "ValueError") exception.

        **On Windows**: Resizing the map will raise an [`OSError`](exceptions.html#OSError "OSError") if there are other
        maps against the same named file. Resizing an anonymous map (ie against the
        pagefile) will silently create a new map with the original data copied over
        up to the length of the new size.

        Changed in version 3.11: Correctly fails if attempting to resize when another map is held
        Allows resize against an anonymous map on Windows

    rfind(*sub*[, *start*[, *end*]])
    :   Returns the highest index in the object where the subsequence *sub* is
        found, such that *sub* is contained in the range [*start*, *end*].
        Optional arguments *start* and *end* are interpreted as in slice notation.
        Returns `-1` on failure.

    seek(*pos*[, *whence*])
    :   Set the file’s current position. *whence* argument is optional and
        defaults to `os.SEEK_SET` or `0` (absolute file positioning); other
        values are `os.SEEK_CUR` or `1` (seek relative to the current
        position) and `os.SEEK_END` or `2` (seek relative to the file’s end).

        Changed in version 3.13: Return the new absolute position instead of `None`.

    seekable()
    :   Return whether the file supports seeking, and the return value is always `True`.

    size()
    :   Return the length of the file, which can be larger than the size of the
        memory-mapped area.

    tell()
    :   Returns the current position of the file pointer.

    write(*bytes*)
    :   Write the bytes in *bytes* into memory at the current position of the
        file pointer and return the number of bytes written (never less than
        `len(bytes)`, since if the write fails, a [`ValueError`](exceptions.html#ValueError "ValueError") will be
        raised). The file position is updated to point after the bytes that
        were written. If the mmap was created with `ACCESS_READ`, then
        writing to it will raise a [`TypeError`](exceptions.html#TypeError "TypeError") exception.

        Changed in version 3.6: The number of bytes written is now returned.

    write\_byte(*byte*)
    :   Write the integer *byte* into memory at the current
        position of the file pointer; the file position is advanced by `1`. If
        the mmap was created with `ACCESS_READ`, then writing to it will
        raise a [`TypeError`](exceptions.html#TypeError "TypeError") exception.