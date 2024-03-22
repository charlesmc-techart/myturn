from datetime import datetime
from pathlib import Path


def get_current_time() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def verify_scene(scene_path: Path) -> str:
    """Verify if the scene path is a valid Harmony scene."""
    if not scene_path.exists():
        return f"Path does not exist: {scene_path}"
    elif not scene_path.suffix == ".xstage":
        return "Not a Harmony scene: " + scene_path.name
    elif "myt" not in scene_path.stem:
        return "Not a My Turn scene: " + scene_path.stem
    return ""


def get_sequence(scene_path: Path) -> tuple[str, str]:
    """Get the act and shot numbers based on the scene path."""

    def get_act_shot_numbers(scene_name: str) -> tuple[str, str]:
        act, shot = scene_name.split("_")[1:3]
        return act[-1], shot

    if scene_path.stem.lower().startswith("myt"):
        return get_act_shot_numbers(scene_path.stem)

    # If scene name doesn't start with "myt", get string after "myt"
    scene_name_tail = scene_path.stem.split("myt")[-1]
    try:
        act_num, shot_num = get_act_shot_numbers(scene_name_tail)
    except ValueError:
        return "0", "000"
    else:
        return act_num, shot_num


def find_render_dir(act_num: str, shot_num: str, g_drive: Path) -> Path:
    """Find the directory based on the act and shot numbers."""

    def filter_dir(filter: str, dir: Path) -> Path:
        for d in dir.iterdir():
            if d.is_dir() and d.stem.endswith(filter):
                return d

    act_dir = filter_dir(act_num, g_drive)
    return filter_dir(shot_num, act_dir) / "EXR"


def get_current_version_num(dir: Path) -> int:
    """Get the current version of the render by counting the number of folders."""
    dirs = [
        d
        for d in dir.iterdir()
        if (d.is_dir() and d.stem.lower().startswith("myt"))
    ]
    if not dirs:
        return 0

    dirs.sort()
    last_item = f"{dirs[-1]}"

    try:
        current_ver = int(last_item.rsplit("v", 1)[-1])
    except ValueError:
        return len(dirs)
    else:
        return current_ver


def set_version_suffix(num: int) -> str:
    """Set the version number and format it as 'v000'."""
    return "v" + f"{num + 1}".rjust(3, "0")


def set_version(dir: Path) -> str:
    """Get the current version and set the version suffix."""
    ver = get_current_version_num(dir)
    return set_version_suffix(ver)
