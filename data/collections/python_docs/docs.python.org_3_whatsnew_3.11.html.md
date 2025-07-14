* Some macros have been converted to static inline functions to avoid
  [macro pitfalls](https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html).
  The change should be mostly transparent to users,
  as the replacement functions will cast their arguments to the expected types
  to avoid compiler warnings due to static type checks.
  However, when the limited C API is set to >=3.11,
  these casts are not done,
  and callers will need to cast arguments to their expected types.
  See [**PEP 670**](https://peps.python.org/pep-0670/) for more details.
  (Contributed by Victor Stinner and Erlend E. Aasland in [gh-89653](https://github.com/python/cpython/issues/89653).)
* [`PyErr_SetExcInfo()`](../c-api/exceptions.html#c.PyErr_SetExcInfo "PyErr_SetExcInfo") no longer uses the `type` and `traceback`
  arguments, the interpreter now derives those values from the exception
  instance (the `value` argument). The function still steals references
  of all three arguments.
  (Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
* [`PyErr_GetExcInfo()`](../c-api/exceptions.html#c.PyErr_GetExcInfo "PyErr_GetExcInfo") now derives the `type` and `traceback`
  fields of the result from the exception instance (the `value` field).
  (Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
* [`_frozen`](../c-api/import.html#c._frozen "_frozen") has a new `is_package` field to indicate whether
  or not the frozen module is a package. Previously, a negative value
  in the `size` field was the indicator. Now only non-negative values
  be used for `size`.
  (Contributed by Kumar Aditya in [bpo-46608](https://bugs.python.org/issue?@action=redirect&bpo=46608).)
* [`_PyFrameEvalFunction()`](../c-api/init.html#c._PyFrameEvalFunction "_PyFrameEvalFunction") now takes `_PyInterpreterFrame*`
  as its second parameter, instead of `PyFrameObject*`.
  See [**PEP 523**](https://peps.python.org/pep-0523/) for more details of how to use this function pointer type.
* `PyCode_New()` and `PyCode_NewWithPosOnlyArgs()` now take
  an additional `exception_table` argument.
  Using these functions should be avoided, if at all possible.
  To get a custom code object: create a code object using the compiler,
  then get a modified version with the `replace` method.
* [`PyCodeObject`](../c-api/code.html#c.PyCodeObject "PyCodeObject") no longer has the `co_code`, `co_varnames`,
  `co_cellvars` and `co_freevars` fields. Instead, use
  [`PyCode_GetCode()`](../c-api/code.html#c.PyCode_GetCode "PyCode_GetCode"), [`PyCode_GetVarnames()`](../c-api/code.html#c.PyCode_GetVarnames "PyCode_GetVarnames"),
  [`PyCode_GetCellvars()`](../c-api/code.html#c.PyCode_GetCellvars "PyCode_GetCellvars") and [`PyCode_GetFreevars()`](../c-api/code.html#c.PyCode_GetFreevars "PyCode_GetFreevars") respectively
  to access them via the C API.
  (Contributed by Brandt Bucher in [bpo-46841](https://bugs.python.org/issue?@action=redirect&bpo=46841) and Ken Jin in [gh-92154](https://github.com/python/cpython/issues/92154)
  and [gh-94936](https://github.com/python/cpython/issues/94936).)
* The old trashcan macros (`Py_TRASHCAN_SAFE_BEGIN`/`Py_TRASHCAN_SAFE_END`)
  are now deprecated. They should be replaced by the new macros
  `Py_TRASHCAN_BEGIN` and `Py_TRASHCAN_END`.

  A tp\_dealloc function that has the old macros, such as:

  Copy

  ```
  static void
  mytype_dealloc(mytype *p)
  {
      PyObject_GC_UnTrack(p);
      Py_TRASHCAN_SAFE_BEGIN(p);
      ...
      Py_TRASHCAN_SAFE_END
  }

  ```

  should migrate to the new macros as follows:

  Copy

  ```
  static void
  mytype_dealloc(mytype *p)
  {
      PyObject_GC_UnTrack(p);
      Py_TRASHCAN_BEGIN(p, mytype_dealloc)
      ...
      Py_TRASHCAN_END
  }

  ```

  Note that `Py_TRASHCAN_BEGIN` has a second argument which
  should be the deallocation function it is in.

  To support older Python versions in the same codebase, you
  can define the following macros and use them throughout
  the code (credit: these were copied from the `mypy` codebase):

  Copy

  ```
  #if PY_VERSION_HEX >= 0x03080000
  #  define CPy_TRASHCAN_BEGIN(op, dealloc) Py_TRASHCAN_BEGIN(op, dealloc)
  #  define CPy_TRASHCAN_END(op) Py_TRASHCAN_END
  #else
  #  define CPy_TRASHCAN_BEGIN(op, dealloc) Py_TRASHCAN_SAFE_BEGIN(op)
  #  define CPy_TRASHCAN_END(op) Py_TRASHCAN_SAFE_END(op)
  #endif

  ```
* The [`PyType_Ready()`](../c-api/type.html#c.PyType_Ready "PyType_Ready") function now raises an error if a type is defined
  with the [`Py_TPFLAGS_HAVE_GC`](../c-api/typeobj.html#c.Py_TPFLAGS_HAVE_GC "Py_TPFLAGS_HAVE_GC") flag set but has no traverse function
  ([`PyTypeObject.tp_traverse`](../c-api/typeobj.html#c.PyTypeObject.tp_traverse "PyTypeObject.tp_traverse")).
  (Contributed by Victor Stinner in [bpo-44263](https://bugs.python.org/issue?@action=redirect&bpo=44263).)
* Heap types with the [`Py_TPFLAGS_IMMUTABLETYPE`](../c-api/typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE "Py_TPFLAGS_IMMUTABLETYPE") flag can now inherit
  the [**PEP 590**](https://peps.python.org/pep-0590/) vectorcall protocol. Previously, this was only possible for
  [static types](../c-api/typeobj.html#static-types).
  (Contributed by Erlend E. Aasland in [bpo-43908](https://bugs.python.org/issue?@action=redirect&bpo=43908))
* Since [`Py_TYPE()`](../c-api/structures.html#c.Py_TYPE "Py_TYPE") is changed to a inline static function,
  `Py_TYPE(obj) = new_type` must be replaced with
  `Py_SET_TYPE(obj, new_type)`: see the [`Py_SET_TYPE()`](../c-api/structures.html#c.Py_SET_TYPE "Py_SET_TYPE") function
  (available since Python 3.9). For backward compatibility, this macro can be
  used:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030900A4 && !defined(Py_SET_TYPE)
  static inline void _Py_SET_TYPE(PyObject *ob, PyTypeObject *type)
  { ob->ob_type = type; }
  #define Py_SET_TYPE(ob, type) _Py_SET_TYPE((PyObject*)(ob), type)
  #endif

  ```

  (Contributed by Victor Stinner in [bpo-39573](https://bugs.python.org/issue?@action=redirect&bpo=39573).)
* Since [`Py_SIZE()`](../c-api/structures.html#c.Py_SIZE "Py_SIZE") is changed to a inline static function,
  `Py_SIZE(obj) = new_size` must be replaced with
  `Py_SET_SIZE(obj, new_size)`: see the [`Py_SET_SIZE()`](../c-api/structures.html#c.Py_SET_SIZE "Py_SET_SIZE") function
  (available since Python 3.9). For backward compatibility, this macro can be
  used:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030900A4 && !defined(Py_SET_SIZE)
  static inline void _Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size)
  { ob->ob_size = size; }
  #define Py_SET_SIZE(ob, size) _Py_SET_SIZE((PyVarObject*)(ob), size)
  #endif

  ```

  (Contributed by Victor Stinner in [bpo-39573](https://bugs.python.org/issue?@action=redirect&bpo=39573).)
* `<Python.h>` no longer includes the header files `<stdlib.h>`,
  `<stdio.h>`, `<errno.h>` and `<string.h>` when the `Py_LIMITED_API`
  macro is set to `0x030b0000` (Python 3.11) or higher. C extensions should
  explicitly include the header files after `#include <Python.h>`.
  (Contributed by Victor Stinner in [bpo-45434](https://bugs.python.org/issue?@action=redirect&bpo=45434).)
* The non-limited API files `cellobject.h`, `classobject.h`, `code.h`, `context.h`,
  `funcobject.h`, `genobject.h` and `longintrepr.h` have been moved to
  the `Include/cpython` directory. Moreover, the `eval.h` header file was
  removed. These files must not be included directly, as they are already
  included in `Python.h`: [Include Files](../c-api/intro.html#api-includes). If they have
  been included directly, consider including `Python.h` instead.
  (Contributed by Victor Stinner in [bpo-35134](https://bugs.python.org/issue?@action=redirect&bpo=35134).)
* The `PyUnicode_CHECK_INTERNED()` macro has been excluded from the
  limited C API. It was never usable there, because it used internal structures
  which are not available in the limited C API.
  (Contributed by Victor Stinner in [bpo-46007](https://bugs.python.org/issue?@action=redirect&bpo=46007).)
* The following frame functions and type are now directly available with
  `#include <Python.h>`, it’s no longer needed to add
  `#include <frameobject.h>`:

  (Contributed by Victor Stinner in [gh-93937](https://github.com/python/cpython/issues/93937).)

* The [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject "PyFrameObject") structure members have been removed from the
  public C API.

  While the documentation notes that the [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject "PyFrameObject") fields are
  subject to change at any time, they have been stable for a long time and were
  used in several popular extensions.

  In Python 3.11, the frame struct was reorganized to allow performance
  optimizations. Some fields were removed entirely, as they were details of the
  old implementation.

  [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject "PyFrameObject") fields:

  The Python frame object is now created lazily. A side effect is that the
  [`f_back`](../reference/datamodel.html#frame.f_back "frame.f_back") member must not be accessed directly,
  since its value is now also
  computed lazily. The [`PyFrame_GetBack()`](../c-api/frame.html#c.PyFrame_GetBack "PyFrame_GetBack") function must be called
  instead.

  Debuggers that accessed the [`f_locals`](../reference/datamodel.html#frame.f_locals "frame.f_locals") directly *must* call
  [`PyFrame_GetLocals()`](../c-api/frame.html#c.PyFrame_GetLocals "PyFrame_GetLocals") instead. They no longer need to call
  `PyFrame_FastToLocalsWithError()` or `PyFrame_LocalsToFast()`,
  in fact they should not call those functions. The necessary updating of the
  frame is now managed by the virtual machine.

  Code defining `PyFrame_GetCode()` on Python 3.8 and older:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030900B1
  static inline PyCodeObject* PyFrame_GetCode(PyFrameObject *frame)
  {
      Py_INCREF(frame->f_code);
      return frame->f_code;
  }
  #endif

  ```

  Code defining `PyFrame_GetBack()` on Python 3.8 and older:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030900B1
  static inline PyFrameObject* PyFrame_GetBack(PyFrameObject *frame)
  {
      Py_XINCREF(frame->f_back);
      return frame->f_back;
  }
  #endif

  ```

  Or use the [pythoncapi\_compat project](https://github.com/python/pythoncapi-compat) to get these two
  functions on older Python versions.
* Changes of the [`PyThreadState`](../c-api/init.html#c.PyThreadState "PyThreadState") structure members:

  Code defining `PyThreadState_GetFrame()` on Python 3.8 and older:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030900B1
  static inline PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate)
  {
      Py_XINCREF(tstate->frame);
      return tstate->frame;
  }
  #endif

  ```

  Code defining `PyThreadState_EnterTracing()` and
  `PyThreadState_LeaveTracing()` on Python 3.10 and older:

  Copy

  ```
  #if PY_VERSION_HEX < 0x030B00A2
  static inline void PyThreadState_EnterTracing(PyThreadState *tstate)
  {
      tstate->tracing++;
  #if PY_VERSION_HEX >= 0x030A00A1
      tstate->cframe->use_tracing = 0;
  #else
      tstate->use_tracing = 0;
  #endif
  }

  static inline void PyThreadState_LeaveTracing(PyThreadState *tstate)
  {
      int use_tracing = (tstate->c_tracefunc != NULL || tstate->c_profilefunc != NULL);
      tstate->tracing--;
  #if PY_VERSION_HEX >= 0x030A00A1
      tstate->cframe->use_tracing = use_tracing;
  #else
      tstate->use_tracing = use_tracing;
  #endif
  }
  #endif

  ```

  Or use [the pythoncapi-compat project](https://github.com/python/pythoncapi-compat) to get these functions
  on old Python functions.
* Distributors are encouraged to build Python with the optimized Blake2
  library [libb2](https://www.blake2.net/).
* The [`PyConfig.module_search_paths_set`](../c-api/init_config.html#c.PyConfig.module_search_paths_set "PyConfig.module_search_paths_set") field must now be set to 1 for
  initialization to use [`PyConfig.module_search_paths`](../c-api/init_config.html#c.PyConfig.module_search_paths "PyConfig.module_search_paths") to initialize
  [`sys.path`](../library/sys.html#sys.path "sys.path"). Otherwise, initialization will recalculate the path and replace
  any values added to `module_search_paths`.
* [`PyConfig_Read()`](../c-api/init_config.html#c.PyConfig_Read "PyConfig_Read") no longer calculates the initial search path, and will not
  fill any values into [`PyConfig.module_search_paths`](../c-api/init_config.html#c.PyConfig.module_search_paths "PyConfig.module_search_paths"). To calculate default
  paths and then modify them, finish initialization and use [`PySys_GetObject()`](../c-api/sys.html#c.PySys_GetObject "PySys_GetObject")
  to retrieve [`sys.path`](../library/sys.html#sys.path "sys.path") as a Python list object and modify it directly.