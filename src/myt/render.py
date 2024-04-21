from __future__ import annotations

import os
import subprocess
import uuid
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile

import myt.files
import myt.logs

_HARMONY_SCRIPTS_DIR = Path(__file__).with_name("harmony")
_PRE_RENDER_SCRIPT = _HARMONY_SCRIPTS_DIR / "prerender.js"
_POST_RENDER_SCRIPT = _HARMONY_SCRIPTS_DIR / "postrender.js"

_RENDER_DIR = _HARMONY_SCRIPTS_DIR.parents[2]


def render(scene: Path) -> str | None:
    """Render the Harmony scene, then return an error message if any"""
    args = (
        "Harmony Premium",
        "-readonly",
        "-batch",
        scene,
        "-preRenderScript",
        _PRE_RENDER_SCRIPT,
        "-postRenderScript",
        _POST_RENDER_SCRIPT,
    )
    if subprocess.run(args).returncode:
        return f"Harmony failure    : {scene.stem}"
    return None


def main(scene_files: Sequence[Path]) -> None:
    job_start_time = myt.logs.time()

    harmony_info_file = NamedTemporaryFile(mode="r", prefix="myt_render_")
    env = os.environ
    env["MYT_RENDER_INFO_PATH"] = harmony_info_file.name

    successful_renders: list[str] = []
    error_messages: list[str] = []

    for scene in scene_files:
        job_id = uuid.uuid4().time_hi_version
        render_start_time = myt.logs.time()

        if error_message := myt.files.verify(scene):
            error_messages.append(error_message)
            continue

        shot = myt.files.ShotId.from_filename(scene.stem)
        render_path = myt.files.find_render_path(shot, _RENDER_DIR)

        env["MYT_RENDER_PATH"] = f"{render_path}"
        env["MYT_RENDER_VERSION"] = myt.files.new_version(render_path)

        if error_message := render(scene):
            error_messages.append(error_message)
            continue

        successful_renders.append(scene.stem)
        render_end_time = myt.logs.time()
        myt.logs.write(
            _RENDER_DIR,
            job_id=job_id,
            job_start_time=job_start_time,
            render_start_time=render_start_time,
            render_end_time=render_end_time,
            harmony_info_file=harmony_info_file,  # type: ignore
        )
    myt.logs.show(successful_renders, error_messages=error_messages)
