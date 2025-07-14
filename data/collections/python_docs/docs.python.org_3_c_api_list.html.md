Note

This macro “steals” a reference to *item*, and, unlike
[`PyList_SetItem()`](#c.PyList_SetItem "PyList_SetItem"), does *not* discard a reference to any item that
is being replaced; any reference in *list* at position *i* will be
leaked.