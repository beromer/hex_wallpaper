#!/usr/bin/env python3
"""Create a dark grayscale wallpaper with a regular hexagonal or square lattice.

Requires: pip install pillow
"""
import argparse
import math
import random
from PIL import Image, ImageDraw


def grayscale(value: str) -> int:
    n = int(value)
    if not 0 <= n <= 255:
        raise argparse.ArgumentTypeError("grayscale values must be 0..255")
    return n


def positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return n


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=positive_int, default=3456)
    parser.add_argument("--height", type=positive_int, default=2234)
    parser.add_argument("--shape", choices=("hex", "square"), default="hex")
    parser.add_argument("--cell-size", type=float, default=25.0,
                        help="lattice pitch / size of unshrunk tiling cells in pixels")
    parser.add_argument("--gap", type=float, default=1.5,
                        help="minimum edge-to-edge gap between cells in pixels")
    parser.add_argument("--shade-min", type=grayscale, default=8)
    parser.add_argument("--shade-max", type=grayscale, default=45)
    parser.add_argument("--gap-shade", type=grayscale, default=65)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--supersample", type=positive_int, default=2)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.output is None:
        args.output = f"{args.shape}_wallpaper.png"

    if not (args.cell_size > 0 and 0 <= args.gap < args.cell_size):
        parser.error("require cell-size > 0 and 0 <= gap < cell-size")
    if args.shade_min > args.shade_max:
        parser.error("shade-min must be <= shade-max")
    if args.shade_min <= args.gap_shade <= args.shade_max:
        print("Warning: gap shade is within the cell shade range; "
              "some cells may blend into gaps.")

    rng = random.Random(args.seed)
    s = args.supersample
    W, H = args.width * s, args.height * s
    image = Image.new("L", (W, H), color=args.gap_shade)
    draw = ImageDraw.Draw(image)

    if args.shape == "hex":
        # Pointy-top regular hexagons. Their centers form a triangular
        # lattice. The pitch is the width across flats of the unshrunk
        # tiling cells.
        pitch_x = args.cell_size
        pitch_y = args.cell_size * math.sqrt(3) / 2
        radius = (args.cell_size - args.gap) / math.sqrt(3)
        vertex_offsets = [
            (math.cos(math.radians(-90 + 60 * k)) * radius * s,
             math.sin(math.radians(-90 + 60 * k)) * radius * s)
            for k in range(6)
        ]

        rows = math.ceil(args.height / pitch_y) + 3
        cols = math.ceil(args.width / pitch_x) + 3
        for row in range(-2, rows):
            cy = row * pitch_y * s
            offset_x = 0.5 * (row % 2)
            for col in range(-2, cols):
                cx = (col + offset_x) * pitch_x * s
                vertices = [(cx + dx, cy + dy) for dx, dy in vertex_offsets]
                shade = rng.randint(args.shade_min, args.shade_max)
                draw.polygon(vertices, fill=shade)
    else:
        # Axis-aligned squares on a regular grid. The pitch is the side
        # length of the unshrunk tiling cells.
        pitch = args.cell_size
        half = (args.cell_size - args.gap) * s / 2

        rows = math.ceil(args.height / pitch) + 3
        cols = math.ceil(args.width / pitch) + 3
        for row in range(-2, rows):
            cy = row * pitch * s
            for col in range(-2, cols):
                cx = col * pitch * s
                shade = rng.randint(args.shade_min, args.shade_max)
                draw.rectangle([cx - half, cy - half, cx + half, cy + half],
                               fill=shade)

    if s > 1:
        image = image.resize((args.width, args.height), Image.Resampling.LANCZOS)
    image.save(args.output)
    print(f"Saved {args.output} ({args.width} x {args.height})")


if __name__ == "__main__":
    main()
