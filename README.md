# hex_wallpaper

Single-file wallpaper generator. Renders a regular hexagonal or square
lattice to a PNG: the canvas is filled with a gap color, and each cell is
filled with a random grayscale shade drawn from a configurable range. The
result is a dark, low-contrast texture intended for use as a desktop
background.

## Installation

Pillow is the only dependency:

```sh
python -m pip install pillow
```

## Examples

Hexagonal lattice at 3456 x 2234, reproducible via a fixed seed:

```sh
python hex_wallpaper.py \
    --width 3456 \
    --height 2234 \
    --cell-size 25 \
    --gap 1.5 \
    --shade-min 8 \
    --shade-max 45 \
    --gap-shade 65 \
    --seed 42 \
    --output wallpaper.png
```

Hexagonal lattice, compact form with a near-black palette:

```sh
python hex_wallpaper.py \
    --cell-size 25 --gap 1 \
    --shade-min 3 --shade-max 26 --gap-shade 42 \
    --output wallpaper.png
```

Square lattice with the same palette:

```sh
python hex_wallpaper.py \
    --shape square \
    --cell-size 25 --gap 1 \
    --shade-min 3 --shade-max 26 --gap-shade 42 \
    --output wallpaper.png
```

## Parameters

| Flag | Default | Description |
| --- | --- | --- |
| `--width` | `3456` | Output image width in pixels. |
| `--height` | `2234` | Output image height in pixels. |
| `--shape` | `hex` | Lattice shape: `hex` or `square`. |
| `--cell-size` | `25` | Lattice pitch: the size of the unshrunk tiling cells in pixels (width across flats for hex, side length for square). |
| `--gap` | `1.5` | Minimum edge-to-edge gap between cells, in pixels. Must be less than `--cell-size`. |
| `--shade-min` | `8` | Lower bound of the cell shade range (grayscale 0-255). |
| `--shade-max` | `45` | Upper bound of the cell shade range (grayscale 0-255). Must be at least `--shade-min`. |
| `--gap-shade` | `65` | Grayscale (0-255) of the canvas, i.e. the color of the gaps between cells. |
| `--seed` | none | Seed for the per-cell random shades. Omit to get a different image on every run. |
| `--supersample` | `2` | Render the lattice at N times the output resolution, then downsample with LANCZOS filtering to soften cell edges. |
| `--output` | `hex_wallpaper.png` or `square_wallpaper.png` | Output PNG path; the default depends on `--shape`. |

Each cell is filled with a uniformly random integer shade in
`[--shade-min, --shade-max]`. The canvas is painted with `--gap-shade`
before cells are drawn, so the gaps take that color. A warning is printed
(and the image is still written) if `--gap-shade` falls within the cell
shade range, since cells of that shade then blend into the gaps.

Sample outputs are committed as `wallpaper_*.png`.
