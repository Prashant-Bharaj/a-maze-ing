#!/usr/bin/env python3
"""
Graphical maze display using MiniLibX (mlx). For Ubuntu eval; pygame not allowed.
Run with -g/--graphical or call run_graphics(gen, path).
Requires: pip install ./mlx-2.2-py3-ubuntu-any.whl  (on Ubuntu/WSL)
"""

import ctypes
from ctypes import cast, POINTER, c_uint32
from typing import List, TYPE_CHECKING

from maze_pathfinding import get_path_cells

if TYPE_CHECKING:
    from maze import MazeGenerator

try:
    import mlx
except ImportError:
    mlx = None  # type: ignore[assignment]

MARGIN = 24
CELL_SIZE_DEFAULT = 28
WALL_THICKNESS = 2


def _rgb(r: int, g: int, b: int) -> int:
    return (r << 16) | (g << 8) | b


COLOR_BG = _rgb(250, 250, 252)
COLOR_WALL = _rgb(40, 44, 52)
COLOR_PATH = _rgb(129, 199, 132)
COLOR_42 = _rgb(187, 222, 251)
COLOR_ENTRY = _rgb(102, 187, 106)
COLOR_EXIT = _rgb(239, 83, 80)


def _set_rect(
    arr: ctypes.Array,
    width: int,
    size_line: int,
    img_h: int,
    x: int,
    y: int,
    w: int,
    h: int,
    color: int,
) -> None:
    sl = size_line // 4
    for dy in range(h):
        for dx in range(w):
            px, py = x + dx, y + dy
            if 0 <= px < width and 0 <= py < img_h:
                arr[py * sl + px] = color


def _set_circle(
    arr: ctypes.Array,
    width: int,
    size_line: int,
    img_h: int,
    cx: int,
    cy: int,
    r: int,
    color: int,
) -> None:
    sl = size_line // 4
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                px, py = cx + dx, cy + dy
                if 0 <= px < width and 0 <= py < img_h:
                    arr[py * sl + px] = color


def _draw_into_image(
    mlx_ptr: object,
    img: object,
    gen: "MazeGenerator",
    path: List[str],
    w: int,
    h: int,
    cell_size: int,
    show_path: bool,
    show_42: bool,
) -> None:
    cs = cell_size
    addr, bpp, size_line, endian = mlx.mlx_get_data_addr(img)
    arr = cast(addr, POINTER(c_uint32))
    sl = size_line // 4

    path_cells = set(get_path_cells(gen, path)) if (show_path and path) else set()
    pattern_cells = gen.get_42_pattern_cells() if show_42 else set()
    entry_rc = (gen.entry[1], gen.entry[0])
    exit_rc = (gen.exit[1], gen.exit[0])

    for py in range(h):
        for px in range(w):
            arr[py * sl + px] = COLOR_BG

    for row in range(gen.height):
        for col in range(gen.width):
            x0, y0 = MARGIN + col * cs, MARGIN + row * cs
            c = (
                COLOR_PATH
                if (row, col) in path_cells
                else (COLOR_42 if (row, col) in pattern_cells else None)
            )
            if c is not None:
                _set_rect(arr, w, size_line, h, x0, y0, cs, cs, c)

    t = WALL_THICKNESS
    for row in range(gen.height):
        for col in range(gen.width):
            walls = gen.maze[(row, col)]
            x0, y0 = MARGIN + col * cs, MARGIN + row * cs
            if walls & gen.NORTH:
                _set_rect(arr, w, size_line, h, x0, y0, cs, t, COLOR_WALL)
            if walls & gen.SOUTH:
                _set_rect(arr, w, size_line, h, x0, y0 + cs, cs, t, COLOR_WALL)
            if walls & gen.WEST:
                _set_rect(arr, w, size_line, h, x0, y0, t, cs, COLOR_WALL)
            if walls & gen.EAST:
                _set_rect(arr, w, size_line, h, x0 + cs, y0, t, cs, COLOR_WALL)

    _set_rect(arr, w, size_line, h, 0, 0, w, MARGIN, COLOR_WALL)
    _set_rect(arr, w, size_line, h, 0, 0, MARGIN, h, COLOR_WALL)
    _set_rect(arr, w, size_line, h, w - MARGIN, 0, MARGIN, h, COLOR_WALL)
    _set_rect(arr, w, size_line, h, 0, h - MARGIN, w, MARGIN, COLOR_WALL)

    rad = max(4, cs // 3)
    for (r, c), color in [(entry_rc, COLOR_ENTRY), (exit_rc, COLOR_EXIT)]:
        cx = MARGIN + c * cs + cs // 2
        cy = MARGIN + r * cs + cs // 2
        _set_circle(arr, w, size_line, h, cx, cy, rad, color)


def run_graphics(
    gen: "MazeGenerator",
    path: List[str],
    *,
    show_path: bool = True,
    show_42: bool = True,
    cell_size: int = CELL_SIZE_DEFAULT,
    title: str = "A-MAZE-ING",
) -> None:
    """
    Open an MLX (MiniLibX) window and display the maze. Closes on ESC or Q.

    Args:
        gen: MazeGenerator with a generated maze.
        path: Shortest path from find_shortest_path.
        show_path: Draw the solution path.
        show_42: Highlight the 42 pattern cells.
        cell_size: Pixels per cell.
        title: Window title.

    Raises:
        RuntimeError: If mlx is not installed (use mlx-2.2-py3-ubuntu-any.whl on Ubuntu).
    """
    if mlx is None:
        raise RuntimeError(
            "mlx (MiniLibX) is required. On Ubuntu: pip install ./mlx-2.2-py3-ubuntu-any.whl"
        )

    w = gen.width * cell_size + MARGIN * 2
    h = gen.height * cell_size + MARGIN * 2

    init = getattr(mlx, "mlx_init", getattr(mlx, "init", None))
    if init is None:
        raise RuntimeError("mlx has no mlx_init or init; got: " + str(dir(mlx)))

    mlx_ptr = init()
    if mlx_ptr is None:
        raise RuntimeError("mlx_init failed (no X11 display?)")

    new_win = getattr(mlx, "mlx_new_window", getattr(mlx, "new_window", None))
    new_img = getattr(mlx, "mlx_new_image", getattr(mlx, "new_image", None))
    get_addr = getattr(mlx, "mlx_get_data_addr", getattr(mlx, "get_data_addr", None))
    put_img = getattr(
        mlx, "mlx_put_image_to_window", getattr(mlx, "put_image_to_window", None)
    )
    key_hook = getattr(mlx, "mlx_key_hook", getattr(mlx, "key_hook", None))
    loop = getattr(mlx, "mlx_loop", getattr(mlx, "loop", None))
    loop_end = getattr(mlx, "mlx_loop_end", getattr(mlx, "loop_end", None))

    for name, fn in [
        ("new_window", new_win),
        ("new_image", new_img),
        ("get_data_addr", get_addr),
        ("put_image_to_window", put_img),
        ("key_hook", key_hook),
        ("loop", loop),
    ]:
        if fn is None:
            raise RuntimeError("mlx missing: " + name + "; " + str(dir(mlx)))

    title_b = title.encode("utf-8") if isinstance(title, str) else title
    win = new_win(mlx_ptr, w, h, title_b)
    img = new_img(mlx_ptr, w, h)

    _draw_into_image(mlx_ptr, img, gen, path, w, h, cell_size, show_path, show_42)
    put_img(mlx_ptr, win, img, 0, 0)

    done = [False]

    def on_key(key: int, _: object) -> None:
        # X11: ESC=65307, q=113
        if key in (65307, 113):
            done[0] = True
            if loop_end:
                loop_end(mlx_ptr)

    key_hook(win, on_key, None)
    loop(mlx_ptr)

    for n in ("mlx_destroy_image", "mlx_destroy_window", "mlx_destroy_display"):
        fn = getattr(mlx, n, None)
        if fn is not None:
            try:
                if "image" in n:
                    fn(mlx_ptr, img)
                elif "window" in n:
                    fn(mlx_ptr, win)
                else:
                    fn(mlx_ptr)
            except Exception:
                pass
