from __future__ import annotations

import csv
from collections.abc import MutableSequence, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, NoReturn, Optional


def getCurrentTime() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parseHarmonyInfo(tempFile: Path) -> list[str]:
    """Get information about the scene from the file Harmony wrote to"""
    with tempFile.open("r", encoding="utf-8") as f:
        return f.read().split(",")


def formatInformation(
    infoFromHarmony: MutableSequence[Any],
    infoAboutRender: Sequence[Any],
) -> tuple[Any, ...]:
    """Reorganize information before writing to the TSV file"""
    *timeStamps, jobId = infoAboutRender
    jobStartTime, renderStartTime, renderEndTime = timeStamps

    infoFromHarmony.insert(0, jobStartTime)
    infoFromHarmony.insert(-1, renderStartTime)
    infoFromHarmony.insert(-1, renderEndTime)
    infoFromHarmony.append(jobId)

    return tuple(infoFromHarmony)


def writeToTsv(infoToWrite: Sequence[str | int], tsvFile: Path) -> None:
    """Write the information to the TSV file"""
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
    willWriteHeaders = not (tsvFile.exists() and tsvFile.is_file())

    with tsvFile.open("a", encoding="utf-8") as f:
        writer = csv.writer(f, dialect=csv.excel_tab)
        if willWriteHeaders:
            writer.writerow(headers)
        writer.writerow(infoToWrite)


def logResults(
    tsvFile: Path,
    tempFile: Path,
    jobId: int,
    jobStartTime: str,
    renderStartTime: str,
    renderEndTime: str,
):
    infoFromHarmony = parseHarmonyInfo(tempFile)
    infoAboutRender = jobStartTime, renderStartTime, renderEndTime, jobId
    formattedInfo = formatInformation(
        infoFromHarmony, infoAboutRender=infoAboutRender
    )
    writeToTsv(formattedInfo, tsvFile)


def printResults(
    successfulRenders: Sequence[str], errorMessages: Sequence[str]
) -> Optional[NoReturn]:
    """Print the file names of successful renders and error messages"""

    def printErrorMessages():
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
            printErrorMessages()
    else:
        printErrorMessages()
        exit(1)
