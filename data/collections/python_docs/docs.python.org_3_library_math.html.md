|  |  |
| --- | --- |
| **Number-theoretic functions** | |
| [`comb(n, k)`](#math.comb "math.comb") | Number of ways to choose *k* items from *n* items without repetition and without order |
| [`factorial(n)`](#math.factorial "math.factorial") | *n* factorial |
| [`gcd(*integers)`](#math.gcd "math.gcd") | Greatest common divisor of the integer arguments |
| [`isqrt(n)`](#math.isqrt "math.isqrt") | Integer square root of a nonnegative integer *n* |
| [`lcm(*integers)`](#math.lcm "math.lcm") | Least common multiple of the integer arguments |
| [`perm(n, k)`](#math.perm "math.perm") | Number of ways to choose *k* items from *n* items without repetition and with order |
| **Floating point arithmetic** | |
| [`ceil(x)`](#math.ceil "math.ceil") | Ceiling of *x*, the smallest integer greater than or equal to *x* |
| [`fabs(x)`](#math.fabs "math.fabs") | Absolute value of *x* |
| [`floor(x)`](#math.floor "math.floor") | Floor of *x*, the largest integer less than or equal to *x* |
| [`fma(x, y, z)`](#math.fma "math.fma") | Fused multiply-add operation: `(x * y) + z` |
| [`fmod(x, y)`](#math.fmod "math.fmod") | Remainder of division `x / y` |
| [`modf(x)`](#math.modf "math.modf") | Fractional and integer parts of *x* |
| [`remainder(x, y)`](#math.remainder "math.remainder") | Remainder of *x* with respect to *y* |
| [`trunc(x)`](#math.trunc "math.trunc") | Integer part of *x* |
| **Floating point manipulation functions** | |
| [`copysign(x, y)`](#math.copysign "math.copysign") | Magnitude (absolute value) of *x* with the sign of *y* |
| [`frexp(x)`](#math.frexp "math.frexp") | Mantissa and exponent of *x* |
| [`isclose(a, b, rel_tol, abs_tol)`](#math.isclose "math.isclose") | Check if the values *a* and *b* are close to each other |
| [`isfinite(x)`](#math.isfinite "math.isfinite") | Check if *x* is neither an infinity nor a NaN |
| [`isinf(x)`](#math.isinf "math.isinf") | Check if *x* is a positive or negative infinity |
| [`isnan(x)`](#math.isnan "math.isnan") | Check if *x* is a NaN (not a number) |
| [`ldexp(x, i)`](#math.ldexp "math.ldexp") | `x * (2**i)`, inverse of function [`frexp()`](#math.frexp "math.frexp") |
| [`nextafter(x, y, steps)`](#math.nextafter "math.nextafter") | Floating-point value *steps* steps after *x* towards *y* |
| [`ulp(x)`](#math.ulp "math.ulp") | Value of the least significant bit of *x* |
| **Power, exponential and logarithmic functions** | |
| [`cbrt(x)`](#math.cbrt "math.cbrt") | Cube root of *x* |
| [`exp(x)`](#math.exp "math.exp") | *e* raised to the power *x* |
| [`exp2(x)`](#math.exp2 "math.exp2") | *2* raised to the power *x* |
| [`expm1(x)`](#math.expm1 "math.expm1") | *e* raised to the power *x*, minus 1 |
| [`log(x, base)`](#math.log "math.log") | Logarithm of *x* to the given base (*e* by default) |
| [`log1p(x)`](#math.log1p "math.log1p") | Natural logarithm of *1+x* (base *e*) |
| [`log2(x)`](#math.log2 "math.log2") | Base-2 logarithm of *x* |
| [`log10(x)`](#math.log10 "math.log10") | Base-10 logarithm of *x* |
| [`pow(x, y)`](#math.pow "math.pow") | *x* raised to the power *y* |
| [`sqrt(x)`](#math.sqrt "math.sqrt") | Square root of *x* |
| **Summation and product functions** | |
| [`dist(p, q)`](#math.dist "math.dist") | Euclidean distance between two points *p* and *q* given as an iterable of coordinates |
| [`fsum(iterable)`](#math.fsum "math.fsum") | Sum of values in the input *iterable* |
| [`hypot(*coordinates)`](#math.hypot "math.hypot") | Euclidean norm of an iterable of coordinates |
| [`prod(iterable, start)`](#math.prod "math.prod") | Product of elements in the input *iterable* with a *start* value |
| [`sumprod(p, q)`](#math.sumprod "math.sumprod") | Sum of products from two iterables *p* and *q* |
| **Angular conversion** | |
| [`degrees(x)`](#math.degrees "math.degrees") | Convert angle *x* from radians to degrees |
| [`radians(x)`](#math.radians "math.radians") | Convert angle *x* from degrees to radians |
| **Trigonometric functions** | |
| [`acos(x)`](#math.acos "math.acos") | Arc cosine of *x* |
| [`asin(x)`](#math.asin "math.asin") | Arc sine of *x* |
| [`atan(x)`](#math.atan "math.atan") | Arc tangent of *x* |
| [`atan2(y, x)`](#math.atan2 "math.atan2") | `atan(y / x)` |
| [`cos(x)`](#math.cos "math.cos") | Cosine of *x* |
| [`sin(x)`](#math.sin "math.sin") | Sine of *x* |
| [`tan(x)`](#math.tan "math.tan") | Tangent of *x* |
| **Hyperbolic functions** | |
| [`acosh(x)`](#math.acosh "math.acosh") | Inverse hyperbolic cosine of *x* |
| [`asinh(x)`](#math.asinh "math.asinh") | Inverse hyperbolic sine of *x* |
| [`atanh(x)`](#math.atanh "math.atanh") | Inverse hyperbolic tangent of *x* |
| [`cosh(x)`](#math.cosh "math.cosh") | Hyperbolic cosine of *x* |
| [`sinh(x)`](#math.sinh "math.sinh") | Hyperbolic sine of *x* |
| [`tanh(x)`](#math.tanh "math.tanh") | Hyperbolic tangent of *x* |
| **Special functions** | |
| [`erf(x)`](#math.erf "math.erf") | [Error function](https://en.wikipedia.org/wiki/Error_function) at *x* |
| [`erfc(x)`](#math.erfc "math.erfc") | [Complementary error function](https://en.wikipedia.org/wiki/Error_function) at *x* |
| [`gamma(x)`](#math.gamma "math.gamma") | [Gamma function](https://en.wikipedia.org/wiki/Gamma_function) at *x* |
| [`lgamma(x)`](#math.lgamma "math.lgamma") | Natural logarithm of the absolute value of the [Gamma function](https://en.wikipedia.org/wiki/Gamma_function) at *x* |
| **Constants** | |
| [`pi`](#math.pi "math.pi") | *π* = 3.141592… |
| [`e`](#math.e "math.e") | *e* = 2.718281… |
| [`tau`](#math.tau "math.tau") | *τ* = 2*π* = 6.283185… |
| [`inf`](#math.inf "math.inf") | Positive infinity |
| [`nan`](#math.nan "math.nan") | “Not a number” (NaN) |