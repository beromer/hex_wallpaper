# AGENTS.md

## What this is

Single-file wallpaper generator: `hex_wallpaper.py` renders a dark grayscale
hexagonal or square lattice to PNG. No tests, lint, typecheck, or CI — the
script is the whole codebase.

## Running

Pillow is the only dependency; it is already installed in `.venv` (Python 3.14):

    .venv/bin/python hex_wallpaper.py --seed 42 --output wallpaper.png

Or install fresh: `python -m pip install pillow` then run with `python`.
Two ready-made example invocations are in `README.md`.

## Notes

- Output is random per run unless `--seed` is passed; use a seed for
  reproducible results when comparing parameter changes.
- Default output is `hex_wallpaper.png` in the current directory; pass
  `--output` otherwise. Generated PNGs are large (~1 MB) — the repo commits
  sample outputs (`wallpaper_*.png`).
- Parameter semantics (non-obvious from names): `--cell-size` is the lattice
  pitch / size of the unshrunk tiling cells (width across flats for hex, side
  length for square); `--gap` is the minimum edge-to-edge gap in pixels and
  must be < `--cell-size`; `--shade-min`/`--shade-max`/`--gap-shade` are
  grayscale 0–255 values; `--shape` is `hex` (default) or `square`.
- The script warns (and continues) if `--gap-shade` falls inside the
  `--shade-min`..`--shade-max` range.
