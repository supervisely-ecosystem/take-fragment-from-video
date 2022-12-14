import math
import os
import subprocess

import cv2
import supervisely as sly
from supervisely.app.widgets import (
    Button,
    Card,
    Container,
    DestinationProject,
    SlyTqdm,
    VideoThumbnail,
)

from supervisely.io.fs import mkdir, remove_dir, silent_remove

import src.globals as g
import src.ui.video_player as video_player
import src.ui.video_selector as video_selector

destination = DestinationProject(workspace_id=g.WORKSPACE_ID, project_type="videos")

progress = SlyTqdm()
progress.hide()

output_video = VideoThumbnail()
output_video.hide()

extract_button = Button(text="Extract frame range")
destination_container = Container(widgets=[destination, extract_button, progress, output_video])

card = Card(
    "4️⃣ Output project",
    "Select output destination",
    collapsable=False,
    content=destination_container,
    lock_message="Select video fragment frame range before extracting it at step 3️⃣",
)


def calculate_threshold(video_info, start_frame, end_frame):
    thresh_percent = (end_frame - start_frame) / video_info.frames_count
    return g.FULL_VIDEO if thresh_percent > g.DOWNLOAD_THRESHOLD else g.BY_FRAME


def validate_selected_frame_range(video_info, start_frame, end_frame):
    if start_frame >= end_frame:
        raise sly.app.DialogWindowError(
            title="Please submit correct frames on step 3️⃣",
            description="Start frame can't be higher or equal to end frame",
        )

    if start_frame == 0 and end_frame == video_info.frames_count - 1:
        raise sly.app.DialogWindowError(
            title="Please submit correct frames on step 3️⃣",
            description="You have selected full video length. There's nothing to extract.",
        )


def merge_frames_into_video_fragment(video_info, start_frame, end_frame):
    frames_dir = os.path.join(g.STORAGE_DIR, "frames")
    mkdir(frames_dir, True)
    frame_indexes = list(range(start_frame, end_frame + 1))
    frame_paths = [os.path.join(frames_dir, f"frame_{idx}.png") for idx in frame_indexes]
    g.api.video.frame.download_paths(
        video_id=video_info.id,
        frame_indexes=frame_indexes,
        paths=frame_paths,
    )

    output_video_name = f"{start_frame}_{end_frame}_{video_info.name}"
    output_video_path = os.path.join(g.STORAGE_DIR, output_video_name)

    video = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        g.FRAME_RATE,
        (video_info.frame_width, video_info.frame_height),
    )
    for img_path in frame_paths:
        img = cv2.imread(img_path)
        video.write(img)
        silent_remove(img_path)
    video.release()
    remove_dir(frames_dir)

    if os.path.isfile(output_video_path):
        converted_path = output_video_path.replace(
            output_video_path, f"{output_video_path}_converted.mp4"
        )
        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-i",
                f"{output_video_path}",
                "-c:v",
                "libx264",
                "-c:a",
                "libopus",
                f"{converted_path}",
            ]
        )
        os.remove(output_video_path)
        os.rename(converted_path, output_video_path)

    return output_video_name, output_video_path


def extract_fragment_from_video(video_info, start_frame, end_frame):

    time_codes = video_info.frames_to_timecodes
    start_time = time_codes[start_frame]
    end_time = time_codes[end_frame] + time_codes[1]

    path_to_video = os.path.join(g.STORAGE_DIR, video_info.name)
    if not os.path.exists(path=path_to_video):
        g.api.video.download_path(id=video_info.id, path=path_to_video)

    output_video_name = f"{start_frame}_{end_frame}_{video_info.name}"
    output_video_path = os.path.join(g.STORAGE_DIR, output_video_name)

    subprocess.call(
        [
            "ffmpeg",
            "-ss",
            str(start_time),
            "-to",
            str(end_time),
            "-i",
            f"{path_to_video}",
            "-c:v",
            "libx264",
            f"{output_video_path}",
        ]
    )

    return output_video_name, output_video_path


@extract_button.click
def extract_frame_range():
    output_video.hide()
    progress.show()

    start_frame_val = video_player.start_frame.get_value()
    end_frame_val = video_player.end_frame.get_value()
    info = video_selector.current_video
    validate_selected_frame_range(info, start_frame_val, end_frame_val)

    with progress(message=f"Processing {info.name}", total=3) as pbar:
        download_mode = calculate_threshold(info, start_frame_val, end_frame_val)
        pbar.update()

        if download_mode == g.FULL_VIDEO:
            video_name, video_path = extract_fragment_from_video(
                info, start_frame_val, end_frame_val
            )
        else:
            video_name, video_path = merge_frames_into_video_fragment(
                info, start_frame_val, end_frame_val
            )
        pbar.update()

        upload_video_to_destination(
            project_name=destination.get_project_name(),
            dataset_name=destination.get_dataset_name(),
            video_name=video_name,
            video_path=video_path,
            start_frame=start_frame_val,
            end_frame=end_frame_val,
            progress=pbar,
        )


def upload_video_to_destination(
    project_name, dataset_name, video_name, video_path, start_frame, end_frame, progress
):
    project_id = destination.get_selected_project_id()
    if project_id is None:
        project_name = project_name or g.PROJECT_INFO.name
        project = g.api.project.create(
            workspace_id=g.WORKSPACE_ID,
            name=project_name,
            type=sly.ProjectType.VIDEOS,
            change_name_if_conflict=True,
        )
        project_id = project.id

    dataset_id = destination.get_selected_dataset_id()
    if dataset_id is None:
        dataset_name = dataset_name or "ds0"
        dataset = g.api.dataset.create(
            project_id=project_id, name=dataset_name, change_name_if_conflict=True
        )
        dataset_id = dataset.id

    video_info = g.api.video.upload_path(
        dataset_id=dataset_id,
        name=video_name,
        path=video_path,
        meta={
            "source_project_id": g.PROJECT_ID,
            "start_frame": start_frame,
            "end_frame": end_frame,
        },
    )
    silent_remove(video_path)
    progress.update()
    output_video.set_video_id(id=video_info.id)
    output_video.show()
