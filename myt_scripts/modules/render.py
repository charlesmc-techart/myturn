import os
import subprocess
import tempfile
import uuid
from pathlib import Path

import myt_scripts.src.modules.postrender as myt_post
import myt_scripts.src.modules.prerender as myt_pre


def render_scene(
    scene_path: Path, pre_render_script: str, post_render_script: str
) -> str:
    """Render the Harmony scene, then return a failure message if any."""
    args: list[str] = []
    if pre_render_script:
        args.extend(("-preRenderScript", pre_render_script))
    if post_render_script:
        args.extend(("-postRenderScript", post_render_script))

    result = subprocess.run(
        (
            "Harmony Premium",
            "-readonly",
            "-batch",
            scene_path,
            *args,
        )
    )
    if result.returncode:
        return "Harmony failure    : " + scene_path.stem
    return ""


def process_render(
    scene_paths: list[str], pre_render_script: str, post_render_script: str
) -> None:
    exec_start_time = myt_pre.get_current_time()

    temp_file = tempfile.NamedTemporaryFile(prefix="myt_render_")
    os.environ["MYT_TEMP_FILE"] = temp_file.name
    temp_file_path = Path(temp_file.name)

    g_drive = Path(__file__).resolve().parents[3]
    os.environ["MYT_G_DRIVE"] = f"{g_drive}"

    tsv_path = g_drive / "myt_render_log.tsv"

    successful_renders: list[str] = []
    failed_renders: list[str] = []

    for scene_path in scene_paths:
        job_id = uuid.uuid4().time_hi_version
        render_time_start = myt_pre.get_current_time()

        scene_path = Path(scene_path).resolve()

        if failure_message := myt_pre.verify_scene(scene_path):
            failed_renders.append(failure_message)
            continue

        act_num, shot_num = myt_pre.get_sequence(scene_path)
        render_dir = myt_pre.find_render_dir(act_num, shot_num, g_drive)

        os.environ["MYT_RENDER_DIR"] = f"{render_dir}"
        os.environ["MYT_RENDER_VER"] = myt_pre.set_version(render_dir)

        if failure_message := render_scene(
            scene_path, pre_render_script, post_render_script
        ):
            failed_renders.append(failure_message)
            continue

        successful_renders.append(scene_path.stem)
        render_time_end = myt_pre.get_current_time()
        myt_post.log_results(
            temp_file_path,
            exec_start_time,
            render_time_start,
            render_time_end,
            job_id,
            tsv_path,
        )
    myt_post.print_results(successful_renders, failed_renders)
