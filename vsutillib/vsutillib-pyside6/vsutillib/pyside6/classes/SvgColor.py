"""
SvgColor defines the recognized SVG color keywords

colors https://en.wikipedia.org/wiki/Web_colors
"""

from typing import ClassVar

from PySide6.QtGui import QColor

class SvgColor:
    """
    Standard SVG color labels
    """

    aliceblue: ClassVar[QColor] = QColor(240, 248, 255)
    antiquewhite: ClassVar[QColor] = QColor(250, 235, 215)
    aqua: ClassVar[QColor] = QColor(0, 255, 255)
    aquamarine: ClassVar[QColor] = QColor(127, 255, 212)
    azure: ClassVar[QColor] = QColor(240, 255, 255)
    beige: ClassVar[QColor] = QColor(245, 245, 220)
    bisque: ClassVar[QColor] = QColor(255, 228, 196)
    black: ClassVar[QColor] = QColor(0, 0, 0)
    blanchedalmond: ClassVar[QColor] = QColor(255, 235, 205)
    blue: ClassVar[QColor] = QColor(0, 0, 255)
    blueviolet: ClassVar[QColor] = QColor(138, 43, 226)
    brown: ClassVar[QColor] = QColor(165, 42, 42)
    burlywood: ClassVar[QColor] = QColor(222, 184, 135)
    cadetblue: ClassVar[QColor] = QColor(95, 158, 160)
    chartreuse: ClassVar[QColor] = QColor(127, 255, 0)
    chocolate: ClassVar[QColor] = QColor(210, 105, 30)
    coral: ClassVar[QColor] = QColor(255, 127, 80)
    cornflowerblue: ClassVar[QColor] = QColor(100, 149, 237)
    cornsilk: ClassVar[QColor] = QColor(255, 248, 220)
    crimson: ClassVar[QColor] = QColor(220, 20, 60)
    cyan: ClassVar[QColor] = QColor(0, 255, 255)
    darkblue: ClassVar[QColor] = QColor(0, 0, 139)
    darkcyan: ClassVar[QColor] = QColor(0, 139, 139)
    darkgoldenrod: ClassVar[QColor] = QColor(184, 134, 11)
    darkgray: ClassVar[QColor] = QColor(169, 169, 169)
    darkgreen: ClassVar[QColor] = QColor(0, 100, 0)
    darkgrey: ClassVar[QColor] = QColor(169, 169, 169)
    darkkhaki: ClassVar[QColor] = QColor(189, 183, 107)
    darkmagenta: ClassVar[QColor] = QColor(139, 0, 139)
    darkolivegreen: ClassVar[QColor] = QColor(85, 107, 47)
    darkorange: ClassVar[QColor] = QColor(255, 140, 0)
    darkorchid: ClassVar[QColor] = QColor(153, 50, 204)
    darkred: ClassVar[QColor] = QColor(139, 0, 0)
    darksalmon: ClassVar[QColor] = QColor(233, 150, 122)
    darkseagreen: ClassVar[QColor] = QColor(143, 188, 143)
    darkslateblue: ClassVar[QColor] = QColor(72, 61, 139)
    darkslategray: ClassVar[QColor] = QColor(47, 79, 79)
    darkslategrey: ClassVar[QColor] = QColor(47, 79, 79)
    darkturquoise: ClassVar[QColor] = QColor(0, 206, 209)
    darkviolet: ClassVar[QColor] = QColor(148, 0, 211)
    deeppink: ClassVar[QColor] = QColor(255, 20, 147)
    deepskyblue: ClassVar[QColor] = QColor(0, 191, 255)
    dimgray: ClassVar[QColor] = QColor(105, 105, 105)
    dimgrey: ClassVar[QColor] = QColor(105, 105, 105)
    dodgerblue: ClassVar[QColor] = QColor(30, 144, 255)
    firebrick: ClassVar[QColor] = QColor(178, 34, 34)
    floralwhite: ClassVar[QColor] = QColor(255, 250, 240)
    forestgreen: ClassVar[QColor] = QColor(34, 139, 34)
    fuchsia: ClassVar[QColor] = QColor(255, 0, 255)
    gainsboro: ClassVar[QColor] = QColor(220, 220, 220)
    ghostwhite: ClassVar[QColor] = QColor(248, 248, 255)
    gold: ClassVar[QColor] = QColor(255, 215, 0)
    goldenrod: ClassVar[QColor] = QColor(218, 165, 32)
    gray: ClassVar[QColor] = QColor(128, 128, 128)
    grey: ClassVar[QColor] = QColor(128, 128, 128)
    green: ClassVar[QColor] = QColor(0, 128, 0)
    greenyellow: ClassVar[QColor] = QColor(173, 255, 47)
    honeydew: ClassVar[QColor] = QColor(240, 255, 240)
    hotpink: ClassVar[QColor] = QColor(255, 105, 180)
    indianred: ClassVar[QColor] = QColor(205, 92, 92)
    indigo: ClassVar[QColor] = QColor(75, 0, 130)
    ivory: ClassVar[QColor] = QColor(255, 255, 240)
    khaki: ClassVar[QColor] = QColor(240, 230, 140)
    lavender: ClassVar[QColor] = QColor(230, 230, 250)
    lavenderblush: ClassVar[QColor] = QColor(255, 240, 245)
    lawngreen: ClassVar[QColor] = QColor(124, 252, 0)
    lemonchiffon: ClassVar[QColor] = QColor(255, 250, 205)
    lightblue: ClassVar[QColor] = QColor(173, 216, 230)
    lightcoral: ClassVar[QColor] = QColor(240, 128, 128)
    lightcyan: ClassVar[QColor] = QColor(224, 255, 255)
    lightgoldenrodyellow: ClassVar[QColor] = QColor(250, 250, 210)
    lightgray: ClassVar[QColor] = QColor(211, 211, 211)
    lightgreen: ClassVar[QColor] = QColor(144, 238, 144)
    lightgrey: ClassVar[QColor] = QColor(211, 211, 211)
    lightpink: ClassVar[QColor] = QColor(255, 182, 193)
    lightsalmon: ClassVar[QColor] = QColor(255, 160, 122)
    lightseagreen: ClassVar[QColor] = QColor(32, 178, 170)
    lightskyblue: ClassVar[QColor] = QColor(135, 206, 250)
    lightslategray: ClassVar[QColor] = QColor(119, 136, 153)
    lightslategrey: ClassVar[QColor] = QColor(119, 136, 153)
    lightsteelblue: ClassVar[QColor] = QColor(176, 196, 222)
    lightyellow: ClassVar[QColor] = QColor(255, 255, 224)
    lime: ClassVar[QColor] = QColor(0, 255, 0)
    limegreen: ClassVar[QColor] = QColor(50, 205, 50)
    linen: ClassVar[QColor] = QColor(250, 240, 230)
    magenta: ClassVar[QColor] = QColor(255, 0, 255)
    maroon: ClassVar[QColor] = QColor(128, 0, 0)
    mediumaquamarine: ClassVar[QColor] = QColor(102, 205, 170)
    mediumblue: ClassVar[QColor] = QColor(0, 0, 205)
    mediumorchid: ClassVar[QColor] = QColor(186, 85, 211)
    mediumpurple: ClassVar[QColor] = QColor(147, 112, 219)
    mediumseagreen: ClassVar[QColor] = QColor(60, 179, 113)
    mediumslateblue: ClassVar[QColor] = QColor(123, 104, 238)
    mediumspringgreen: ClassVar[QColor] = QColor(0, 250, 154)
    mediumturquoise: ClassVar[QColor] = QColor(72, 209, 204)
    mediumvioletred: ClassVar[QColor] = QColor(199, 21, 133)
    midnightblue: ClassVar[QColor] = QColor(25, 25, 112)
    mintcream: ClassVar[QColor] = QColor(245, 255, 250)
    mistyrose: ClassVar[QColor] = QColor(255, 228, 225)
    moccasin: ClassVar[QColor] = QColor(255, 228, 181)
    navajowhite: ClassVar[QColor] = QColor(255, 222, 173)
    navy: ClassVar[QColor] = QColor(0, 0, 128)
    oldlace: ClassVar[QColor] = QColor(253, 245, 230)
    olive: ClassVar[QColor] = QColor(128, 128, 0)
    olivedrab: ClassVar[QColor] = QColor(107, 142, 35)
    orange: ClassVar[QColor] = QColor(255, 165, 0)
    orangered: ClassVar[QColor] = QColor(255, 69, 0)
    orchid: ClassVar[QColor] = QColor(218, 112, 214)
    palegoldenrod: ClassVar[QColor] = QColor(238, 232, 170)
    palegreen: ClassVar[QColor] = QColor(152, 251, 152)
    paleturquoise: ClassVar[QColor] = QColor(175, 238, 238)
    palevioletred: ClassVar[QColor] = QColor(219, 112, 147)
    papayawhip: ClassVar[QColor] = QColor(255, 239, 213)
    peachpuff: ClassVar[QColor] = QColor(255, 218, 185)
    peru: ClassVar[QColor] = QColor(205, 133, 63)
    pink: ClassVar[QColor] = QColor(255, 192, 203)
    plum: ClassVar[QColor] = QColor(221, 160, 221)
    powderblue: ClassVar[QColor] = QColor(176, 224, 230)
    purple: ClassVar[QColor] = QColor(128, 0, 128)
    red: ClassVar[QColor] = QColor(255, 0, 0)
    rosybrown: ClassVar[QColor] = QColor(188, 143, 143)
    royalblue: ClassVar[QColor] = QColor(65, 105, 225)
    saddlebrown: ClassVar[QColor] = QColor(139, 69, 19)
    salmon: ClassVar[QColor] = QColor(250, 128, 114)
    sandybrown: ClassVar[QColor] = QColor(244, 164, 96)
    seagreen: ClassVar[QColor] = QColor(46, 139, 87)
    seashell: ClassVar[QColor] = QColor(255, 245, 238)
    sienna: ClassVar[QColor] = QColor(160, 82, 45)
    silver: ClassVar[QColor] = QColor(192, 192, 192)
    skyblue: ClassVar[QColor] = QColor(135, 206, 235)
    slateblue: ClassVar[QColor] = QColor(106, 90, 205)
    slategray: ClassVar[QColor] = QColor(112, 128, 144)
    snow: ClassVar[QColor] = QColor(255, 250, 250)
    springgreen: ClassVar[QColor] = QColor(0, 255, 127)
    steelblue: ClassVar[QColor] = QColor(70, 130, 180)
    tan: ClassVar[QColor] = QColor(210, 180, 140)
    teal: ClassVar[QColor] = QColor(0, 128, 128)
    thistle: ClassVar[QColor] = QColor(216, 191, 216)
    tomato: ClassVar[QColor] = QColor(255, 99, 71)
    turquoise: ClassVar[QColor] = QColor(64, 224, 208)
    violet: ClassVar[QColor] = QColor(238, 130, 238)
    wheat: ClassVar[QColor] = QColor(245, 222, 179)
    white: ClassVar[QColor] = QColor(255, 255, 255)
    whitesmoke: ClassVar[QColor] = QColor(245, 245, 245)
    yellow: ClassVar[QColor] = QColor(255, 255, 0)
    yellowgreen: ClassVar[QColor] = QColor(154, 205, 50)
