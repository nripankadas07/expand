"""expand — tab/space conversion with custom stops and modes."""
from __future__ import annotations

from typing import List, Tuple, Union

__all__ = ["ExpandError", "expand", "unexpand"]
__version__ = "0.1.0"


class ExpandError(ValueError):
    """Raised on invalid input."""


def _validate_tabsize(tabsize):
    if isinstance(tabsize, bool) or not isinstance(tabsize, int):
        raise ExpandError("tabsize must be an int")
    if tabsize < 1:
        raise ExpandError("tabsize must be >= 1")
    return tabsize


def _validate_stops(stops):
    if isinstance(stops, int) and not isinstance(stops, bool):
        return (_validate_tabsize(stops),)
    if isinstance(stops, (list, tuple)):
        if not stops:
            raise ExpandError("stops list must be non-empty")
        last = -1
        for s in stops:
            if isinstance(s, bool) or not isinstance(s, int) or s <= last:
                raise ExpandError("stops must be strictly increasing positive ints")
            last = s
        return tuple(stops)
    raise ExpandError("stops must be int or list of ints")


def _next_stop(col, stops):
    for s in stops:
        if s > col:
            return s
    if len(stops) == 1:
        period = stops[0]
    else:
        period = stops[-1] - stops[-2]
    after = stops[-1]
    while after <= col:
        after += period
    return after


def expand(text, tabsize=8, *, leading_only=False):
    """Replace tabs with spaces. tabsize may be an int or list of stops."""
    if not isinstance(text, str):
        raise ExpandError(f"text must be str, got {type(text).__name__}")
    stops = _validate_stops(tabsize)
    out = []
    for line in text.split("\n"):
        new_line = []
        col = 0
        seen_non_ws = False
        for ch in line:
            if ch == "\t" and (not leading_only or not seen_non_ws):
                target = _next_stop(col, stops)
                spaces = target - col
                new_line.append(" " * spaces)
                col = target
            else:
                if ch != " " and ch != "\t":
                    seen_non_ws = True
                new_line.append(ch)
                col += 1
        out.append("".join(new_line))
    return "\n".join(out)


def unexpand(text, tabsize=8, *, leading_only=True, all_blanks=False):
    """Replace runs of spaces with tabs where possible."""
    if not isinstance(text, str):
        raise ExpandError(f"text must be str, got {type(text).__name__}")
    stops = _validate_stops(tabsize)
    out = []
    for line in text.split("\n"):
        result = []
        col = 0
        i = 0
        n = len(line)
        in_leading = True
        while i < n:
            if line[i] == " " and (in_leading or all_blanks or not leading_only):
                j = i
                pushed = False
                while j < n and line[j] == " ":
                    j += 1
                    if _next_stop(col, stops) == col + (j - i):
                        result.append("\t")
                        col += (j - i)
                        i = j
                        pushed = True
                        break
                if not pushed:
                    while i < n and line[i] == " ":
                        result.append(" ")
                        col += 1
                        i += 1
                continue
            if line[i] != " " and line[i] != "\t":
                in_leading = False
            result.append(line[i])
            col += 1
            i += 1
        out.append("".join(result))
    return "\n".join(out)
