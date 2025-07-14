`token` — Constants used with Python parse trees
================================================

**Source code:** [Lib/token.py](https://github.com/python/cpython/tree/3.13/Lib/token.py)

---

This module provides constants which represent the numeric values of leaf nodes
of the parse tree (terminal tokens). Refer to the file `Grammar/Tokens`
in the Python distribution for the definitions of the names in the context of
the language grammar. The specific numeric values which the names map to may
change between Python versions.

The module also provides a mapping from numeric codes to names and some
functions. The functions mirror definitions in the Python C header files.

Note that a token’s value may depend on tokenizer options. For example, a
`"+"` token may be reported as either [`PLUS`](#token.PLUS "token.PLUS") or [`OP`](#token.OP "token.OP"), or
a `"match"` token may be either [`NAME`](#token.NAME "token.NAME") or [`SOFT_KEYWORD`](#token.SOFT_KEYWORD "token.SOFT_KEYWORD").

token.tok\_name
:   Dictionary mapping the numeric values of the constants defined in this module
    back to name strings, allowing more human-readable representation of parse trees
    to be generated.

token.ISTERMINAL(*x*)
:   Return `True` for terminal token values.

token.ISNONTERMINAL(*x*)
:   Return `True` for non-terminal token values.

token.ISEOF(*x*)
:   Return `True` if *x* is the marker indicating the end of input.

The token constants are:

token.NAME
:   Token value that indicates an [identifier](../reference/lexical_analysis.html#identifiers).
    Note that keywords are also initially tokenized as `NAME` tokens.

token.NUMBER
:   Token value that indicates a [numeric literal](../reference/lexical_analysis.html#numbers)

token.STRING
:   Token value that indicates a [string or byte literal](../reference/lexical_analysis.html#strings),
    excluding [formatted string literals](../reference/lexical_analysis.html#f-strings).
    The token string is not interpreted:
    it includes the surrounding quotation marks and the prefix (if given);
    backslashes are included literally, without processing escape sequences.

token.OP
:   A generic token value that indicates an
    [operator](../reference/lexical_analysis.html#operators) or [delimiter](../reference/lexical_analysis.html#delimiters).

    **CPython implementation detail:** This value is only reported by the [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module.
    Internally, the tokenizer uses
    [exact token types](#token-operators-delimiters) instead.

:   Token value used to indicate a comment.
    The parser ignores `COMMENT` tokens.

token.NEWLINE
:   Token value that indicates the end of a [logical line](../reference/lexical_analysis.html#logical-lines).

token.NL
:   Token value used to indicate a non-terminating newline.
    `NL` tokens are generated when a logical line of code is continued
    over multiple physical lines. The parser ignores `NL` tokens.

token.INDENT
:   Token value used at the beginning of a [logical line](../reference/lexical_analysis.html#logical-lines)
    to indicate the start of an [indented block](../reference/lexical_analysis.html#indentation).

token.DEDENT
:   Token value used at the beginning of a [logical line](../reference/lexical_analysis.html#logical-lines)
    to indicate the end of an [indented block](../reference/lexical_analysis.html#indentation).

token.FSTRING\_START
:   Token value used to indicate the beginning of an
    [f-string literal](../reference/lexical_analysis.html#f-strings).

    **CPython implementation detail:** The token string includes the prefix and the opening quote(s), but none
    of the contents of the literal.

token.FSTRING\_MIDDLE
:   Token value used for literal text inside an [f-string literal](../reference/lexical_analysis.html#f-strings),
    including format specifications.

    **CPython implementation detail:** Replacement fields (that is, the non-literal parts of f-strings) use
    the same tokens as other expressions, and are delimited by
    [`LBRACE`](#token.LBRACE "token.LBRACE"), [`RBRACE`](#token.RBRACE "token.RBRACE"), [`EXCLAMATION`](#token.EXCLAMATION "token.EXCLAMATION") and [`COLON`](#token.COLON "token.COLON")
    tokens.

token.FSTRING\_END
:   Token value used to indicate the end of a [f-string](../reference/lexical_analysis.html#f-strings).

    **CPython implementation detail:** The token string contains the closing quote(s).

token.ENDMARKER
:   Token value that indicates the end of input.

token.ENCODING
:   Token value that indicates the encoding used to decode the source bytes
    into text. The first token returned by [`tokenize.tokenize()`](tokenize.html#tokenize.tokenize "tokenize.tokenize") will
    always be an `ENCODING` token.

    **CPython implementation detail:** This token type isn’t used by the C tokenizer but is needed for
    the [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module.

The following token types are not produced by the [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module,
and are defined for special uses in the tokenizer or parser:

token.TYPE\_IGNORE
:   Token value indicating that a `type: ignore` comment was recognized.
    Such tokens are produced instead of regular [`COMMENT`](#token.COMMENT "token.COMMENT") tokens only
    with the [`PyCF_TYPE_COMMENTS`](ast.html#ast.PyCF_TYPE_COMMENTS "ast.PyCF_TYPE_COMMENTS") flag.

:   Token value indicating that a type comment was recognized.
    Such tokens are produced instead of regular [`COMMENT`](#token.COMMENT "token.COMMENT") tokens only
    with the [`PyCF_TYPE_COMMENTS`](ast.html#ast.PyCF_TYPE_COMMENTS "ast.PyCF_TYPE_COMMENTS") flag.

token.SOFT\_KEYWORD
:   Token value indicating a [soft keyword](../reference/lexical_analysis.html#soft-keywords).

    The tokenizer never produces this value.
    To check for a soft keyword, pass a [`NAME`](#token.NAME "token.NAME") token’s string to
    [`keyword.issoftkeyword()`](keyword.html#keyword.issoftkeyword "keyword.issoftkeyword").

token.ERRORTOKEN
:   Token value used to indicate wrong input.

    The [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module generally indicates errors by
    raising exceptions instead of emitting this token.
    It can also emit tokens such as [`OP`](#token.OP "token.OP") or [`NAME`](#token.NAME "token.NAME") with strings that
    are later rejected by the parser.

The remaining tokens represent specific [operators](../reference/lexical_analysis.html#operators) and
[delimiters](../reference/lexical_analysis.html#delimiters).
(The [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module reports these as [`OP`](#token.OP "token.OP"); see `exact_type`
in the [`tokenize`](tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") documentation for details.)

| Token | Value |
| --- | --- |
| token.LPAR | `"("` |
| token.RPAR | `")"` |
| token.LSQB | `"["` |
| token.RSQB | `"]"` |
| token.COLON | `":"` |
| token.COMMA | `","` |
| token.SEMI | `";"` |
| token.PLUS | `"+"` |
| token.MINUS | `"-"` |
| token.STAR | `"*"` |
| token.SLASH | `"/"` |
| token.VBAR | `"|"` |
| token.AMPER | `"&"` |
| token.LESS | `"<"` |
| token.GREATER | `">"` |
| token.EQUAL | `"="` |
| token.DOT | `"."` |
| token.PERCENT | `"%"` |
| token.LBRACE | `"{"` |
| token.RBRACE | `"}"` |
| token.EQEQUAL | `"=="` |
| token.NOTEQUAL | `"!="` |
| token.LESSEQUAL | `"<="` |
| token.GREATEREQUAL | `">="` |
| token.TILDE | `"~"` |
| token.CIRCUMFLEX | `"^"` |
| token.LEFTSHIFT | `"<<"` |
| token.RIGHTSHIFT | `">>"` |
| token.DOUBLESTAR | `"**"` |
| token.PLUSEQUAL | `"+="` |
| token.MINEQUAL | `"-="` |
| token.STAREQUAL | `"*="` |
| token.SLASHEQUAL | `"/="` |
| token.PERCENTEQUAL | `"%="` |
| token.AMPEREQUAL | `"&="` |
| token.VBAREQUAL | `"|="` |
| token.CIRCUMFLEXEQUAL | `"^="` |
| token.LEFTSHIFTEQUAL | `"<<="` |
| token.RIGHTSHIFTEQUAL | `">>="` |
| token.DOUBLESTAREQUAL | `"**="` |
| token.DOUBLESLASH | `"//"` |
| token.DOUBLESLASHEQUAL | `"//="` |
| token.AT | `"@"` |
| token.ATEQUAL | `"@="` |
| token.RARROW | `"->"` |
| token.ELLIPSIS | `"..."` |
| token.COLONEQUAL | `":="` |
| token.EXCLAMATION | `"!"` |

The following non-token constants are provided:

token.N\_TOKENS
:   The number of token types defined in this module.

token.EXACT\_TOKEN\_TYPES
:   A dictionary mapping the string representation of a token to its numeric code.

Changed in version 3.5: Added `AWAIT` and `ASYNC` tokens.

Changed in version 3.7: Removed `AWAIT` and `ASYNC` tokens. “async” and “await” are
now tokenized as [`NAME`](#token.NAME "token.NAME") tokens.

Changed in version 3.13: Removed `AWAIT` and `ASYNC` tokens again.