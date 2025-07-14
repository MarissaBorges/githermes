`keyword` — Testing for Python keywords
=======================================

**Source code:** [Lib/keyword.py](https://github.com/python/cpython/tree/3.13/Lib/keyword.py)

---

This module allows a Python program to determine if a string is a
[keyword](../reference/lexical_analysis.html#keywords) or [soft keyword](../reference/lexical_analysis.html#soft-keywords).

keyword.iskeyword(*s*)
:   Return `True` if *s* is a Python [keyword](../reference/lexical_analysis.html#keywords).

keyword.kwlist
:   Sequence containing all the [keywords](../reference/lexical_analysis.html#keywords) defined for the
    interpreter. If any keywords are defined to only be active when particular
    [`__future__`](__future__.html#module-__future__ "__future__: Future statement definitions") statements are in effect, these will be included as well.

keyword.issoftkeyword(*s*)
:   Return `True` if *s* is a Python [soft keyword](../reference/lexical_analysis.html#soft-keywords).

keyword.softkwlist
:   Sequence containing all the [soft keywords](../reference/lexical_analysis.html#soft-keywords) defined for the
    interpreter. If any soft keywords are defined to only be active when particular
    [`__future__`](__future__.html#module-__future__ "__future__: Future statement definitions") statements are in effect, these will be included as well.