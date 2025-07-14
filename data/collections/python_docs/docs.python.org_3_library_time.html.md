|  |  |  |
| --- | --- | --- |
| `%a` | Locale’s abbreviated weekday name. |  |
| `%A` | Locale’s full weekday name. |  |
| `%b` | Locale’s abbreviated month name. |  |
| `%B` | Locale’s full month name. |  |
| `%c` | Locale’s appropriate date and time representation. |  |
| `%d` | Day of the month as a decimal number [01,31]. |  |
| `%f` | Microseconds as a decimal number  [000000,999999]. | (1) |
| `%H` | Hour (24-hour clock) as a decimal number [00,23]. |  |
| `%I` | Hour (12-hour clock) as a decimal number [01,12]. |  |
| `%j` | Day of the year as a decimal number [001,366]. |  |
| `%m` | Month as a decimal number [01,12]. |  |
| `%M` | Minute as a decimal number [00,59]. |  |
| `%p` | Locale’s equivalent of either AM or PM. | (2) |
| `%S` | Second as a decimal number [00,61]. | (3) |
| `%U` | Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. | (4) |
| `%u` | Day of the week (Monday is 1; Sunday is 7) as a decimal number [1, 7]. |  |
| `%w` | Weekday as a decimal number [0(Sunday),6]. |  |
| `%W` | Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. | (4) |
| `%x` | Locale’s appropriate date representation. |  |
| `%X` | Locale’s appropriate time representation. |  |
| `%y` | Year without century as a decimal number [00,99]. |  |
| `%Y` | Year with century as a decimal number. |  |
| `%z` | Time zone offset indicating a positive or negative time difference from UTC/GMT of the form +HHMM or -HHMM, where H represents decimal hour digits and M represents decimal minute digits [-23:59, +23:59]. |  |
| `%Z` | Time zone name (no characters if no time zone exists). Deprecated. |  |
| `%G` | ISO 8601 year (similar to `%Y` but follows the rules for the ISO 8601 calendar year). The year starts with the week that contains the first Thursday of the calendar year. |  |
| `%V` | ISO 8601 week number (as a decimal number [01,53]). The first week of the year is the one that contains the first Thursday of the year. Weeks start on Monday. |  |
| `%%` | A literal `'%'` character. |  |