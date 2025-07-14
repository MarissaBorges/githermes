SQLite is a C library that provides a lightweight disk-based database that
doesn’t require a separate server process and allows accessing the database
using a nonstandard variant of the SQL query language. Some applications can use
SQLite for internal data storage. It’s also possible to prototype an
application using SQLite and then port the code to a larger database such as
PostgreSQL or Oracle.

Tutorial
--------

In this tutorial, you will create a database of Monty Python movies
using basic `sqlite3` functionality.
It assumes a fundamental understanding of database concepts,
including [cursors](https://en.wikipedia.org/wiki/Cursor_(databases)) and [transactions](https://en.wikipedia.org/wiki/Database_transaction).

First, we need to create a new database and open
a database connection to allow `sqlite3` to work with it.
Call [`sqlite3.connect()`](#sqlite3.connect "sqlite3.connect") to create a connection to
the database `tutorial.db` in the current working directory,
implicitly creating it if it does not exist:

Copy

```
import sqlite3
con = sqlite3.connect("tutorial.db")

```

The returned [`Connection`](#sqlite3.Connection "sqlite3.Connection") object `con`
represents the connection to the on-disk database.

In order to execute SQL statements and fetch results from SQL queries,
we will need to use a database cursor.
Call [`con.cursor()`](#sqlite3.Connection.cursor "sqlite3.Connection.cursor") to create the [`Cursor`](#sqlite3.Cursor "sqlite3.Cursor"):

Now that we’ve got a database connection and a cursor,
we can create a database table `movie` with columns for title,
release year, and review score.
For simplicity, we can just use column names in the table declaration –
thanks to the [flexible typing](https://www.sqlite.org/flextypegood.html) feature of SQLite,
specifying the data types is optional.
Execute the `CREATE TABLE` statement
by calling [`cur.execute(...)`](#sqlite3.Cursor.execute "sqlite3.Cursor.execute"):

Copy

```
cur.execute("CREATE TABLE movie(title, year, score)")

```

We can verify that the new table has been created by querying
the `sqlite_master` table built-in to SQLite,
which should now contain an entry for the `movie` table definition
(see [The Schema Table](https://www.sqlite.org/schematab.html) for details).
Execute that query by calling [`cur.execute(...)`](#sqlite3.Cursor.execute "sqlite3.Cursor.execute"),
assign the result to `res`,
and call [`res.fetchone()`](#sqlite3.Cursor.fetchone "sqlite3.Cursor.fetchone") to fetch the resulting row:

Copy

```
>>> res = cur.execute("SELECT name FROM sqlite_master")
>>> res.fetchone()
('movie',)

```

We can see that the table has been created,
as the query returns a [`tuple`](stdtypes.html#tuple "tuple") containing the table’s name.
If we query `sqlite_master` for a non-existent table `spam`,
`res.fetchone()` will return `None`:

Copy

```
>>> res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")
>>> res.fetchone() is None
True

```

Now, add two rows of data supplied as SQL literals
by executing an `INSERT` statement,
once again by calling [`cur.execute(...)`](#sqlite3.Cursor.execute "sqlite3.Cursor.execute"):

Copy

```
cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")

```

The `INSERT` statement implicitly opens a transaction,
which needs to be committed before changes are saved in the database
(see [Transaction control](#sqlite3-controlling-transactions) for details).
Call [`con.commit()`](#sqlite3.Connection.commit "sqlite3.Connection.commit") on the connection object
to commit the transaction:

We can verify that the data was inserted correctly
by executing a `SELECT` query.
Use the now-familiar [`cur.execute(...)`](#sqlite3.Cursor.execute "sqlite3.Cursor.execute") to
assign the result to `res`,
and call [`res.fetchall()`](#sqlite3.Cursor.fetchall "sqlite3.Cursor.fetchall") to return all resulting rows:

Copy

```
>>> res = cur.execute("SELECT score FROM movie")
>>> res.fetchall()
[(8.2,), (7.5,)]

```

The result is a [`list`](stdtypes.html#list "list") of two `tuple`s, one per row,
each containing that row’s `score` value.

Now, insert three more rows by calling
[`cur.executemany(...)`](#sqlite3.Cursor.executemany "sqlite3.Cursor.executemany"):

Copy

```
data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
con.commit()  # Remember to commit the transaction after executing INSERT.

```

Notice that `?` placeholders are used to bind `data` to the query.
Always use placeholders instead of [string formatting](../tutorial/inputoutput.html#tut-formatting)
to bind Python values to SQL statements,
to avoid [SQL injection attacks](https://en.wikipedia.org/wiki/SQL_injection)
(see [How to use placeholders to bind values in SQL queries](#sqlite3-placeholders) for more details).

We can verify that the new rows were inserted
by executing a `SELECT` query,
this time iterating over the results of the query:

Copy

```
>>> for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
...     print(row)
(1971, 'And Now for Something Completely Different')
(1975, 'Monty Python and the Holy Grail')
(1979, "Monty Python's Life of Brian")
(1982, 'Monty Python Live at the Hollywood Bowl')
(1983, "Monty Python's The Meaning of Life")

```

Each row is a two-item [`tuple`](stdtypes.html#tuple "tuple") of `(year, title)`,
matching the columns selected in the query.

Finally, verify that the database has been written to disk
by calling [`con.close()`](#sqlite3.Connection.close "sqlite3.Connection.close")
to close the existing connection, opening a new one,
creating a new cursor, then querying the database:

Copy

```
>>> con.close()
>>> new_con = sqlite3.connect("tutorial.db")
>>> new_cur = new_con.cursor()
>>> res = new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC")
>>> title, year = res.fetchone()
>>> print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
The highest scoring Monty Python movie is 'Monty Python and the Holy Grail', released in 1975
>>> new_con.close()

```

You’ve now created an SQLite database using the `sqlite3` module,
inserted data and retrieved values from it in multiple ways.

How-to guides
-------------

### How to use placeholders to bind values in SQL queries

SQL operations usually need to use values from Python variables. However,
beware of using Python’s string operations to assemble queries, as they
are vulnerable to [SQL injection attacks](https://en.wikipedia.org/wiki/SQL_injection). For example, an attacker can simply
close the single quote and inject `OR TRUE` to select all rows:

Copy

```
>>> # Never do this -- insecure!
>>> symbol = input()
' OR TRUE; --
>>> sql = "SELECT * FROM stocks WHERE symbol = '%s'" % symbol
>>> print(sql)
SELECT * FROM stocks WHERE symbol = '' OR TRUE; --'
>>> cur.execute(sql)

```

Instead, use the DB-API’s parameter substitution. To insert a variable into a
query string, use a placeholder in the string, and substitute the actual values
into the query by providing them as a [`tuple`](stdtypes.html#tuple "tuple") of values to the second
argument of the cursor’s [`execute()`](#sqlite3.Cursor.execute "sqlite3.Cursor.execute") method.

An SQL statement may use one of two kinds of placeholders:
question marks (qmark style) or named placeholders (named style).
For the qmark style, *parameters* must be a
[sequence](../glossary.html#term-sequence) whose length must match the number of placeholders,
or a [`ProgrammingError`](#sqlite3.ProgrammingError "sqlite3.ProgrammingError") is raised.
For the named style, *parameters* must be
an instance of a [`dict`](stdtypes.html#dict "dict") (or a subclass),
which must contain keys for all named parameters;
any extra items are ignored.
Here’s an example of both styles:

Copy

```
con = sqlite3.connect(":memory:")
cur = con.execute("CREATE TABLE lang(name, first_appeared)")

# This is the named style used with executemany():
data = (
    {"name": "C", "year": 1972},
    {"name": "Fortran", "year": 1957},
    {"name": "Python", "year": 1991},
    {"name": "Go", "year": 2009},
)
cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

# This is the qmark style used in a SELECT query:
params = (1972,)
cur.execute("SELECT * FROM lang WHERE first_appeared = ?", params)
print(cur.fetchall())
con.close()

```

Note

[**PEP 249**](https://peps.python.org/pep-0249/) numeric placeholders are *not* supported.
If used, they will be interpreted as named placeholders.

### How to adapt custom Python types to SQLite values

SQLite supports only a limited set of data types natively.
To store custom Python types in SQLite databases, *adapt* them to one of the
[Python types SQLite natively understands](#sqlite3-types).

There are two ways to adapt Python objects to SQLite types:
letting your object adapt itself, or using an *adapter callable*.
The latter will take precedence above the former.
For a library that exports a custom type,
it may make sense to enable that type to adapt itself.
As an application developer, it may make more sense to take direct control by
registering custom adapter functions.

#### How to write adaptable objects

Suppose we have a `Point` class that represents a pair of coordinates,
`x` and `y`, in a Cartesian coordinate system.
The coordinate pair will be stored as a text string in the database,
using a semicolon to separate the coordinates.
This can be implemented by adding a `__conform__(self, protocol)`
method which returns the adapted value.
The object passed to *protocol* will be of type [`PrepareProtocol`](#sqlite3.PrepareProtocol "sqlite3.PrepareProtocol").

Copy

```
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.x};{self.y}"

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("SELECT ?", (Point(4.0, -3.2),))
print(cur.fetchone()[0])
con.close()

```

#### How to register adapter callables

The other possibility is to create a function that converts the Python object
to an SQLite-compatible type.
This function can then be registered using [`register_adapter()`](#sqlite3.register_adapter "sqlite3.register_adapter").

Copy

```
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

def adapt_point(point):
    return f"{point.x};{point.y}"

sqlite3.register_adapter(Point, adapt_point)

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("SELECT ?", (Point(1.0, 2.5),))
print(cur.fetchone()[0])
con.close()

```

### How to convert SQLite values to custom Python types

Writing an adapter lets you convert *from* custom Python types *to* SQLite
values.
To be able to convert *from* SQLite values *to* custom Python types,
we use *converters*.

Let’s go back to the `Point` class. We stored the x and y coordinates
separated via semicolons as strings in SQLite.

First, we’ll define a converter function that accepts the string as a parameter
and constructs a `Point` object from it.

Note

Converter functions are **always** passed a [`bytes`](stdtypes.html#bytes "bytes") object,
no matter the underlying SQLite data type.

Copy

```
def convert_point(s):
    x, y = map(float, s.split(b";"))
    return Point(x, y)

```

We now need to tell `sqlite3` when it should convert a given SQLite value.
This is done when connecting to a database, using the *detect\_types* parameter
of [`connect()`](#sqlite3.connect "sqlite3.connect"). There are three options:

* Implicit: set *detect\_types* to [`PARSE_DECLTYPES`](#sqlite3.PARSE_DECLTYPES "sqlite3.PARSE_DECLTYPES")
* Explicit: set *detect\_types* to [`PARSE_COLNAMES`](#sqlite3.PARSE_COLNAMES "sqlite3.PARSE_COLNAMES")
* Both: set *detect\_types* to
  `sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES`.
  Column names take precedence over declared types.

The following example illustrates the implicit and explicit approaches:

Copy

```
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

def adapt_point(point):
    return f"{point.x};{point.y}"

def convert_point(s):
    x, y = list(map(float, s.split(b";")))
    return Point(x, y)

# Register the adapter and converter
sqlite3.register_adapter(Point, adapt_point)
sqlite3.register_converter("point", convert_point)

# 1) Parse using declared types
p = Point(4.0, -3.2)
con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.execute("CREATE TABLE test(p point)")

cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
cur.execute("SELECT p FROM test")
print("with declared types:", cur.fetchone()[0])
cur.close()
con.close()

# 2) Parse using column names
con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_COLNAMES)
cur = con.execute("CREATE TABLE test(p)")

cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
cur.execute('SELECT p AS "p [point]" FROM test')
print("with column names:", cur.fetchone()[0])
cur.close()
con.close()

```

### Adapter and converter recipes

This section shows recipes for common adapters and converters.

Copy

```
import datetime
import sqlite3

def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.replace(tzinfo=None).isoformat()

def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromtimestamp(int(val))

sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("datetime", convert_datetime)
sqlite3.register_converter("timestamp", convert_timestamp)

```

### How to use connection shortcut methods

Using the [`execute()`](#sqlite3.Connection.execute "sqlite3.Connection.execute"),
[`executemany()`](#sqlite3.Connection.executemany "sqlite3.Connection.executemany"), and [`executescript()`](#sqlite3.Connection.executescript "sqlite3.Connection.executescript")
methods of the [`Connection`](#sqlite3.Connection "sqlite3.Connection") class, your code can
be written more concisely because you don’t have to create the (often
superfluous) [`Cursor`](#sqlite3.Cursor "sqlite3.Cursor") objects explicitly. Instead, the [`Cursor`](#sqlite3.Cursor "sqlite3.Cursor")
objects are created implicitly and these shortcut methods return the cursor
objects. This way, you can execute a `SELECT` statement and iterate over it
directly using only a single call on the [`Connection`](#sqlite3.Connection "sqlite3.Connection") object.

Copy

```
# Create and fill the table.
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE lang(name, first_appeared)")
data = [
    ("C++", 1985),
    ("Objective-C", 1984),
]
con.executemany("INSERT INTO lang(name, first_appeared) VALUES(?, ?)", data)

# Print the table contents
for row in con.execute("SELECT name, first_appeared FROM lang"):
    print(row)

print("I just deleted", con.execute("DELETE FROM lang").rowcount, "rows")

# close() is not a shortcut method and it's not called automatically;
# the connection object should be closed manually
con.close()

```

### How to use the connection context manager

A [`Connection`](#sqlite3.Connection "sqlite3.Connection") object can be used as a context manager that
automatically commits or rolls back open transactions when leaving the body of
the context manager.
If the body of the [`with`](../reference/compound_stmts.html#with) statement finishes without exceptions,
the transaction is committed.
If this commit fails,
or if the body of the `with` statement raises an uncaught exception,
the transaction is rolled back.
If [`autocommit`](#sqlite3.Connection.autocommit "sqlite3.Connection.autocommit") is `False`,
a new transaction is implicitly opened after committing or rolling back.

If there is no open transaction upon leaving the body of the `with` statement,
or if [`autocommit`](#sqlite3.Connection.autocommit "sqlite3.Connection.autocommit") is `True`,
the context manager does nothing.

Note

The context manager neither implicitly opens a new transaction
nor closes the connection. If you need a closing context manager, consider
using [`contextlib.closing()`](contextlib.html#contextlib.closing "contextlib.closing").

Copy

```
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE lang(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE)")

# Successful, con.commit() is called automatically afterwards
with con:
    con.execute("INSERT INTO lang(name) VALUES(?)", ("Python",))

# con.rollback() is called after the with block finishes with an exception,
# the exception is still raised and must be caught
try:
    with con:
        con.execute("INSERT INTO lang(name) VALUES(?)", ("Python",))
except sqlite3.IntegrityError:
    print("couldn't add Python twice")

# Connection object used as context manager only commits or rollbacks transactions,
# so the connection object should be closed manually
con.close()

```

### How to work with SQLite URIs

Some useful URI tricks include:

Copy

```
>>> con = sqlite3.connect("file:tutorial.db?mode=ro", uri=True)
>>> con.execute("CREATE TABLE readonly(data)")
Traceback (most recent call last):
OperationalError: attempt to write a readonly database
>>> con.close()

```

Copy

```
>>> con = sqlite3.connect("file:nosuchdb.db?mode=rw", uri=True)
Traceback (most recent call last):
OperationalError: unable to open database file

```

Copy

```
db = "file:mem1?mode=memory&cache=shared"
con1 = sqlite3.connect(db, uri=True)
con2 = sqlite3.connect(db, uri=True)
with con1:
    con1.execute("CREATE TABLE shared(data)")
    con1.execute("INSERT INTO shared VALUES(28)")
res = con2.execute("SELECT data FROM shared")
assert res.fetchone() == (28,)

con1.close()
con2.close()

```

More information about this feature, including a list of parameters,
can be found in the [SQLite URI documentation](https://www.sqlite.org/uri.html).

### How to create and use row factories

By default, `sqlite3` represents each row as a [`tuple`](stdtypes.html#tuple "tuple").
If a `tuple` does not suit your needs,
you can use the [`sqlite3.Row`](#sqlite3.Row "sqlite3.Row") class
or a custom [`row_factory`](#sqlite3.Cursor.row_factory "sqlite3.Cursor.row_factory").

While `row_factory` exists as an attribute both on the
[`Cursor`](#sqlite3.Cursor "sqlite3.Cursor") and the [`Connection`](#sqlite3.Connection "sqlite3.Connection"),
it is recommended to set [`Connection.row_factory`](#sqlite3.Connection.row_factory "sqlite3.Connection.row_factory"),
so all cursors created from the connection will use the same row factory.

`Row` provides indexed and case-insensitive named access to columns,
with minimal memory overhead and performance impact over a `tuple`.
To use `Row` as a row factory,
assign it to the `row_factory` attribute:

Copy

```
>>> con = sqlite3.connect(":memory:")
>>> con.row_factory = sqlite3.Row

```

Queries now return `Row` objects:

Copy

```
>>> res = con.execute("SELECT 'Earth' AS name, 6378 AS radius")
>>> row = res.fetchone()
>>> row.keys()
['name', 'radius']
>>> row[0]         # Access by index.
'Earth'
>>> row["name"]    # Access by name.
'Earth'
>>> row["RADIUS"]  # Column names are case-insensitive.
6378
>>> con.close()

```

Note

The `FROM` clause can be omitted in the `SELECT` statement, as in the
above example. In such cases, SQLite returns a single row with columns
defined by expressions, e.g. literals, with the given aliases
`expr AS alias`.

You can create a custom [`row_factory`](#sqlite3.Cursor.row_factory "sqlite3.Cursor.row_factory")
that returns each row as a [`dict`](stdtypes.html#dict "dict"), with column names mapped to values:

Copy

```
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

```

Using it, queries now return a `dict` instead of a `tuple`:

Copy

```
>>> con = sqlite3.connect(":memory:")
>>> con.row_factory = dict_factory
>>> for row in con.execute("SELECT 1 AS a, 2 AS b"):
...     print(row)
{'a': 1, 'b': 2}
>>> con.close()

```

The following row factory returns a [named tuple](../glossary.html#term-named-tuple):

Copy

```
from collections import namedtuple

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

```

`namedtuple_factory()` can be used as follows:

Copy

```
>>> con = sqlite3.connect(":memory:")
>>> con.row_factory = namedtuple_factory
>>> cur = con.execute("SELECT 1 AS a, 2 AS b")
>>> row = cur.fetchone()
>>> row
Row(a=1, b=2)
>>> row[0]  # Indexed access.
1
>>> row.b   # Attribute access.
2
>>> con.close()

```

With some adjustments, the above recipe can be adapted to use a
[`dataclass`](dataclasses.html#dataclasses.dataclass "dataclasses.dataclass"), or any other custom class,
instead of a [`namedtuple`](collections.html#collections.namedtuple "collections.namedtuple").

### How to handle non-UTF-8 text encodings

By default, `sqlite3` uses [`str`](stdtypes.html#str "str") to adapt SQLite values
with the `TEXT` data type.
This works well for UTF-8 encoded text, but it might fail for other encodings
and invalid UTF-8.
You can use a custom [`text_factory`](#sqlite3.Connection.text_factory "sqlite3.Connection.text_factory") to handle such cases.

Because of SQLite’s [flexible typing](https://www.sqlite.org/flextypegood.html), it is not uncommon to encounter table
columns with the `TEXT` data type containing non-UTF-8 encodings,
or even arbitrary data.
To demonstrate, let’s assume we have a database with ISO-8859-2 (Latin-2)
encoded text, for example a table of Czech-English dictionary entries.
Assuming we now have a [`Connection`](#sqlite3.Connection "sqlite3.Connection") instance `con`
connected to this database,
we can decode the Latin-2 encoded text using this [`text_factory`](#sqlite3.Connection.text_factory "sqlite3.Connection.text_factory"):

Copy

```
con.text_factory = lambda data: str(data, encoding="latin2")

```

For invalid UTF-8 or arbitrary data in stored in `TEXT` table columns,
you can use the following technique, borrowed from the [Unicode HOWTO](../howto/unicode.html#unicode-howto):

Copy

```
con.text_factory = lambda data: str(data, errors="surrogateescape")

```

Note

The `sqlite3` module API does not support strings
containing surrogates.