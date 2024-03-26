from __future__ import annotations

import csv
from collections.abc import Sequence
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import NoReturn, Optional

_LOG_FILENAME = "myt_render_log.tsv"


def time() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write(
    dir: Path,
    jobId: int,
    jobStartTime: str,
    renderStartTime: str,
    renderEndTime: str,
    harmonyInfoFile: TextIOWrapper,
):
    """Write the information to the TSV file"""
    with harmonyInfoFile:
        harmonyInfo = harmonyInfoFile.read().split(",")
    # harmonyInfo is formatted as:
    # harmonyInfo = [
    #     versionName,
    #     numberOfFrames,
    #     startFrame,
    #     endFrame,
    #     colorSpace,
    #     renderedFrames
    # ]
    formattedInfo = (
        jobStartTime,
        *harmonyInfo[:5],
        renderStartTime,
        renderEndTime,
        harmonyInfo[-1],
        jobId,
    )

    logFile = dir / _LOG_FILENAME
    willWriteHeaders = not (logFile.exists() and logFile.is_file())
    with logFile.open("a", encoding="utf-8") as f:
        writer = csv.writer(f, dialect=csv.excel_tab)
        if willWriteHeaders:
            headers = (
                "Date",
                "Version",
                "Frames",
                "Start",
                "End",
                "Color Space",
                "Started",
                "Finished",
                "Rendered",
                "Job ID",
            )
            writer.writerow(headers)
        writer.writerow(formattedInfo)


def show(
    successfulRenders: Sequence[str], errorMessages: Sequence[str]
) -> Optional[NoReturn]:
    """Print the file names of successful renders and error messages"""

    def showErrorMessages():
        print("Failed to render:")
        for e in errorMessages:
            print(e)

    print()
    if successfulRenders:
        print("Successfully rendered:")
        for item in successfulRenders:
            print(item)
        if errorMessages:
            print()
            showErrorMessages()
    else:
        showErrorMessages()
        exit(1)
