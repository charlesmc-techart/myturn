from __future__ import annotations

__author__ = "Charles Mesa Cayobit"

from pathlib import Path
from typing import NoReturn

SHOW = "myt"


def verify(scene: Path) -> str | None:
    """Verify if the path is a valid Harmony scene"""

    if not scene.exists():
        return f"Path does not exist: {scene}"
    elif scene.suffix != ".xstage":
        return f"Not a Harmony scene: {scene.name}"
    elif SHOW not in scene.stem:
        return f"Not a My Turn! scene: {scene.stem}"
    return None


class InvalidFilenameError(ValueError):
    """File does not adhere to My Turn!'s filename protocol"""


class ShotId:
    """Shot identifier used in asset filenames, formatted `a#_###`"""

    __slots__ = "name", "act", "number", "full"

    def __new__(cls, name: str) -> ShotId:
        try:
            int(name[3:])
        except ValueError as e:
            message = f"Name {name!r} must match pattern 'a#_###'"
            raise InvalidFilenameError(message) from e
        return super().__new__(cls)

    def __init__(self, name: str) -> None:
        self.name = name
        self.act = name[1:2]
        self.number = name[3:6]
        self.full = f"{SHOW}_{name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"

    @classmethod
    def from_filename(cls, filename: str, affix: str = f"{SHOW}_") -> ShotId:
        if affix not in filename:
            message = f"Filename {filename!r} must match pattern 'myt_a#_###'"
            raise InvalidFilenameError(message)
        name = filename.split(affix, 1)[-1][:6]
        return cls(name)


def find_render_path(shot: ShotId, parent_dir: Path) -> Path | NoReturn:
    """Get the path to the specific shot directory"""

    class DirectoryNotFoundError(FileNotFoundError):
        """Directory could not be found"""

        def __init__(self, dir: Path | str) -> None:
            super().__init__(f"Could not find directory: '{dir}'")

    def find_dir(identifier: str, parent_dir: Path) -> Path | NoReturn:
        for d in parent_dir.iterdir():
            if d.is_dir() and d.stem.endswith(identifier):
                return d
        raise DirectoryNotFoundError(parent_dir / ("*" + identifier))

    act_dir = find_dir(shot.act, parent_dir=parent_dir)
    shot_dir = find_dir(shot.number, parent_dir=act_dir) / "EXR"
    if shot_dir.is_dir():
        return shot_dir
    raise DirectoryNotFoundError(shot_dir)


def new_version(directory: Path, version_indicator: str = "v") -> str:
    """Construct a directory name version, formatted `v###`"""

    dirs = [d for d in directory.iterdir() if d.is_dir() and SHOW in d.name]

    def construct(version: int) -> str:
        return version_indicator + f"{version + 1}".zfill(3)

    if not dirs:
        version = 0
        return construct(version)

    dirs.sort()
    last_item = f"{dirs[-1]}"
    try:
        version = int(last_item.rsplit(version_indicator, 1)[-1])
    except ValueError:
        version = len(dirs)
    return construct(version)
