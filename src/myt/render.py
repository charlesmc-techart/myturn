import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import myt.postrender as post
import myt.prerender as pre

HARMONY_SCRIPTS_DIR = Path(__file__).with_name("harmony")
PRE_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "prerender.js"
POST_RENDER_SCRIPT = HARMONY_SCRIPTS_DIR / "postrender.js"


def render(scene: Path) -> Optional[str]:
    """Render the Harmony scene, then return a failure message if any."""
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


def main(scenePaths: list[str]) -> None:
    execStartTime = pre.getCurrentTime()

    tempFile = tempfile.NamedTemporaryFile(prefix="myt_render_")
    os.environ["MYT_TEMP_FILE"] = tempFile.name
    tempFilePath = Path(tempFile.name)

    # gDrive = Path(__file__).resolve().parents[2]
    gDrive = Path(
        "/Users/charles_mc/Library/CloudStorage/GoogleDrive-charlesvincent.cayobit@sjsu.edu/Shared drives/BFA_23_24_My_Turn_COMP"
    )
    os.environ["MYT_G_DRIVE"] = f"{gDrive}"

    tsvPath = gDrive / "myt_render_log.tsv"

    successfulRenders: list[str] = []
    failedRenders: list[str] = []

    for scenePath in scenePaths:
        jobId = uuid.uuid4().time_hi_version
        renderStartTime = pre.getCurrentTime()

        scenePath = Path(scenePath).resolve()

        if failureMessage := pre.verifyScene(scenePath):
            failedRenders.append(failureMessage)
            continue

        actNum, shotNum = pre.getSequence(scenePath)
        renderDir = pre.findRenderDir(actNum, shotNum, gDrive)

        os.environ["MYT_RENDER_DIR"] = f"{renderDir}"
        os.environ["MYT_RENDER_VER"] = pre.setVersion(renderDir)

        if failureMessage := render(scenePath):
            failedRenders.append(failureMessage)
            continue

        successfulRenders.append(scenePath.stem)
        renderEndTime = pre.getCurrentTime()
        post.logResults(
            tempFilePath,
            execStartTime,
            renderStartTime,
            renderEndTime,
            jobId,
            tsvPath,
        )
    post.printResults(successfulRenders, failedRenders)
