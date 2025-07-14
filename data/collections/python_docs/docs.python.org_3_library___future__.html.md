`__future__` — Future statement definitions
===========================================

**Source code:** [Lib/\_\_future\_\_.py](https://github.com/python/cpython/tree/3.13/Lib/__future__.py)

---

Imports of the form `from __future__ import feature` are called
[future statements](../reference/simple_stmts.html#future). These are special-cased by the Python compiler
to allow the use of new Python features in modules containing the future statement
before the release in which the feature becomes standard.

While these future statements are given additional special meaning by the
Python compiler, they are still executed like any other import statement and
the [`__future__`](#module-__future__ "__future__: Future statement definitions") exists and is handled by the import system the same way
any other Python module would be. This design serves three purposes:

* To avoid confusing existing tools that analyze import statements and expect to
  find the modules they’re importing.
* To document when incompatible changes were introduced, and when they will be
  — or were — made mandatory. This is a form of executable documentation, and
  can be inspected programmatically via importing [`__future__`](#module-__future__ "__future__: Future statement definitions") and examining
  its contents.
* To ensure that [future statements](../reference/simple_stmts.html#future) run under releases prior to
  Python 2.1 at least yield runtime exceptions (the import of [`__future__`](#module-__future__ "__future__: Future statement definitions")
  will fail, because there was no module of that name prior to 2.1).

Module Contents
---------------

No feature description will ever be deleted from [`__future__`](#module-__future__ "__future__: Future statement definitions"). Since its
introduction in Python 2.1 the following features have found their way into the
language using this mechanism:

| feature | optional in | mandatory in | effect |
| --- | --- | --- | --- |
| nested\_scopes | 2.1.0b1 | 2.2 | [**PEP 227**](https://peps.python.org/pep-0227/): *Statically Nested Scopes* |
| generators | 2.2.0a1 | 2.3 | [**PEP 255**](https://peps.python.org/pep-0255/): *Simple Generators* |
| division | 2.2.0a2 | 3.0 | [**PEP 238**](https://peps.python.org/pep-0238/): *Changing the Division Operator* |
| absolute\_import | 2.5.0a1 | 3.0 | [**PEP 328**](https://peps.python.org/pep-0328/): *Imports: Multi-Line and Absolute/Relative* |
| with\_statement | 2.5.0a1 | 2.6 | [**PEP 343**](https://peps.python.org/pep-0343/): *The “with” Statement* |
| print\_function | 2.6.0a2 | 3.0 | [**PEP 3105**](https://peps.python.org/pep-3105/): *Make print a function* |
| unicode\_literals | 2.6.0a2 | 3.0 | [**PEP 3112**](https://peps.python.org/pep-3112/): *Bytes literals in Python 3000* |
| generator\_stop | 3.5.0b1 | 3.7 | [**PEP 479**](https://peps.python.org/pep-0479/): *StopIteration handling inside generators* |
| annotations | 3.7.0b1 | TBD | [**PEP 563**](https://peps.python.org/pep-0563/): *Postponed evaluation of annotations* |

*class* \_\_future\_\_.\_Feature
:   Each statement in `__future__.py` is of the form:

    Copy

    ```
    FeatureName = _Feature(OptionalRelease, MandatoryRelease,
                           CompilerFlag)

    ```

    where, normally, *OptionalRelease* is less than *MandatoryRelease*, and both are
    5-tuples of the same form as [`sys.version_info`](sys.html#sys.version_info "sys.version_info"):

    Copy

    ```
    (PY_MAJOR_VERSION, # the 2 in 2.1.0a3; an int
     PY_MINOR_VERSION, # the 1; an int
     PY_MICRO_VERSION, # the 0; an int
     PY_RELEASE_LEVEL, # "alpha", "beta", "candidate" or "final"; string
     PY_RELEASE_SERIAL # the 3; an int
    )

    ```

\_Feature.getOptionalRelease()
:   *OptionalRelease* records the first release in which the feature was accepted.

\_Feature.getMandatoryRelease()
:   In the case of a *MandatoryRelease* that has not yet occurred,
    *MandatoryRelease* predicts the release in which the feature will become part of
    the language.

    Else *MandatoryRelease* records when the feature became part of the language; in
    releases at or after that, modules no longer need a future statement to use the
    feature in question, but may continue to use such imports.

    *MandatoryRelease* may also be `None`, meaning that a planned feature got
    dropped or that it is not yet decided.

\_Feature.compiler\_flag
:   *CompilerFlag* is the (bitfield) flag that should be passed in the fourth
    argument to the built-in function [`compile()`](functions.html#compile "compile") to enable the feature in
    dynamically compiled code. This flag is stored in the [`_Feature.compiler_flag`](#future__._Feature.compiler_flag "__future__._Feature.compiler_flag")
    attribute on [`_Feature`](#future__._Feature "__future__._Feature") instances.

See also

[Future statements](../reference/simple_stmts.html#future)
:   How the compiler treats future imports.

[**PEP 236**](https://peps.python.org/pep-0236/) - Back to the \_\_future\_\_
:   The original proposal for the \_\_future\_\_ mechanism.