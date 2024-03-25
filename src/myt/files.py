from __future__ import annotations

from pathlib import Path
from typing import NoReturn, Optional

SHOW = "myt"


def verify(scene: Path) -> Optional[str]:
    """Verify if the path is a valid Harmony scene"""
    if not scene.exists():
        return f"Path does not exist: {scene}"
    elif scene.suffix != ".xstage":
        return "Not a Harmony scene: " + scene.name
    elif SHOW not in scene.stem:
        return "Not a My Turn! scene: " + scene.stem
    return None


class MyTurnInvalidFilenameError(ValueError):
    """File does not adhere to My Turn!'s filename protocol"""

    def __init__(self, filename: str) -> None:
        message = (
            f"The scene's filename, {filename}, must contain "
            "'myt_a#_###' for the script to work properly."
        )
        super().__init__(message)


class ShotID:
    """Shot identifier used in asset filenames, formatted `a#_###`"""

    __slots__ = "name", "act", "number", "full"

    def __new__(cls, name: str) -> ShotID:
        try:
            int(name[3:])
        except ValueError as e:
            raise ValueError(f"{name} must follow 'a#_###'") from e
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
            raise MyTurnInvalidFilenameError(filename)
        name = filename.split(affix, 1)[-1][:6]
        return cls(name)


class GoogleSharedDriveDirectoryNotFoundError(FileNotFoundError):
    """Provided directory could not be found on the Google shared drive"""

    def __init__(self, dir: Path | str) -> None:
        super().__init__(
            f"The directory, {dir}, could not be found on a Google shared drive"
        )


def findRenderPath(shot: ShotID, parentDir: Path) -> Path | NoReturn:
    """Get the path to the specific shot directory"""

    def findDir(identifier: str, parentDir: Path) -> Path | NoReturn:
        for d in parentDir.iterdir():
            if d.is_dir() and d.stem.endswith(identifier):
                return d
        raise GoogleSharedDriveDirectoryNotFoundError(
            parentDir / ("*" + identifier)
        )

    actDir = findDir(shot.act, parentDir=parentDir)
    return findDir(shot.number, parentDir=actDir) / "EXR"


def newVersion(dir: Path, versionIndicator: str = "v") -> str:
    """Construct a directory name version, formatted `v###`"""
    dirs = [d for d in dir.iterdir() if d.is_dir() and SHOW in d.name]

    def construct(version: int) -> str:
        return versionIndicator + f"{version + 1}".zfill(3)

    if not dirs:
        version = 0
        return construct(version)

    dirs.sort()
    lastItem = f"{dirs[-1]}"
    try:
        version = int(lastItem.rsplit(versionIndicator, 1)[-1])
    except ValueError:
        version = len(dirs)

    return construct(version)
