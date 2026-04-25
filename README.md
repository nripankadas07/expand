# expand

Zero-dependency Python library implementing GNU `expand(1)` and `unexpand(1)` semantics: replace tabs with spaces and vice versa, with custom tab stops and leading-only / all-blanks modes.

## Install

```bash
pip install expand
```

Requires Python 3.10+. No runtime dependencies.

## Quick example

```python
from expand import expand, unexpand

expand("a\tb\tc", tabsize=4)             # "a   b   c"
expand("a\tb\tc", tabsize=[4, 8, 12])    # "a   b   c"

unexpand("    hello", tabsize=4)         # "\thello"
unexpand("    a    b", tabsize=4, all_blanks=True)
```

## API

### `expand(text, tabsize=8, *, leading_only=False) -> str`
Replace tabs with spaces. `tabsize` may be a single int (every-N-columns) or a list of strictly-increasing stops.

### `unexpand(text, tabsize=8, *, leading_only=True, all_blanks=False) -> str`
Compress runs of spaces back to tabs where they reach a stop boundary.

### `ExpandError`
Subclass of `ValueError`.

## License

MIT
