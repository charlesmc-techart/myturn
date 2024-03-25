from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import NoReturn


def getCurrentTime() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def verifyScene(scene: Path) -> str:
    """Verify if the scene path is a valid Harmony scene."""
    if not scene.exists():
        return f"Path does not exist: {scene}"
    elif scene.suffix != ".xstage":
        return "Not a Harmony scene: " + scene.name
    elif "myt" not in scene.stem:
        return "Not a My Turn scene: " + scene.stem
    return ""


def getSequence(scene: Path) -> tuple[str, str]:
    """Get the act and shot numbers based on the scene path."""

    def getActShotNumbers(sceneName: str) -> tuple[str, str]:
        act, shot = sceneName.split("_")[1:3]
        return act[-1], shot

    if scene.stem.lower().startswith("myt"):
        return getActShotNumbers(scene.stem)

    # If scene name doesn't start with "myt", get string after "myt"
    sceneNameTail = scene.stem.split("myt")[-1]
    try:
        actNum, shotNum = getActShotNumbers(sceneNameTail)
    except ValueError:
        return "0", "000"
    else:
        return actNum, shotNum


def findRenderDir(actNum: str, shotNum: str, gDrive: Path) -> Path:
    """Find the directory based on the act and shot numbers."""

    def filterDir(filter: str, dir: Path) -> Path | NoReturn:
        for d in dir.iterdir():
            if d.is_dir() and d.stem.endswith(filter):
                return d
        raise FileNotFoundError

    actDir = filterDir(actNum, gDrive)
    return filterDir(shotNum, actDir) / "EXR"


def getCurrentVersionNum(dir: Path) -> int:
    """Get the current version of the render by counting the number of folders."""
    dirs = [
        d
        for d in dir.iterdir()
        if (d.is_dir() and d.stem.lower().startswith("myt"))
    ]
    if not dirs:
        return 0

    dirs.sort()
    lastItem = f"{dirs[-1]}"

    try:
        currentVer = int(lastItem.rsplit("v", 1)[-1])
    except ValueError:
        return len(dirs)
    else:
        return currentVer


def setVersionSuffix(num: int) -> str:
    """Set the version number and format it as 'v000'."""
    return "v" + f"{num + 1}".zfill(3)


def setVersion(dir: Path) -> str:
    """Get the current version and set the version suffix."""
    ver = getCurrentVersionNum(dir)
    return setVersionSuffix(ver)
