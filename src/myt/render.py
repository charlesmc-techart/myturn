import os
import subprocess
import uuid
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import myt.files
import myt.logs

_HARMONY_SCRIPTS_DIR = Path(__file__).with_name("harmony")
_PRE_RENDER_SCRIPT = _HARMONY_SCRIPTS_DIR / "prerender.js"
_POST_RENDER_SCRIPT = _HARMONY_SCRIPTS_DIR / "postrender.js"

_RENDER_DIR = _HARMONY_SCRIPTS_DIR.parents[2]


def render(scene: Path) -> Optional[str]:
    """Render the Harmony scene, then return an error message if any"""
    args = (
        "Harmony Premium",
        "-readonly",
        "-batch",
        scene,
        "-preRenderScript",
        _PRE_RENDER_SCRIPT,
        "-postRenderScript",
        _POST_RENDER_SCRIPT,
    )
    if subprocess.run(args).returncode:
        return f"Harmony failure    : {scene.stem}"
    return None


def main(sceneFiles: Sequence[Path]) -> None:
    jobStartTime = myt.logs.time()

    harmonyInfoFile = NamedTemporaryFile(mode="r", prefix="myt_render_")
    env = os.environ
    env["MYT_RENDER_INFO_PATH"] = harmonyInfoFile.name

    successfulRenders: list[str] = []
    errorMessages: list[str] = []

    for scene in sceneFiles:
        jobId = uuid.uuid4().time_hi_version
        renderStartTime = myt.logs.time()

        if errorMessage := myt.files.verify(scene):
            errorMessages.append(errorMessage)
            continue

        shot = myt.files.ShotID.fromFilename(scene.stem)
        renderPath = myt.files.findRenderPath(shot, _RENDER_DIR)

        env["MYT_RENDER_PATH"] = f"{renderPath}"
        env["MYT_RENDER_VERSION"] = myt.files.newVersion(renderPath)

        if errorMessage := render(scene):
            errorMessages.append(errorMessage)
            continue

        successfulRenders.append(scene.stem)
        renderEndTime = myt.logs.time()
        myt.logs.write(
            _RENDER_DIR,
            jobId=jobId,
            jobStartTime=jobStartTime,
            renderStartTime=renderStartTime,
            renderEndTime=renderEndTime,
            harmonyInfoFile=harmonyInfoFile,
        )
    myt.logs.show(successfulRenders, errorMessages=errorMessages)
