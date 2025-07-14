:   *Part of the [Stable ABI](stable.html#stable).*

    Register the error handling callback function *error* under the given *name*.
    This callback function will be called by a codec when it encounters
    unencodable characters/undecodable bytes and *name* is specified as the error
    parameter in the call to the encode/decode function.

    The callback gets a single argument, an instance of
    [`UnicodeEncodeError`](../library/exceptions.html#UnicodeEncodeError "UnicodeEncodeError"), [`UnicodeDecodeError`](../library/exceptions.html#UnicodeDecodeError "UnicodeDecodeError") or
    [`UnicodeTranslateError`](../library/exceptions.html#UnicodeTranslateError "UnicodeTranslateError") that holds information about the problematic
    sequence of characters or bytes and their offset in the original string (see
    [Unicode Exception Objects](exceptions.html#unicodeexceptions) for functions to extract this information). The
    callback must either raise the given exception, or return a two-item tuple
    containing the replacement for the problematic sequence, and an integer
    giving the offset in the original string at which encoding/decoding should be
    resumed.

    Return `0` on success, `-1` on error.