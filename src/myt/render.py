import os
import subprocess
import uuid
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import myt.files
import myt.logs

HARMONY_SCRIPTS_PATH = Path(__file__).with_name("harmony")
PRE_RENDER_SCRIPT = HARMONY_SCRIPTS_PATH / "prerender.js"
POST_RENDER_SCRIPT = HARMONY_SCRIPTS_PATH / "postrender.js"

RENDER_DIR = HARMONY_SCRIPTS_PATH.parents[2]


def render(scene: Path) -> Optional[str]:
    """Render the Harmony scene, then return an error message if any"""
    args = (
        "Harmony Premium",
        "-readonly",
        "-batch",
        scene,
        "-preRenderScript",
        PRE_RENDER_SCRIPT,
        "-postRenderScript",
        POST_RENDER_SCRIPT,
    )
    if subprocess.run(args).returncode:
        return "Harmony failure    : " + scene.stem
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
        renderPath = myt.files.findRenderPath(shot, RENDER_DIR)

        env["MYT_RENDER_PATH"] = f"{renderPath}"
        env["MYT_RENDER_VERSION"] = myt.files.newVersion(renderPath)

        if errorMessage := render(scene):
            errorMessages.append(errorMessage)
            continue

        successfulRenders.append(scene.stem)
        renderEndTime = myt.logs.time()
        myt.logs.write(
            RENDER_DIR,
            jobId=jobId,
            jobStartTime=jobStartTime,
            renderStartTime=renderStartTime,
            renderEndTime=renderEndTime,
            harmonyInfoFile=harmonyInfoFile,
        )
    myt.logs.show(successfulRenders, errorMessages=errorMessages)
