Let’s try some simple Python commands. Start the interpreter and wait for the
primary prompt, `>>>`. (It shouldn’t take long.)

### 3.1.1. Numbers

The interpreter acts as a simple calculator: you can type an expression at it
and it will write the value. Expression syntax is straightforward: the
operators `+`, `-`, `*` and `/` can be used to perform
arithmetic; parentheses (`()`) can be used for grouping.
For example:

Copy

```
>>> 2 + 2
4
>>> 50 - 5*6
20
>>> (50 - 5*6) / 4
5.0
>>> 8 / 5  # division always returns a floating-point number
1.6

```

The integer numbers (e.g. `2`, `4`, `20`) have type [`int`](../library/functions.html#int "int"),
the ones with a fractional part (e.g. `5.0`, `1.6`) have type
[`float`](../library/functions.html#float "float"). We will see more about numeric types later in the tutorial.

Division (`/`) always returns a float. To do [floor division](../glossary.html#term-floor-division) and
get an integer result you can use the `//` operator; to calculate
the remainder you can use `%`:

Copy

```
>>> 17 / 3  # classic division returns a float
5.666666666666667
>>>
>>> 17 // 3  # floor division discards the fractional part
5
>>> 17 % 3  # the % operator returns the remainder of the division
2
>>> 5 * 3 + 2  # floored quotient * divisor + remainder
17

```

With Python, it is possible to use the `**` operator to calculate powers :

Copy

```
>>> 5 ** 2  # 5 squared
25
>>> 2 ** 7  # 2 to the power of 7
128

```

The equal sign (`=`) is used to assign a value to a variable. Afterwards, no
result is displayed before the next interactive prompt:

Copy

```
>>> width = 20
>>> height = 5 * 9
>>> width * height
900

```

If a variable is not “defined” (assigned a value), trying to use it will
give you an error:

Copy

```
>>> n  # try to access an undefined variable
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'n' is not defined

```

There is full support for floating point; operators with mixed type operands
convert the integer operand to floating point:

Copy

```
>>> 4 * 3.75 - 1
14.0

```

In interactive mode, the last printed expression is assigned to the variable
`_`. This means that when you are using Python as a desk calculator, it is
somewhat easier to continue calculations, for example:

Copy

```
>>> tax = 12.5 / 100
>>> price = 100.50
>>> price * tax
12.5625
>>> price + _
113.0625
>>> round(_, 2)
113.06

```

This variable should be treated as read-only by the user. Don’t explicitly
assign a value to it — you would create an independent local variable with the
same name masking the built-in variable with its magic behavior.

In addition to [`int`](../library/functions.html#int "int") and [`float`](../library/functions.html#float "float"), Python supports other types of
numbers, such as [`Decimal`](../library/decimal.html#decimal.Decimal "decimal.Decimal") and [`Fraction`](../library/fractions.html#fractions.Fraction "fractions.Fraction").
Python also has built-in support for [complex numbers](../library/stdtypes.html#typesnumeric),
and uses the `j` or `J` suffix to indicate the imaginary part
(e.g. `3+5j`).

### 3.1.2. Text

Python can manipulate text (represented by type [`str`](../library/stdtypes.html#str "str"), so-called
“strings”) as well as numbers. This includes characters “`!`”, words
“`rabbit`”, names “`Paris`”, sentences “`Got your back.`”, etc.
“`Yay! :)`”. They can be enclosed in single quotes (`'...'`) or double
quotes (`"..."`) with the same result .

Copy

```
>>> 'spam eggs'  # single quotes
'spam eggs'
>>> "Paris rabbit got your back :)! Yay!"  # double quotes
'Paris rabbit got your back :)! Yay!'
>>> '1975'  # digits and numerals enclosed in quotes are also strings
'1975'

```

To quote a quote, we need to “escape” it, by preceding it with `\`.
Alternatively, we can use the other type of quotation marks:

Copy

```
>>> 'doesn\'t'  # use \' to escape the single quote...
"doesn't"
>>> "doesn't"  # ...or use double quotes instead
"doesn't"
>>> '"Yes," they said.'
'"Yes," they said.'
>>> "\"Yes,\" they said."
'"Yes," they said.'
>>> '"Isn\'t," they said.'
'"Isn\'t," they said.'

```

In the Python shell, the string definition and output string can look
different. The [`print()`](../library/functions.html#print "print") function produces a more readable output, by
omitting the enclosing quotes and by printing escaped and special characters:

Copy

```
>>> s = 'First line.\nSecond line.'  # \n means newline
>>> s  # without print(), special characters are included in the string
'First line.\nSecond line.'
>>> print(s)  # with print(), special characters are interpreted, so \n produces new line
First line.
Second line.

```

If you don’t want characters prefaced by `\` to be interpreted as
special characters, you can use *raw strings* by adding an `r` before
the first quote:

Copy

```
>>> print('C:\some\name')  # here \n means newline!
C:\some
ame
>>> print(r'C:\some\name')  # note the r before the quote
C:\some\name

```

There is one subtle aspect to raw strings: a raw string may not end in
an odd number of `\` characters; see
[the FAQ entry](../faq/programming.html#faq-programming-raw-string-backslash) for more information
and workarounds.

String literals can span multiple lines. One way is using triple-quotes:
`"""..."""` or `'''...'''`. End-of-line characters are automatically
included in the string, but it’s possible to prevent this by adding a `\` at
the end of the line. In the following example, the initial newline is not
included:

Copy

```
>>> print("""\
... Usage: thingy [OPTIONS]
...      -h                        Display this usage message
...      -H hostname               Hostname to connect to
... """)
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to

>>>

```

Strings can be concatenated (glued together) with the `+` operator, and
repeated with `*`:

Copy

```
>>> # 3 times 'un', followed by 'ium'
>>> 3 * 'un' + 'ium'
'unununium'

```

Two or more *string literals* (i.e. the ones enclosed between quotes) next
to each other are automatically concatenated.

Copy

```
>>> 'Py' 'thon'
'Python'

```

This feature is particularly useful when you want to break long strings:

Copy

```
>>> text = ('Put several strings within parentheses '
...         'to have them joined together.')
>>> text
'Put several strings within parentheses to have them joined together.'

```

This only works with two literals though, not with variables or expressions:

Copy

```
>>> prefix = 'Py'
>>> prefix 'thon'  # can't concatenate a variable and a string literal
  File "<stdin>", line 1
    prefix 'thon'
           ^^^^^^
SyntaxError: invalid syntax
>>> ('un' * 3) 'ium'
  File "<stdin>", line 1
    ('un' * 3) 'ium'
               ^^^^^
SyntaxError: invalid syntax

```

If you want to concatenate variables or a variable and a literal, use `+`:

Copy

```
>>> prefix + 'thon'
'Python'

```

Strings can be *indexed* (subscripted), with the first character having index 0.
There is no separate character type; a character is simply a string of size
one:

Copy

```
>>> word = 'Python'
>>> word[0]  # character in position 0
'P'
>>> word[5]  # character in position 5
'n'

```

Indices may also be negative numbers, to start counting from the right:

Copy

```
>>> word[-1]  # last character
'n'
>>> word[-2]  # second-last character
'o'
>>> word[-6]
'P'

```

Note that since -0 is the same as 0, negative indices start from -1.

In addition to indexing, *slicing* is also supported. While indexing is used
to obtain individual characters, *slicing* allows you to obtain a substring:

Copy

```
>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
'tho'

```

Slice indices have useful defaults; an omitted first index defaults to zero, an
omitted second index defaults to the size of the string being sliced.

Copy

```
>>> word[:2]   # character from the beginning to position 2 (excluded)
'Py'
>>> word[4:]   # characters from position 4 (included) to the end
'on'
>>> word[-2:]  # characters from the second-last (included) to the end
'on'

```

Note how the start is always included, and the end always excluded. This
makes sure that `s[:i] + s[i:]` is always equal to `s`:

Copy

```
>>> word[:2] + word[2:]
'Python'
>>> word[:4] + word[4:]
'Python'

```

One way to remember how slices work is to think of the indices as pointing
*between* characters, with the left edge of the first character numbered 0.
Then the right edge of the last character of a string of *n* characters has
index *n*, for example:

Copy

```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1

```

The first row of numbers gives the position of the indices 0…6 in the string;
the second row gives the corresponding negative indices. The slice from *i* to
*j* consists of all characters between the edges labeled *i* and *j*,
respectively.

For non-negative indices, the length of a slice is the difference of the
indices, if both are within bounds. For example, the length of `word[1:3]` is
2.

Attempting to use an index that is too large will result in an error:

Copy

```
>>> word[42]  # the word only has 6 characters
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range

```

However, out of range slice indexes are handled gracefully when used for
slicing:

Copy

```
>>> word[4:42]
'on'
>>> word[42:]
''

```

Python strings cannot be changed — they are [immutable](../glossary.html#term-immutable).
Therefore, assigning to an indexed position in the string results in an error:

Copy

```
>>> word[0] = 'J'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
>>> word[2:] = 'py'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment

```

If you need a different string, you should create a new one:

Copy

```
>>> 'J' + word[1:]
'Jython'
>>> word[:2] + 'py'
'Pypy'

```

The built-in function [`len()`](../library/functions.html#len "len") returns the length of a string:

Copy

```
>>> s = 'supercalifragilisticexpialidocious'
>>> len(s)
34

```

### 3.1.3. Lists

Python knows a number of *compound* data types, used to group together other
values. The most versatile is the *list*, which can be written as a list of
comma-separated values (items) between square brackets. Lists might contain
items of different types, but usually the items all have the same type.

Copy

```
>>> squares = [1, 4, 9, 16, 25]
>>> squares
[1, 4, 9, 16, 25]

```

Like strings (and all other built-in [sequence](../glossary.html#term-sequence) types), lists can be
indexed and sliced:

Copy

```
>>> squares[0]  # indexing returns the item
1
>>> squares[-1]
25
>>> squares[-3:]  # slicing returns a new list
[9, 16, 25]

```

Lists also support operations like concatenation:

Copy

```
>>> squares + [36, 49, 64, 81, 100]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

```

Unlike strings, which are [immutable](../glossary.html#term-immutable), lists are a [mutable](../glossary.html#term-mutable)
type, i.e. it is possible to change their content:

Copy

```
>>> cubes = [1, 8, 27, 65, 125]  # something's wrong here
>>> 4 ** 3  # the cube of 4 is 64, not 65!
64
>>> cubes[3] = 64  # replace the wrong value
>>> cubes
[1, 8, 27, 64, 125]

```

You can also add new items at the end of the list, by using
the `list.append()` *method* (we will see more about methods later):

Copy

```
>>> cubes.append(216)  # add the cube of 6
>>> cubes.append(7 ** 3)  # and the cube of 7
>>> cubes
[1, 8, 27, 64, 125, 216, 343]

```

Simple assignment in Python never copies data. When you assign a list
to a variable, the variable refers to the *existing list*.
Any changes you make to the list through one variable will be seen
through all other variables that refer to it.:

Copy

```
>>> rgb = ["Red", "Green", "Blue"]
>>> rgba = rgb
>>> id(rgb) == id(rgba)  # they reference the same object
True
>>> rgba.append("Alph")
>>> rgb
["Red", "Green", "Blue", "Alph"]

```

All slice operations return a new list containing the requested elements. This
means that the following slice returns a
[shallow copy](../library/copy.html#shallow-vs-deep-copy) of the list:

Copy

```
>>> correct_rgba = rgba[:]
>>> correct_rgba[-1] = "Alpha"
>>> correct_rgba
["Red", "Green", "Blue", "Alpha"]
>>> rgba
["Red", "Green", "Blue", "Alph"]

```

Assignment to slices is also possible, and this can even change the size of the
list or clear it entirely:

Copy

```
>>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> letters
['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> # replace some values
>>> letters[2:5] = ['C', 'D', 'E']
>>> letters
['a', 'b', 'C', 'D', 'E', 'f', 'g']
>>> # now remove them
>>> letters[2:5] = []
>>> letters
['a', 'b', 'f', 'g']
>>> # clear the list by replacing all the elements with an empty list
>>> letters[:] = []
>>> letters
[]

```

The built-in function [`len()`](../library/functions.html#len "len") also applies to lists:

Copy

```
>>> letters = ['a', 'b', 'c', 'd']
>>> len(letters)
4

```

It is possible to nest lists (create lists containing other lists), for
example:

Copy

```
>>> a = ['a', 'b', 'c']
>>> n = [1, 2, 3]
>>> x = [a, n]
>>> x
[['a', 'b', 'c'], [1, 2, 3]]
>>> x[0]
['a', 'b', 'c']
>>> x[0][1]
'b'

```