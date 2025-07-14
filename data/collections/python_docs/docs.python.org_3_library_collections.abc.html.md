|  |  |  |  |
| --- | --- | --- | --- |
| [`Container`](#collections.abc.Container "collections.abc.Container") |  | `__contains__` |  |
| [`Hashable`](#collections.abc.Hashable "collections.abc.Hashable") |  | `__hash__` |  |
| [`Iterable`](#collections.abc.Iterable "collections.abc.Iterable") |  | `__iter__` |  |
| [`Iterator`](#collections.abc.Iterator "collections.abc.Iterator") | [`Iterable`](#collections.abc.Iterable "collections.abc.Iterable") | `__next__` | `__iter__` |
| [`Reversible`](#collections.abc.Reversible "collections.abc.Reversible") | [`Iterable`](#collections.abc.Iterable "collections.abc.Iterable") | `__reversed__` |  |
| [`Generator`](#collections.abc.Generator "collections.abc.Generator") | [`Iterator`](#collections.abc.Iterator "collections.abc.Iterator") | `send`, `throw` | `close`, `__iter__`, `__next__` |
| [`Sized`](#collections.abc.Sized "collections.abc.Sized") |  | `__len__` |  |
| [`Callable`](#collections.abc.Callable "collections.abc.Callable") |  | `__call__` |  |
| [`Collection`](#collections.abc.Collection "collections.abc.Collection") | [`Sized`](#collections.abc.Sized "collections.abc.Sized"), [`Iterable`](#collections.abc.Iterable "collections.abc.Iterable"), [`Container`](#collections.abc.Container "collections.abc.Container") | `__contains__`, `__iter__`, `__len__` |  |
| [`Sequence`](#collections.abc.Sequence "collections.abc.Sequence") | [`Reversible`](#collections.abc.Reversible "collections.abc.Reversible"), [`Collection`](#collections.abc.Collection "collections.abc.Collection") | `__getitem__`, `__len__` | `__contains__`, `__iter__`, `__reversed__`, `index`, and `count` |
| [`MutableSequence`](#collections.abc.MutableSequence "collections.abc.MutableSequence") | [`Sequence`](#collections.abc.Sequence "collections.abc.Sequence") | `__getitem__`, `__setitem__`, `__delitem__`, `__len__`, `insert` | Inherited [`Sequence`](#collections.abc.Sequence "collections.abc.Sequence") methods and `append`, `clear`, `reverse`, `extend`, `pop`, `remove`, and `__iadd__` |
| [`ByteString`](#collections.abc.ByteString "collections.abc.ByteString") | [`Sequence`](#collections.abc.Sequence "collections.abc.Sequence") | `__getitem__`, `__len__` | Inherited [`Sequence`](#collections.abc.Sequence "collections.abc.Sequence") methods |
| [`Set`](#collections.abc.Set "collections.abc.Set") | [`Collection`](#collections.abc.Collection "collections.abc.Collection") | `__contains__`, `__iter__`, `__len__` | `__le__`, `__lt__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`, `__and__`, `__or__`, `__sub__`, `__rsub__`, `__xor__`, `__rxor__` and `isdisjoint` |
| [`MutableSet`](#collections.abc.MutableSet "collections.abc.MutableSet") | [`Set`](#collections.abc.Set "collections.abc.Set") | `__contains__`, `__iter__`, `__len__`, `add`, `discard` | Inherited [`Set`](#collections.abc.Set "collections.abc.Set") methods and `clear`, `pop`, `remove`, `__ior__`, `__iand__`, `__ixor__`, and `__isub__` |
| [`Mapping`](#collections.abc.Mapping "collections.abc.Mapping") | [`Collection`](#collections.abc.Collection "collections.abc.Collection") | `__getitem__`, `__iter__`, `__len__` | `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, and `__ne__` |
| [`MutableMapping`](#collections.abc.MutableMapping "collections.abc.MutableMapping") | [`Mapping`](#collections.abc.Mapping "collections.abc.Mapping") | `__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__len__` | Inherited [`Mapping`](#collections.abc.Mapping "collections.abc.Mapping") methods and `pop`, `popitem`, `clear`, `update`, and `setdefault` |
| [`MappingView`](#collections.abc.MappingView "collections.abc.MappingView") | [`Sized`](#collections.abc.Sized "collections.abc.Sized") |  | `__init__`, `__len__` and `__repr__` |
| [`ItemsView`](#collections.abc.ItemsView "collections.abc.ItemsView") | [`MappingView`](#collections.abc.MappingView "collections.abc.MappingView"), [`Set`](#collections.abc.Set "collections.abc.Set") |  | `__contains__`, `__iter__` |
| [`KeysView`](#collections.abc.KeysView "collections.abc.KeysView") | [`MappingView`](#collections.abc.MappingView "collections.abc.MappingView"), [`Set`](#collections.abc.Set "collections.abc.Set") |  | `__contains__`, `__iter__` |
| [`ValuesView`](#collections.abc.ValuesView "collections.abc.ValuesView") | [`MappingView`](#collections.abc.MappingView "collections.abc.MappingView"), [`Collection`](#collections.abc.Collection "collections.abc.Collection") |  | `__contains__`, `__iter__` |
| [`Awaitable`](#collections.abc.Awaitable "collections.abc.Awaitable") |  | `__await__` |  |
| [`Coroutine`](#collections.abc.Coroutine "collections.abc.Coroutine") | [`Awaitable`](#collections.abc.Awaitable "collections.abc.Awaitable") | `send`, `throw` | `close` |
| [`AsyncIterable`](#collections.abc.AsyncIterable "collections.abc.AsyncIterable") |  | `__aiter__` |  |
| [`AsyncIterator`](#collections.abc.AsyncIterator "collections.abc.AsyncIterator") | [`AsyncIterable`](#collections.abc.AsyncIterable "collections.abc.AsyncIterable") | `__anext__` | `__aiter__` |
| [`AsyncGenerator`](#collections.abc.AsyncGenerator "collections.abc.AsyncGenerator") | [`AsyncIterator`](#collections.abc.AsyncIterator "collections.abc.AsyncIterator") | `asend`, `athrow` | `aclose`, `__aiter__`, `__anext__` |
| [`Buffer`](#collections.abc.Buffer "collections.abc.Buffer") |  | `__buffer__` |  |