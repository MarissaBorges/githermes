:   Add headers and payload to *msg*:

    Add a header with a `maintype/subtype`
    value.

    * For `str`, set the MIME `maintype` to `text`, and set the
      subtype to *subtype* if it is specified, or `plain` if it is not.
    * For `bytes`, use the specified *maintype* and *subtype*, or
      raise a [`TypeError`](exceptions.html#TypeError "TypeError") if they are not specified.
    * For [`EmailMessage`](email.message.html#email.message.EmailMessage "email.message.EmailMessage") objects, set the maintype
      to `message`, and set the subtype to *subtype* if it is
      specified or `rfc822` if it is not. If *subtype* is
      `partial`, raise an error (`bytes` objects must be used to
      construct `message/partial` parts).

    If *charset* is provided (which is valid only for `str`), encode the
    string to bytes using the specified character set. The default is
    `utf-8`. If the specified *charset* is a known alias for a standard
    MIME charset name, use the standard charset instead.

    If *cte* is set, encode the payload using the specified content transfer
    encoding, and set the header to
    that value. Possible values for *cte* are `quoted-printable`,
    `base64`, `7bit`, `8bit`, and `binary`. If the input cannot be
    encoded in the specified encoding (for example, specifying a *cte* of
    `7bit` for an input that contains non-ASCII values), raise a
    [`ValueError`](exceptions.html#ValueError "ValueError").

    * For `str` objects, if *cte* is not set use heuristics to
      determine the most compact encoding. Prior to encoding,
      [`str.splitlines()`](stdtypes.html#str.splitlines "str.splitlines") is used to normalize all line boundaries,
      ensuring that each line of the payload is terminated by the
      current policy’s [`linesep`](email.policy.html#email.policy.Policy.linesep "email.policy.Policy.linesep") property
      (even if the original string did not end with one).
    * For `bytes` objects, *cte* is taken to be base64 if not set,
      and the aforementioned newline translation is not performed.
    * For [`EmailMessage`](email.message.html#email.message.EmailMessage "email.message.EmailMessage"), per [**RFC 2046**](https://datatracker.ietf.org/doc/html/rfc2046.html), raise
      an error if a *cte* of `quoted-printable` or `base64` is
      requested for *subtype* `rfc822`, and for any *cte* other than
      `7bit` for *subtype* `external-body`. For
      `message/rfc822`, use `8bit` if *cte* is not specified. For
      all other values of *subtype*, use `7bit`.

    Note

    A *cte* of `binary` does not actually work correctly yet.
    The `EmailMessage` object as modified by `set_content` is
    correct, but [`BytesGenerator`](email.generator.html#email.generator.BytesGenerator "email.generator.BytesGenerator") does not
    serialize it correctly.

    If *disposition* is set, use it as the value of the
    header. If not specified, and
    *filename* is specified, add the header with the value `attachment`.
    If *disposition* is not specified and *filename* is also not specified,
    do not add the header. The only valid values for *disposition* are
    `attachment` and `inline`.

    If *filename* is specified, use it as the value of the `filename`
    parameter of the header.

    If *cid* is specified, add a header with
    *cid* as its value.

    If *params* is specified, iterate its `items` method and use the
    resulting `(key, value)` pairs to set additional parameters on the
    header.

    If *headers* is specified and is a list of strings of the form
    `headername: headervalue` or a list of `header` objects
    (distinguished from strings by having a `name` attribute), add the
    headers to *msg*.