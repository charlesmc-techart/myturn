import os
import subprocess
import tempfile
import uuid
from pathlib import Path

import myt.modules.postrender as post
import myt.modules.prerender as pre


def renderScene(
    scenePath: Path, preRenderScript: str, postRenderScript: str
) -> str:
    """Render the Harmony scene, then return a failure message if any."""
    args: list[str] = []
    if preRenderScript:
        args.extend(("-preRenderScript", preRenderScript))
    if postRenderScript:
        args.extend(("-postRenderScript", postRenderScript))

    result = subprocess.run(
        (
            "Harmony Premium",
            "-readonly",
            "-batch",
            scenePath,
            *args,
        )
    )
    if result.returncode:
        return "Harmony failure    : " + scenePath.stem
    return ""


def processRender(
    scenePaths: list[str], preRenderScript: str, postRenderScript: str
) -> None:
    execStartTime = pre.getCurrentTime()

    tempFile = tempfile.NamedTemporaryFile(prefix="myt_render_")
    os.environ["MYT_TEMP_FILE"] = tempFile.name
    tempFilePath = Path(tempFile.name)

    gDrive = Path(__file__).resolve().parents[3]
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

        if failureMessage := renderScene(
            scenePath, preRenderScript, postRenderScript
        ):
            failedRenders.append(failureMessage)
            continue

        successfulRenders.append(scenePath.stem)
        renderEndTime = pre.getCurrentTime()
        post.log_results(
            tempFilePath,
            execStartTime,
            renderStartTime,
            renderEndTime,
            jobId,
            tsvPath,
        )
    post.printResults(successfulRenders, failedRenders)
