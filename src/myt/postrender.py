import csv
from collections.abc import MutableSequence, Sequence
from pathlib import Path
from typing import Any, NoReturn, Union


def parseHarmonyInfo(tempFilePath: Path) -> list[str]:
    """Get information about the scene from the file Harmony wrote to."""
    with open(tempFilePath, "r") as temp_file:
        return temp_file.read().split(",")


def formatInformation(
    infoFromHarmony: MutableSequence[Any],
    infoAboutRender: Sequence[Any],
) -> tuple[Any, ...]:
    """Reorganize information before writing to the TSV file."""
    (
        execStartTime,
        renderStartTime,
        renderEndTime,
        jobId,
    ) = infoAboutRender

    infoFromHarmony.insert(0, execStartTime)
    infoFromHarmony.insert(-1, renderStartTime)
    infoFromHarmony.insert(-1, renderEndTime)
    infoFromHarmony.append(jobId)

    return tuple(infoFromHarmony)


def writeToTsv(infoToWrite: Sequence[Union[str, int]], tsvPath: Path) -> None:
    """Write the information to the TSV file."""
    writeHeaders = not (tsvPath.exists() and tsvPath.is_file())
    with open(tsvPath, "a") as tsvFile:
        writer = csv.writer(tsvFile, dialect=csv.excel_tab)
        if writeHeaders:
            writer.writerow(
                (
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
            )
        writer.writerow(infoToWrite)


def logResults(
    tempFilePath: Path,
    execStartTime: str,
    renderStartTime: str,
    renderEndTime: str,
    jobId: int,
    tsvPath: Path,
):
    infoFromHarmony = parseHarmonyInfo(tempFilePath)
    formattedInfo = formatInformation(
        infoFromHarmony,
        (
            execStartTime,
            renderStartTime,
            renderEndTime,
            jobId,
        ),
    )
    writeToTsv(formattedInfo, tsvPath)


def printResults(
    successfulRenders: Sequence[str], failedRenders: Sequence[str]
) -> Union[None, NoReturn]:
    """Print the file names of successful renders and error messages."""
    print()
    if successfulRenders:
        print("Successfully rendered:")
        for item in successfulRenders:
            print(item)
        if failedRenders:
            print()
            print("Failed to render:")
            for item in failedRenders:
                print(item)
    else:
        print("Failed to render")
        for item in failedRenders:
            print(item)
        exit(1)
