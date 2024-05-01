from __future__ import annotations

__author__ = "Charles Mesa Cayobit"

import csv
import sys
from collections.abc import Sequence
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import NoReturn

_LOG_FILENAME = "myt_render_log.tsv"


def time() -> str:
    """Get the current time in MM/DD/YYYY HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write(
    dir: Path,
    job_id: int,
    job_start_time: str,
    render_start_time: str,
    render_end_time: str,
    harmony_info_file: TextIOWrapper,
) -> None:
    """Write the information to the TSV file"""
    with harmony_info_file:
        harmony_info = tuple(csv.reader(harmony_info_file))
    # harmony_info is formatted as:
    # harmony_info = [
    #     scene_version_name,
    #     scene_number_of_frames,
    #     scene_start_frame,
    #     scene_end_frame,
    #     scene_color_space,
    #     number_of_rendered_frames
    # ]
    formatted_info = (
        job_start_time,
        *harmony_info[:5],
        render_start_time,
        render_end_time,
        harmony_info[-1],
        job_id,
    )

    log_file = dir / _LOG_FILENAME
    will_write_headers = not (log_file.exists() and log_file.is_file())
    with log_file.open("a", encoding="utf-8") as f:
        writer = csv.writer(f, dialect=csv.excel_tab)
        if will_write_headers:
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
        writer.writerow(formatted_info)


def show(
    successful_renders: Sequence[str], error_messages: Sequence[str]
) -> None | NoReturn:
    """Print the file names of successful renders and error messages"""

    def show_error_messages():
        print("Failed to render:")
        for e in error_messages:
            print(e)

    print()
    if successful_renders:
        print("Successfully rendered:")
        for item in successful_renders:
            print(item)
        if error_messages:
            print()
            show_error_messages()
    else:
        show_error_messages()
        sys.exit(1)
