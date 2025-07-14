DateTime Objects
================

Various date and time objects are supplied by the [`datetime`](../library/datetime.html#module-datetime "datetime: Basic date and time types.") module.
Before using any of these functions, the header file `datetime.h` must be
included in your source (note that this is not included by `Python.h`),
and the macro `PyDateTime_IMPORT` must be invoked, usually as part of
the module initialisation function. The macro puts a pointer to a C structure
into a static variable, `PyDateTimeAPI`, that is used by the following
macros.

type PyDateTime\_Date
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python date object.

type PyDateTime\_DateTime
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python datetime object.

type PyDateTime\_Time
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents a Python time object.

type PyDateTime\_Delta
:   This subtype of [`PyObject`](structures.html#c.PyObject "PyObject") represents the difference between two datetime values.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyDateTime\_DateType
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python date type;
    it is the same object as [`datetime.date`](../library/datetime.html#datetime.date "datetime.date") in the Python layer.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyDateTime\_DateTimeType
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python datetime type;
    it is the same object as [`datetime.datetime`](../library/datetime.html#datetime.datetime "datetime.datetime") in the Python layer.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyDateTime\_TimeType
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python time type;
    it is the same object as [`datetime.time`](../library/datetime.html#datetime.time "datetime.time") in the Python layer.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyDateTime\_DeltaType
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents Python type for
    the difference between two datetime values;
    it is the same object as [`datetime.timedelta`](../library/datetime.html#datetime.timedelta "datetime.timedelta") in the Python layer.

[PyTypeObject](type.html#c.PyTypeObject "PyTypeObject") PyDateTime\_TZInfoType
:   This instance of [`PyTypeObject`](type.html#c.PyTypeObject "PyTypeObject") represents the Python time zone info type;
    it is the same object as [`datetime.tzinfo`](../library/datetime.html#datetime.tzinfo "datetime.tzinfo") in the Python layer.

Macro for access to the UTC singleton:

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_TimeZone\_UTC
:   Returns the time zone singleton representing UTC, the same object as
    [`datetime.timezone.utc`](../library/datetime.html#datetime.timezone.utc "datetime.timezone.utc").

Type-check macros:

int PyDate\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DateType`](#c.PyDateTime_DateType "PyDateTime_DateType") or a subtype of
    `PyDateTime_DateType`. *ob* must not be `NULL`. This function always
    succeeds.

int PyDate\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DateType`](#c.PyDateTime_DateType "PyDateTime_DateType"). *ob* must not be
    `NULL`. This function always succeeds.

int PyDateTime\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DateTimeType`](#c.PyDateTime_DateTimeType "PyDateTime_DateTimeType") or a subtype of
    `PyDateTime_DateTimeType`. *ob* must not be `NULL`. This function always
    succeeds.

int PyDateTime\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DateTimeType`](#c.PyDateTime_DateTimeType "PyDateTime_DateTimeType"). *ob* must not
    be `NULL`. This function always succeeds.

int PyTime\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_TimeType`](#c.PyDateTime_TimeType "PyDateTime_TimeType") or a subtype of
    `PyDateTime_TimeType`. *ob* must not be `NULL`. This function always
    succeeds.

int PyTime\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_TimeType`](#c.PyDateTime_TimeType "PyDateTime_TimeType"). *ob* must not be
    `NULL`. This function always succeeds.

int PyDelta\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DeltaType`](#c.PyDateTime_DeltaType "PyDateTime_DeltaType") or a subtype of
    `PyDateTime_DeltaType`. *ob* must not be `NULL`. This function always
    succeeds.

int PyDelta\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_DeltaType`](#c.PyDateTime_DeltaType "PyDateTime_DeltaType"). *ob* must not be
    `NULL`. This function always succeeds.

int PyTZInfo\_Check([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_TZInfoType`](#c.PyDateTime_TZInfoType "PyDateTime_TZInfoType") or a subtype of
    `PyDateTime_TZInfoType`. *ob* must not be `NULL`. This function always
    succeeds.

int PyTZInfo\_CheckExact([PyObject](structures.html#c.PyObject "PyObject") \*ob)
:   Return true if *ob* is of type [`PyDateTime_TZInfoType`](#c.PyDateTime_TZInfoType "PyDateTime_TZInfoType"). *ob* must not be
    `NULL`. This function always succeeds.

Macros to create objects:

[PyObject](structures.html#c.PyObject "PyObject") \*PyDate\_FromDate(int year, int month, int day)
:   *Return value: New reference.*

    Return a [`datetime.date`](../library/datetime.html#datetime.date "datetime.date") object with the specified year, month and day.

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_FromDateAndTime(int year, int month, int day, int hour, int minute, int second, int usecond)
:   *Return value: New reference.*

    Return a [`datetime.datetime`](../library/datetime.html#datetime.datetime "datetime.datetime") object with the specified year, month, day, hour,
    minute, second and microsecond.

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_FromDateAndTimeAndFold(int year, int month, int day, int hour, int minute, int second, int usecond, int fold)
:   *Return value: New reference.*

    Return a [`datetime.datetime`](../library/datetime.html#datetime.datetime "datetime.datetime") object with the specified year, month, day, hour,
    minute, second, microsecond and fold.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTime\_FromTime(int hour, int minute, int second, int usecond)
:   *Return value: New reference.*

    Return a [`datetime.time`](../library/datetime.html#datetime.time "datetime.time") object with the specified hour, minute, second and
    microsecond.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTime\_FromTimeAndFold(int hour, int minute, int second, int usecond, int fold)
:   *Return value: New reference.*

    Return a [`datetime.time`](../library/datetime.html#datetime.time "datetime.time") object with the specified hour, minute, second,
    microsecond and fold.

[PyObject](structures.html#c.PyObject "PyObject") \*PyDelta\_FromDSU(int days, int seconds, int useconds)
:   *Return value: New reference.*

    Return a [`datetime.timedelta`](../library/datetime.html#datetime.timedelta "datetime.timedelta") object representing the given number
    of days, seconds and microseconds. Normalization is performed so that the
    resulting number of microseconds and seconds lie in the ranges documented for
    [`datetime.timedelta`](../library/datetime.html#datetime.timedelta "datetime.timedelta") objects.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTimeZone\_FromOffset([PyObject](structures.html#c.PyObject "PyObject") \*offset)
:   *Return value: New reference.*

    Return a [`datetime.timezone`](../library/datetime.html#datetime.timezone "datetime.timezone") object with an unnamed fixed offset
    represented by the *offset* argument.

[PyObject](structures.html#c.PyObject "PyObject") \*PyTimeZone\_FromOffsetAndName([PyObject](structures.html#c.PyObject "PyObject") \*offset, [PyObject](structures.html#c.PyObject "PyObject") \*name)
:   *Return value: New reference.*

    Return a [`datetime.timezone`](../library/datetime.html#datetime.timezone "datetime.timezone") object with a fixed offset represented
    by the *offset* argument and with tzname *name*.

Macros to extract fields from date objects. The argument must be an instance of
[`PyDateTime_Date`](#c.PyDateTime_Date "PyDateTime_Date"), including subclasses (such as
[`PyDateTime_DateTime`](#c.PyDateTime_DateTime "PyDateTime_DateTime")). The argument must not be `NULL`, and the type is
not checked:

int PyDateTime\_GET\_YEAR([PyDateTime\_Date](#c.PyDateTime_Date "PyDateTime_Date") \*o)
:   Return the year, as a positive int.

int PyDateTime\_GET\_MONTH([PyDateTime\_Date](#c.PyDateTime_Date "PyDateTime_Date") \*o)
:   Return the month, as an int from 1 through 12.

int PyDateTime\_GET\_DAY([PyDateTime\_Date](#c.PyDateTime_Date "PyDateTime_Date") \*o)
:   Return the day, as an int from 1 through 31.

Macros to extract fields from datetime objects. The argument must be an
instance of [`PyDateTime_DateTime`](#c.PyDateTime_DateTime "PyDateTime_DateTime"), including subclasses. The argument
must not be `NULL`, and the type is not checked:

int PyDateTime\_DATE\_GET\_HOUR([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the hour, as an int from 0 through 23.

int PyDateTime\_DATE\_GET\_MINUTE([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the minute, as an int from 0 through 59.

int PyDateTime\_DATE\_GET\_SECOND([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the second, as an int from 0 through 59.

int PyDateTime\_DATE\_GET\_MICROSECOND([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the microsecond, as an int from 0 through 999999.

int PyDateTime\_DATE\_GET\_FOLD([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the fold, as an int from 0 through 1.

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_DATE\_GET\_TZINFO([PyDateTime\_DateTime](#c.PyDateTime_DateTime "PyDateTime_DateTime") \*o)
:   Return the tzinfo (which may be `None`).

Macros to extract fields from time objects. The argument must be an instance of
[`PyDateTime_Time`](#c.PyDateTime_Time "PyDateTime_Time"), including subclasses. The argument must not be `NULL`,
and the type is not checked:

int PyDateTime\_TIME\_GET\_HOUR([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the hour, as an int from 0 through 23.

int PyDateTime\_TIME\_GET\_MINUTE([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the minute, as an int from 0 through 59.

int PyDateTime\_TIME\_GET\_SECOND([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the second, as an int from 0 through 59.

int PyDateTime\_TIME\_GET\_MICROSECOND([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the microsecond, as an int from 0 through 999999.

int PyDateTime\_TIME\_GET\_FOLD([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the fold, as an int from 0 through 1.

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_TIME\_GET\_TZINFO([PyDateTime\_Time](#c.PyDateTime_Time "PyDateTime_Time") \*o)
:   Return the tzinfo (which may be `None`).

Macros to extract fields from time delta objects. The argument must be an
instance of [`PyDateTime_Delta`](#c.PyDateTime_Delta "PyDateTime_Delta"), including subclasses. The argument must
not be `NULL`, and the type is not checked:

int PyDateTime\_DELTA\_GET\_DAYS([PyDateTime\_Delta](#c.PyDateTime_Delta "PyDateTime_Delta") \*o)
:   Return the number of days, as an int from -999999999 to 999999999.

int PyDateTime\_DELTA\_GET\_SECONDS([PyDateTime\_Delta](#c.PyDateTime_Delta "PyDateTime_Delta") \*o)
:   Return the number of seconds, as an int from 0 through 86399.

int PyDateTime\_DELTA\_GET\_MICROSECONDS([PyDateTime\_Delta](#c.PyDateTime_Delta "PyDateTime_Delta") \*o)
:   Return the number of microseconds, as an int from 0 through 999999.

Macros for the convenience of modules implementing the DB API:

[PyObject](structures.html#c.PyObject "PyObject") \*PyDateTime\_FromTimestamp([PyObject](structures.html#c.PyObject "PyObject") \*args)
:   *Return value: New reference.*

    Create and return a new [`datetime.datetime`](../library/datetime.html#datetime.datetime "datetime.datetime") object given an argument
    tuple suitable for passing to [`datetime.datetime.fromtimestamp()`](../library/datetime.html#datetime.datetime.fromtimestamp "datetime.datetime.fromtimestamp").

[PyObject](structures.html#c.PyObject "PyObject") \*PyDate\_FromTimestamp([PyObject](structures.html#c.PyObject "PyObject") \*args)
:   *Return value: New reference.*

    Create and return a new [`datetime.date`](../library/datetime.html#datetime.date "datetime.date") object given an argument
    tuple suitable for passing to [`datetime.date.fromtimestamp()`](../library/datetime.html#datetime.date.fromtimestamp "datetime.date.fromtimestamp").