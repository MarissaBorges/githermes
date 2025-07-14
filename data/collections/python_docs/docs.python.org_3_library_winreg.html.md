:   Creates or opens the specified key, returning a
    [handle object](#handle-object).

    *key* is an already open key, or one of the predefined
    [HKEY\_\* constants](#hkey-constants).

    *sub\_key* is a string that names the key this method opens or creates.

    *reserved* is a reserved integer, and must be zero. The default is zero.

    *access* is an integer that specifies an access mask that describes the desired
    security access for the key. Default is [`KEY_WRITE`](#winreg.KEY_WRITE "winreg.KEY_WRITE"). See
    [Access Rights](#access-rights) for other allowed values.

    If *key* is one of the predefined keys, *sub\_key* may be `None`. In that
    case, the handle returned is the same key handle passed in to the function.

    If the key already exists, this function opens the existing key.

    The return value is the handle of the opened key. If the function fails, an
    [`OSError`](exceptions.html#OSError "OSError") exception is raised.

    Raises an [auditing event](sys.html#auditing) `winreg.CreateKey` with arguments `key`, `sub_key`, `access`.

    Raises an [auditing event](sys.html#auditing) `winreg.OpenKey/result` with argument `key`.

    Changed in version 3.3: See [above](#exception-changed).