from __future__ import annotations

from pathlib import Path
from typing import NoReturn, Optional

SHOW = "myt"


def verify(scene: Path) -> Optional[str]:
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


class ShotID:
    """Shot identifier used in asset filenames, formatted `a#_###`"""

    __slots__ = "name", "act", "number", "full"

    def __new__(cls, name: str) -> ShotID:
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
    def fromFilename(cls, filename: str, affix: str = SHOW + "_") -> ShotID:
        if affix not in filename:
            message = f"Filename {filename!r} must match pattern 'myt_a#_###'"
            raise InvalidFilenameError(message)
        name = filename.split(affix, 1)[-1][:6]
        return cls(name)


def findRenderPath(shot: ShotID, parentDir: Path) -> Path | NoReturn:
    """Get the path to the specific shot directory"""

    class DirectoryNotFoundError(FileNotFoundError):
        """Directory could not be found"""

        def __init__(self, dir: Path | str) -> None:
            super().__init__(f"Could not find directory: '{dir}'")

    def findDir(identifier: str, parentDir: Path) -> Path | NoReturn:
        for d in parentDir.iterdir():
            if d.is_dir() and d.stem.endswith(identifier):
                return d
        raise DirectoryNotFoundError(parentDir / ("*" + identifier))

    actDir = findDir(shot.act, parentDir=parentDir)
    shotDir = findDir(shot.number, parentDir=actDir) / "EXR"
    if shotDir.is_dir():
        return shotDir
    raise DirectoryNotFoundError(shotDir)


def newVersion(dir: Path, versionIndicator: str = "v") -> str:
    """Construct a directory name version, formatted `v###`"""
    dirs = [d for d in dir.iterdir() if d.is_dir() and SHOW in d.name]

    def construct(version: int) -> str:
        return versionIndicator + f"{version + 1}".zfill(3)

    if not dirs:
        version = 0
        return construct(0)

    dirs.sort()
    lastItem = f"{dirs[-1]}"
    try:
        version = int(lastItem.rsplit(versionIndicator, 1)[-1])
    except ValueError:
        version = len(dirs)
    return construct(version)
