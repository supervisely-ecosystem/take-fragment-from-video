import pandas as pd
import supervisely as sly
from supervisely.app.widgets import Button, Card, Table

import src.globals as g
import src.ui.video_player as video_player

current_video = None

COL_ID = "video id".upper()
COL_DS = "dataset id".upper()
COL_VIDEO = "video".upper()
COL_DURATION = "duration (sec)".upper()
COL_FRAMES = "frames".upper()
SELECT_VIDEO = "select".upper()


columns = [
    COL_ID,
    COL_DS,
    COL_VIDEO,
    COL_DURATION,
    COL_FRAMES,
    SELECT_VIDEO,
]

lines = None
table = Table(fixed_cols=2, width="100%")

reselect_pair_btn = Button("Select other videos", icon="zmdi zmdi-rotate-left")
reselect_pair_btn.hide()

card = Card(
    "2️⃣ Select video",
    "Choose the video from which you wish to extract a fragment",
    collapsable=False,
    content=table,
    content_top_right=reselect_pair_btn,
)


def build_table():
    global table, lines
    if lines is None:
        lines = []
    table.loading = True
    if g.DATASET_ID:
        videos = g.api.video.get_list(g.DATASET_ID)
    else:
        videos = []
        for dataset in g.api.dataset.get_list(project_id=g.PROJECT_ID):
            videos.extend(g.api.video.get_list(dataset.id))
    for info in videos:
        labeling_url = sly.video.get_labeling_tool_url(info.dataset_id, info.id)
        lines.append(
            [
                info.id,
                info.dataset_id,
                sly.video.get_labeling_tool_link(labeling_url, info.name),
                info.duration,
                info.frames_count_compact,
                sly.app.widgets.Table.create_button(SELECT_VIDEO),
            ]
        )
    df = pd.DataFrame(lines, columns=columns)
    table.read_pandas(df)
    table.loading = False


@table.click
def handle_table_button(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    global current_video
    if datapoint.button_name is None:
        return
    video_id = datapoint.row[COL_ID]
    current_video = g.api.video.get_info_by_id(video_id)
    if datapoint.button_name == SELECT_VIDEO:
        video_player.player.set_video(video_id)
        video_player.preview.set_video_id(video_id)
        video_player.preview.show()
        video_player.start_frame.max = current_video.frames_count - 1
        video_player.end_frame.max = current_video.frames_count - 1
        video_player.end_frame.value = current_video.frames_count - 1
        video_player.card.unlock()
