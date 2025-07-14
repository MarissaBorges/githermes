`colorsys` — Conversions between color systems
==============================================

**Source code:** [Lib/colorsys.py](https://github.com/python/cpython/tree/3.13/Lib/colorsys.py)

---

The [`colorsys`](#module-colorsys "colorsys: Conversion functions between RGB and other color systems.") module defines bidirectional conversions of color values
between colors expressed in the RGB (Red Green Blue) color space used in
computer monitors and three other coordinate systems: YIQ, HLS (Hue Lightness
Saturation) and HSV (Hue Saturation Value). Coordinates in all of these color
spaces are floating-point values. In the YIQ space, the Y coordinate is between
0 and 1, but the I and Q coordinates can be positive or negative. In all other
spaces, the coordinates are all between 0 and 1.

The [`colorsys`](#module-colorsys "colorsys: Conversion functions between RGB and other color systems.") module defines the following functions:

colorsys.rgb\_to\_yiq(*r*, *g*, *b*)
:   Convert the color from RGB coordinates to YIQ coordinates.

colorsys.yiq\_to\_rgb(*y*, *i*, *q*)
:   Convert the color from YIQ coordinates to RGB coordinates.

colorsys.rgb\_to\_hls(*r*, *g*, *b*)
:   Convert the color from RGB coordinates to HLS coordinates.

colorsys.hls\_to\_rgb(*h*, *l*, *s*)
:   Convert the color from HLS coordinates to RGB coordinates.

colorsys.rgb\_to\_hsv(*r*, *g*, *b*)
:   Convert the color from RGB coordinates to HSV coordinates.

colorsys.hsv\_to\_rgb(*h*, *s*, *v*)
:   Convert the color from HSV coordinates to RGB coordinates.

Example:

Copy

```
>>> import colorsys
>>> colorsys.rgb_to_hsv(0.2, 0.4, 0.4)
(0.5, 0.5, 0.4)
>>> colorsys.hsv_to_rgb(0.5, 0.5, 0.4)
(0.2, 0.4, 0.4)

```