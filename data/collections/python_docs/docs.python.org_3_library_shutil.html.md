:   Recursively copy an entire directory tree rooted at *src* to a directory
    named *dst* and return the destination directory. All intermediate
    directories needed to contain *dst* will also be created by default.

    Permissions and times of directories are copied with [`copystat()`](#shutil.copystat "shutil.copystat"),
    individual files are copied using [`copy2()`](#shutil.copy2 "shutil.copy2").

    If *symlinks* is true, symbolic links in the source tree are represented as
    symbolic links in the new tree and the metadata of the original links will
    be copied as far as the platform allows; if false or omitted, the contents
    and metadata of the linked files are copied to the new tree.

    When *symlinks* is false, if the file pointed to by the symlink doesn’t
    exist, an exception will be added in the list of errors raised in
    an [`Error`](#shutil.Error "shutil.Error") exception at the end of the copy process.
    You can set the optional *ignore\_dangling\_symlinks* flag to true if you
    want to silence this exception. Notice that this option has no effect
    on platforms that don’t support [`os.symlink()`](os.html#os.symlink "os.symlink").

    If *ignore* is given, it must be a callable that will receive as its
    arguments the directory being visited by [`copytree()`](#shutil.copytree "shutil.copytree"), and a list of its
    contents, as returned by [`os.listdir()`](os.html#os.listdir "os.listdir"). Since [`copytree()`](#shutil.copytree "shutil.copytree") is
    called recursively, the *ignore* callable will be called once for each
    directory that is copied. The callable must return a sequence of directory
    and file names relative to the current directory (i.e. a subset of the items
    in its second argument); these names will then be ignored in the copy
    process. [`ignore_patterns()`](#shutil.ignore_patterns "shutil.ignore_patterns") can be used to create such a callable that
    ignores names based on glob-style patterns.

    If exception(s) occur, an [`Error`](#shutil.Error "shutil.Error") is raised with a list of reasons.

    If *copy\_function* is given, it must be a callable that will be used to copy
    each file. It will be called with the source path and the destination path
    as arguments. By default, [`copy2()`](#shutil.copy2 "shutil.copy2") is used, but any function
    that supports the same signature (like [`copy()`](#shutil.copy "shutil.copy")) can be used.

    If *dirs\_exist\_ok* is false (the default) and *dst* already exists, a
    [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is raised. If *dirs\_exist\_ok* is true, the copying
    operation will continue if it encounters existing directories, and files
    within the *dst* tree will be overwritten by corresponding files from the
    *src* tree.

    Raises an [auditing event](sys.html#auditing) `shutil.copytree` with arguments `src`, `dst`.

    Changed in version 3.2: Added the *copy\_function* argument to be able to provide a custom copy
    function.
    Added the *ignore\_dangling\_symlinks* argument to silence dangling symlinks
    errors when *symlinks* is false.

    Changed in version 3.3: Copy metadata when *symlinks* is false.
    Now returns *dst*.

    Changed in version 3.8: Added the *dirs\_exist\_ok* parameter.