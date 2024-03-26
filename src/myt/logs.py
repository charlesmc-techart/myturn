from __future__ import annotations

import csv
from collections.abc import Sequence
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import NoReturn, Optional


def time() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write(
    tsvFile: Path,
    tempFile: TextIOWrapper,
    jobId: int,
    jobStartTime: str,
    renderStartTime: str,
    renderEndTime: str,
):
    """Write the information to the TSV file"""
    with tempFile:
        infoFromHarmony = tempFile.read().split(",")
    # infoFromHarmony is formatted as :
    # infoFromHarmony = [
    #     versionName,
    #     numberOfFrames,
    #     startFrame,
    #     endFrame,
    #     colorSpace,
    #     renderedFrames
    # ]
    formattedInfo = (
        jobStartTime,
        *infoFromHarmony[:5],
        renderStartTime,
        renderEndTime,
        infoFromHarmony[-1],
        jobId,
    )

    willWriteHeaders = not (tsvFile.exists() and tsvFile.is_file())
    with tsvFile.open("a", encoding="utf-8") as f:
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
