:   Decorator to wrap a function with a memoizing callable that saves up to the
    *maxsize* most recent calls. It can save time when an expensive or I/O bound
    function is periodically called with the same arguments.

    The cache is threadsafe so that the wrapped function can be used in
    multiple threads. This means that the underlying data structure will
    remain coherent during concurrent updates.

    It is possible for the wrapped function to be called more than once if
    another thread makes an additional call before the initial call has been
    completed and cached.

    Since a dictionary is used to cache results, the positional and keyword
    arguments to the function must be [hashable](../glossary.html#term-hashable).

    Distinct argument patterns may be considered to be distinct calls with
    separate cache entries. For example, `f(a=1, b=2)` and `f(b=2, a=1)`
    differ in their keyword argument order and may have two separate cache
    entries.

    If *user\_function* is specified, it must be a callable. This allows the
    *lru\_cache* decorator to be applied directly to a user function, leaving
    the *maxsize* at its default value of 128:

    Copy

    ```
    @lru_cache
    def count_vowels(sentence):
        return sum(sentence.count(vowel) for vowel in 'AEIOUaeiou')

    ```

    If *maxsize* is set to `None`, the LRU feature is disabled and the cache can
    grow without bound.

    If *typed* is set to true, function arguments of different types will be
    cached separately. If *typed* is false, the implementation will usually
    regard them as equivalent calls and only cache a single result. (Some
    types such as *str* and *int* may be cached separately even when *typed*
    is false.)

    Note, type specificity applies only to the function’s immediate arguments
    rather than their contents. The scalar arguments, `Decimal(42)` and
    `Fraction(42)` are be treated as distinct calls with distinct results.
    In contrast, the tuple arguments `('answer', Decimal(42))` and
    `('answer', Fraction(42))` are treated as equivalent.

    The wrapped function is instrumented with a `cache_parameters()`
    function that returns a new [`dict`](stdtypes.html#dict "dict") showing the values for *maxsize*
    and *typed*. This is for information purposes only. Mutating the values
    has no effect.

    To help measure the effectiveness of the cache and tune the *maxsize*
    parameter, the wrapped function is instrumented with a `cache_info()`
    function that returns a [named tuple](../glossary.html#term-named-tuple) showing *hits*, *misses*,
    *maxsize* and *currsize*.

    The decorator also provides a `cache_clear()` function for clearing or
    invalidating the cache.

    The original underlying function is accessible through the
    `__wrapped__` attribute. This is useful for introspection, for
    bypassing the cache, or for rewrapping the function with a different cache.

    The cache keeps references to the arguments and return values until they age
    out of the cache or until the cache is cleared.

    If a method is cached, the `self` instance argument is included in the
    cache. See [How do I cache method calls?](../faq/programming.html#faq-cache-method-calls)

    An [LRU (least recently used) cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_(LRU))
    works best when the most recent calls are the best predictors of upcoming
    calls (for example, the most popular articles on a news server tend to
    change each day). The cache’s size limit assures that the cache does not
    grow without bound on long-running processes such as web servers.

    In general, the LRU cache should only be used when you want to reuse
    previously computed values. Accordingly, it doesn’t make sense to cache
    functions with side-effects, functions that need to create
    distinct mutable objects on each call (such as generators and async functions),
    or impure functions such as time() or random().

    Example of an LRU cache for static web content:

    Copy

    ```
    @lru_cache(maxsize=32)
    def get_pep(num):
        'Retrieve text of a Python Enhancement Proposal'
        resource = f'https://peps.python.org/pep-{num:04d}'
        try:
            with urllib.request.urlopen(resource) as s:
                return s.read()
        except urllib.error.HTTPError:
            return 'Not Found'

    >>> for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
    ...     pep = get_pep(n)
    ...     print(n, len(pep))

    >>> get_pep.cache_info()
    CacheInfo(hits=3, misses=8, maxsize=32, currsize=8)

    ```

    Example of efficiently computing
    [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number)
    using a cache to implement a
    [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
    technique:

    Copy

    ```
    @lru_cache(maxsize=None)
    def fib(n):
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)

    >>> [fib(n) for n in range(16)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    >>> fib.cache_info()
    CacheInfo(hits=28, misses=16, maxsize=None, currsize=16)

    ```

    Changed in version 3.3: Added the *typed* option.

    Changed in version 3.8: Added the *user\_function* option.

    Changed in version 3.9: Added the function `cache_parameters()`