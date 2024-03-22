#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from pathlib import Path


def main() -> None:
    scripts_dir = f"{Path(__file__).resolve().parents[2]}"
    if scripts_dir not in sys.path:
        sys.path.append(scripts_dir)

    import myt_scripts.src.main.render

    parser = ArgumentParser(prog="My Turn: Render EXR")
    parser.add_argument(
        "scene_paths", help="paths to Harmony scene files", nargs="+"
    )
    parser.add_argument(
        "-pr", "--pre_render_script", help="path to pre-render script"
    )
    parser.add_argument(
        "-ps", "--post_render_script", help="path to post-render script"
    )
    args = parser.parse_args()

    myt_scripts.src.main.render.process_render(
        args.scene_paths, args.pre_render_script, args.post_render_script
    )


if __name__ == "__main__":
    main()
