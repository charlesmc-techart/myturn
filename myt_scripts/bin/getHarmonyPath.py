#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from pathlib import Path


def main() -> None:
    parser = ArgumentParser(prog="My Turn: Get Harmony Path")
    parser.add_argument("harmony_ver", help="Harmony version number")
    args = parser.parse_args()

    if sys.platform == "win32":
        dir = Path("C:/Program Files (x86)/Toon Boom Animation")
        dir /= f"Toon Boom Harmony {args.harmony_ver} Premium/win64/bin"
    elif sys.platform == "darwin":
        dir = Path(
            f"/Applications/Toon Boom Harmony {args.harmony_ver} Premium"
        )
        dir /= f"Harmony {args.harmony_ver} Premium.app/Contents/tba/macosx/bin"
    print(dir)


if __name__ == "__main__":
    main()
