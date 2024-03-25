import os
import subprocess
import tempfile
import uuid
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

import myt.files
import myt.logs

HARMONY_SCRIPTS_DIR = Path(__file__).with_name("harmony")
PRE_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "prerender.js"
POST_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "postrender.js"

G_DRIVE = HARMONY_SCRIPTS_DIR.parents[2]


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
    result = subprocess.run(args)
    if result.returncode:
        return "Harmony failure    : " + scene.stem
    return None


def main(sceneFiles: Sequence[Path]) -> None:
    jobStartTime = myt.logs.time()

    tempFile = tempfile.NamedTemporaryFile(prefix="myt_render_")
    env = os.environ
    env["MYT_TEMP_FILE"] = tempFile.name
    env["MYT_G_DRIVE"] = f"{G_DRIVE}"

    tempFilePath = Path(tempFile.name)
    tsvFile = G_DRIVE / "myt_render_log.tsv"

    successfulRenders: list[str] = []
    errorMessages: list[str] = []

    for scene in sceneFiles:
        jobId = uuid.uuid4().time_hi_version
        renderStartTime = myt.logs.time()

        if errorMessage := myt.files.verify(scene):
            errorMessages.append(errorMessage)
            continue

        shot = myt.files.ShotID.fromFilename(scene.stem)
        renderPath = myt.files.findRenderPath(shot, G_DRIVE)

        env["MYT_RENDER_DIR"] = f"{renderPath}"
        env["MYT_RENDER_VER"] = myt.files.newVersion(renderPath)

        if errorMessage := render(scene):
            errorMessages.append(errorMessage)
            continue

        successfulRenders.append(scene.stem)
        renderEndTime = myt.logs.time()
        myt.logs.write(
            tsvFile,
            tempFile=tempFilePath,
            jobId=jobId,
            jobStartTime=jobStartTime,
            renderStartTime=renderStartTime,
            renderEndTime=renderEndTime,
        )
    myt.logs.show(successfulRenders, errorMessages=errorMessages)
