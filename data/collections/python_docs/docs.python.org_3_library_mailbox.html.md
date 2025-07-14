:   A subclass of [`Mailbox`](#mailbox.Mailbox "mailbox.Mailbox") for mailboxes in Maildir format. Parameter
    *factory* is a callable object that accepts a file-like message representation
    (which behaves as if opened in binary mode) and returns a custom representation.
    If *factory* is `None`, [`MaildirMessage`](#mailbox.MaildirMessage "mailbox.MaildirMessage") is used as the default message
    representation. If *create* is `True`, the mailbox is created if it does not
    exist.

    If *create* is `True` and the *dirname* path exists, it will be treated as
    an existing maildir without attempting to verify its directory layout.

    It is for historical reasons that *dirname* is named as such rather than *path*.

    Maildir is a directory-based mailbox format invented for the qmail mail
    transfer agent and now widely supported by other programs. Messages in a
    Maildir mailbox are stored in separate files within a common directory
    structure. This design allows Maildir mailboxes to be accessed and modified
    by multiple unrelated programs without data corruption, so file locking is
    unnecessary.

    Maildir mailboxes contain three subdirectories, namely: `tmp`,
    `new`, and `cur`. Messages are created momentarily in the
    `tmp` subdirectory and then moved to the `new` subdirectory to
    finalize delivery. A mail user agent may subsequently move the message to the
    `cur` subdirectory and store information about the state of the message
    in a special “info” section appended to its file name.

    Folders of the style introduced by the Courier mail transfer agent are also
    supported. Any subdirectory of the main mailbox is considered a folder if
    `'.'` is the first character in its name. Folder names are represented by
    `Maildir` without the leading `'.'`. Each folder is itself a Maildir
    mailbox but should not contain other folders. Instead, a logical nesting is
    indicated using `'.'` to delimit levels, e.g., “Archived.2005.07”.

    colon
    :   The Maildir specification requires the use of a colon (`':'`) in certain
        message file names. However, some operating systems do not permit this
        character in file names, If you wish to use a Maildir-like format on such
        an operating system, you should specify another character to use
        instead. The exclamation point (`'!'`) is a popular choice. For
        example:

        Copy

        ```
        import mailbox
        mailbox.Maildir.colon = '!'

        ```

        The `colon` attribute may also be set on a per-instance basis.

    Changed in version 3.13: [`Maildir`](#mailbox.Maildir "mailbox.Maildir") now ignores files with a leading dot.

    `Maildir` instances have all of the methods of [`Mailbox`](#mailbox.Mailbox "mailbox.Mailbox") in
    addition to the following:

    list\_folders()
    :   Return a list of the names of all folders.

    get\_folder(*folder*)
    :   Return a `Maildir` instance representing the folder whose name is
        *folder*. A [`NoSuchMailboxError`](#mailbox.NoSuchMailboxError "mailbox.NoSuchMailboxError") exception is raised if the folder
        does not exist.

    add\_folder(*folder*)
    :   Create a folder whose name is *folder* and return a `Maildir`
        instance representing it.

    remove\_folder(*folder*)
    :   Delete the folder whose name is *folder*. If the folder contains any
        messages, a [`NotEmptyError`](#mailbox.NotEmptyError "mailbox.NotEmptyError") exception will be raised and the folder
        will not be deleted.

    clean()
    :   Delete temporary files from the mailbox that have not been accessed in the
        last 36 hours. The Maildir specification says that mail-reading programs
        should do this occasionally.

    get\_flags(*key*)
    :   Return as a string the flags that are set on the message
        corresponding to *key*.
        This is the same as `get_message(key).get_flags()` but much
        faster, because it does not open the message file.
        Use this method when iterating over the keys to determine which
        messages are interesting to get.

        If you do have a [`MaildirMessage`](#mailbox.MaildirMessage "mailbox.MaildirMessage") object, use
        its [`get_flags()`](#mailbox.MaildirMessage.get_flags "mailbox.MaildirMessage.get_flags") method instead, because
        changes made by the message’s [`set_flags()`](#mailbox.MaildirMessage.set_flags "mailbox.MaildirMessage.set_flags"),
        [`add_flag()`](#mailbox.MaildirMessage.add_flag "mailbox.MaildirMessage.add_flag") and [`remove_flag()`](#mailbox.MaildirMessage.remove_flag "mailbox.MaildirMessage.remove_flag")
        methods are not reflected here until the mailbox’s
        [`__setitem__()`](#mailbox.Maildir.__setitem__ "mailbox.Maildir.__setitem__") method is called.

    set\_flags(*key*, *flags*)
    :   On the message corresponding to *key*, set the flags specified
        by *flags* and unset all others.
        Calling `some_mailbox.set_flags(key, flags)` is similar to

        Copy

        ```
        one_message = some_mailbox.get_message(key)
        one_message.set_flags(flags)
        some_mailbox[key] = one_message

        ```

        but faster, because it does not open the message file.

        If you do have a [`MaildirMessage`](#mailbox.MaildirMessage "mailbox.MaildirMessage") object, use
        its [`set_flags()`](#mailbox.MaildirMessage.set_flags "mailbox.MaildirMessage.set_flags") method instead, because
        changes made with this mailbox method will not be visible to the
        message object’s method, [`get_flags()`](#mailbox.MaildirMessage.get_flags "mailbox.MaildirMessage.get_flags").

    add\_flag(*key*, *flag*)
    :   On the message corresponding to *key*, set the flags specified
        by *flag* without changing other flags. To add more than one
        flag at a time, *flag* may be a string of more than one character.

        Considerations for using this method versus the message object’s
        [`add_flag()`](#mailbox.MaildirMessage.add_flag "mailbox.MaildirMessage.add_flag") method are similar to
        those for [`set_flags()`](#mailbox.Maildir.set_flags "mailbox.Maildir.set_flags"); see the discussion there.

    remove\_flag(*key*, *flag*)
    :   On the message corresponding to *key*, unset the flags specified
        by *flag* without changing other flags. To remove more than one
        flag at a time, *flag* may be a string of more than one character.

        Considerations for using this method versus the message object’s
        [`remove_flag()`](#mailbox.MaildirMessage.remove_flag "mailbox.MaildirMessage.remove_flag") method are similar to
        those for [`set_flags()`](#mailbox.Maildir.set_flags "mailbox.Maildir.set_flags"); see the discussion there.

    get\_info(*key*)
    :   Return a string containing the info for the message
        corresponding to *key*.
        This is the same as `get_message(key).get_info()` but much
        faster, because it does not open the message file.
        Use this method when iterating over the keys to determine which
        messages are interesting to get.

        If you do have a [`MaildirMessage`](#mailbox.MaildirMessage "mailbox.MaildirMessage") object, use
        its [`get_info()`](#mailbox.MaildirMessage.get_info "mailbox.MaildirMessage.get_info") method instead, because
        changes made by the message’s [`set_info()`](#mailbox.MaildirMessage.set_info "mailbox.MaildirMessage.set_info") method
        are not reflected here until the mailbox’s [`__setitem__()`](#mailbox.Maildir.__setitem__ "mailbox.Maildir.__setitem__") method
        is called.

    set\_info(*key*, *info*)
    :   Set the info of the message corresponding to *key* to *info*.
        Calling `some_mailbox.set_info(key, flags)` is similar to

        Copy

        ```
        one_message = some_mailbox.get_message(key)
        one_message.set_info(info)
        some_mailbox[key] = one_message

        ```

        but faster, because it does not open the message file.

        If you do have a [`MaildirMessage`](#mailbox.MaildirMessage "mailbox.MaildirMessage") object, use
        its [`set_info()`](#mailbox.MaildirMessage.set_info "mailbox.MaildirMessage.set_info") method instead, because
        changes made with this mailbox method will not be visible to the
        message object’s method, [`get_info()`](#mailbox.MaildirMessage.get_info "mailbox.MaildirMessage.get_info").

    Some [`Mailbox`](#mailbox.Mailbox "mailbox.Mailbox") methods implemented by `Maildir` deserve special
    remarks:

    add(*message*)

    \_\_setitem\_\_(*key*, *message*)

    update(*arg*)
    :   Warning

        These methods generate unique file names based upon the current process
        ID. When using multiple threads, undetected name clashes may occur and
        cause corruption of the mailbox unless threads are coordinated to avoid
        using these methods to manipulate the same mailbox simultaneously.

    flush()
    :   All changes to Maildir mailboxes are immediately applied, so this method
        does nothing.

    lock()

    unlock()
    :   Maildir mailboxes do not support (or require) locking, so these methods do
        nothing.

    close()
    :   `Maildir` instances do not keep any open files and the underlying
        mailboxes do not support locking, so this method does nothing.

    get\_file(*key*)
    :   Depending upon the host platform, it may not be possible to modify or
        remove the underlying message while the returned file remains open.