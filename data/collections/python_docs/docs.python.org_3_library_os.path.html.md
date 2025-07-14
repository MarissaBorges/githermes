:   Return the canonical path of the specified filename, eliminating any symbolic
    links encountered in the path (if they are supported by the operating
    system). On Windows, this function will also resolve MS-DOS (also called 8.3)
    style names such as `C:\\PROGRA~1` to `C:\\Program Files`.

    By default, the path is evaluated up to the first component that does not
    exist, is a symlink loop, or whose evaluation raises [`OSError`](exceptions.html#OSError "OSError").
    All such components are appended unchanged to the existing part of the path.

    Some errors that are handled this way include “access denied”, “not a
    directory”, or “bad argument to internal function”. Thus, the
    resulting path may be missing or inaccessible, may still contain
    links or loops, and may traverse non-directories.

    This behavior can be modified by keyword arguments:

    If *strict* is `True`, the first error encountered when evaluating the path is
    re-raised.
    In particular, [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is raised if *path* does not exist,
    or another [`OSError`](exceptions.html#OSError "OSError") if it is otherwise inaccessible.

    If *strict* is [`os.path.ALLOW_MISSING`](#os.path.ALLOW_MISSING "os.path.ALLOW_MISSING"), errors other than
    [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") are re-raised (as with `strict=True`).
    Thus, the returned path will not contain any symbolic links, but the named
    file and some of its parent directories may be missing.

    Note

    This function emulates the operating system’s procedure for making a path
    canonical, which differs slightly between Windows and UNIX with respect
    to how links and subsequent path components interact.

    Operating system APIs make paths canonical as needed, so it’s not
    normally necessary to call this function.

    Changed in version 3.8: Symbolic links and junctions are now resolved on Windows.

    Changed in version 3.10: The *strict* parameter was added.

    Changed in version 3.13.4: The [`ALLOW_MISSING`](#os.path.ALLOW_MISSING "os.path.ALLOW_MISSING") value for the *strict* parameter
    was added.