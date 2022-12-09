import os
import supervisely as sly
from supervisely.app.widgets import (
    Card,
    Field,
    Input,
    Button,
    Container,
    VideoThumbnail,
    SlyTqdm,
)
import src.globals as g

import src.ui.video_player as video_player
import src.ui.video_selector as video_selector
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# new project
project_name = Input(placeholder="Please input project name")
new_project = Field(
    content=project_name,
    title="Result project",
    description="Define destination project and dataset",
)

dataset_name = Input(placeholder="Please input dataset name")
new_dataset = Field(
    content=dataset_name,
    title="Result dataset",
    description="Frame range will be extracted to this dataset",
)

extract_button = Button(text="Extract frame range")

new_project_container = Container(widgets=[new_project, new_dataset])

progress = SlyTqdm(show_percents=True)
progress.hide()

output_video = VideoThumbnail()
output_video.hide()

destination_container = Container(
    widgets=[new_project_container, extract_button, progress, output_video]
)

card = Card(
    "4️⃣ Output project",
    "Select output destination",
    collapsable=False,
    content=destination_container,
    lock_message="Select video fragment frame range before extracting it at step 3️⃣",
)

card.lock()


@extract_button.click
def extract_frame_range():
    start_frame_val = video_player.start_frame.get_value()
    end_frame_val = video_player.end_frame.get_value()

    if start_frame_val >= end_frame_val:
        raise sly.app.DialogWindowError(
            title="Start frame can't be higher or equal to end frame"
        )

    info = video_selector.current_video
    progress.show()
    with progress(message=f"Processing {info.name}", total=1) as pbar:
        time_codes = info.frames_to_timecodes
        start_time = time_codes[start_frame_val]
        end_time = time_codes[end_frame_val]
        path_to_video = os.path.join(g.STORAGE_DIR, info.name)
        if not os.path.exists(path=path_to_video):
            g.api.video.download_path(
                id=info.id, path=path_to_video, progress_cb=pbar.update
            )
        output_video_name = f"{start_frame_val}_{end_frame_val}_{info.name}"
        output_video_path = os.path.join(g.STORAGE_DIR, output_video_name)
        ffmpeg_extract_subclip(
            filename=path_to_video,
            t1=start_time,
            t2=end_time,
            targetname=output_video_path,
        )

        upload_video_to_destination(
            project_name=project_name.get_value(),
            dataset_name=dataset_name.get_value(),
            video_name=output_video_name,
            video_path=output_video_path,
            progress_cb=pbar.update,
        )


def upload_video_to_destination(
    project_name, dataset_name, video_name, video_path, progress_cb
):
    output_video.hide()

    # project_id = project_selector.get_selected_id()
    project_name = project_name or g.PROJECT_INFO.name
    project = g.api.project.create(
        workspace_id=g.WORKSPACE_ID,
        name=project_name,
        type=sly.ProjectType.VIDEOS,
        change_name_if_conflict=True,
    )

    # dataset_id = dataset_selector.get_selected_id()
    dataset_name = dataset_name or g.DATASET_INFO.name or "ds0"
    dataset = g.api.dataset.create(
        project_id=project.id, name=dataset_name, change_name_if_conflict=True
    )

    video_info = g.api.video.upload_path(
        dataset_id=dataset.id,
        name=video_name,
        path=video_path,
        item_progress=progress_cb,
    )
    output_video.set_video_id(id=video_info.id)
    output_video.show()