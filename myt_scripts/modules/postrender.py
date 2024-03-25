import csv
from collections.abc import MutableSequence, Sequence
from pathlib import Path
from typing import Any, NoReturn, Union


def parse_harmony_info(temp_file_path: Path) -> list[str]:
    """Get information about the scene from the file Harmony wrote to."""
    with open(temp_file_path, "r") as temp_file:
        return temp_file.read().split(",")


def format_information(
    info_from_harmony: MutableSequence[Any],
    info_about_render: Sequence[Any],
) -> tuple[Any, ...]:
    """Reorganize information before writing to the TSV file."""
    (
        exect_start_time,
        render_time_start,
        render_time_end,
        job_id,
    ) = info_about_render

    info_from_harmony.insert(0, exect_start_time)
    info_from_harmony.insert(-1, render_time_start)
    info_from_harmony.insert(-1, render_time_end)
    info_from_harmony.append(job_id)

    return tuple(info_from_harmony)


def write_to_tsv(
    info_to_write: Sequence[Union[str, int]], tsv_path: Path
) -> None:
    """Write the information to the TSV file."""
    write_headers = not (tsv_path.exists() and tsv_path.is_file())
    with open(tsv_path, "a") as tsv_file:
        writer = csv.writer(tsv_file, dialect=csv.excel_tab)
        if write_headers:
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
        writer.writerow(info_to_write)


def log_results(
    temp_file_path: Path,
    exec_start_time: str,
    render_time_start: str,
    render_time_end: str,
    job_id: int,
    tsv_path: Path,
):
    info_from_harmony = parse_harmony_info(temp_file_path)
    formatted_info = format_information(
        info_from_harmony,
        (
            exec_start_time,
            render_time_start,
            render_time_end,
            job_id,
        ),
    )
    write_to_tsv(formatted_info, tsv_path)


def print_results(
    successful_renders: Sequence[str], failed_renders: Sequence[str]
) -> Union[None, NoReturn]:
    """Print the file names of successful renders and error messages."""
    print()
    if successful_renders:
        print("Successfully rendered:")
        for item in successful_renders:
            print(item)
        if failed_renders:
            print()
            print("Failed to render:")
            for item in failed_renders:
                print(item)
    else:
        print("Failed to render")
        for item in failed_renders:
            print(item)
        exit(1)
