import os
import subprocess
import tempfile
import uuid
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

import myt.files as mfiles
import myt.logs as mlogs

HARMONY_SCRIPTS_DIR = Path(__file__).with_name("harmony")
PRE_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "prerender.js"
POST_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "postrender.js"


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
    jobStartTime = mlogs.getCurrentTime()

    tempFile = tempfile.NamedTemporaryFile(prefix="myt_render_")
    env = os.environ
    env["MYT_TEMP_FILE"] = tempFile.name
    tempFilePath = Path(tempFile.name)

    gDrive = HARMONY_SCRIPTS_DIR.parents[2]
    env["MYT_G_DRIVE"] = f"{gDrive}"

    tsvFile = gDrive / "myt_render_log.tsv"

    successfulRenders: list[str] = []
    errorMessages: list[str] = []

    for sceneFile in sceneFiles:
        jobId = uuid.uuid4().time_hi_version
        renderStartTime = mlogs.getCurrentTime()

        if errorMessage := mfiles.verifyScene(sceneFile):
            errorMessages.append(errorMessage)
            continue

        shot = mfiles.ShotID.getFromFilename(sceneFile.stem)
        renderDir = mfiles.getShotPath(shot, gDrive)

        env["MYT_RENDER_DIR"] = f"{renderDir}"
        env["MYT_RENDER_VER"] = mfiles.constructVersionSuffix(renderDir)

        if errorMessage := render(sceneFile):
            errorMessages.append(errorMessage)
            continue

        successfulRenders.append(sceneFile.stem)
        renderEndTime = mlogs.getCurrentTime()
        mlogs.logResults(
            tsvFile,
            tempFile=tempFilePath,
            jobId=jobId,
            jobStartTime=jobStartTime,
            renderStartTime=renderStartTime,
            renderEndTime=renderEndTime,
        )
    mlogs.printResults(successfulRenders, errorMessages=errorMessages)
