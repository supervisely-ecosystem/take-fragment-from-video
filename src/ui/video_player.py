import supervisely as sly
from supervisely.app.widgets import (
    Button,
    Card,
    Container,
    Field,
    InputNumber,
    Video,
    VideoThumbnail,
)

import src.ui.output as output

preview = VideoThumbnail()
preview.hide()

player = Video()


start_frame = InputNumber(value=0, min=0, max=0)
end_frame = InputNumber(value=0, min=0, max=0)

start_frame_val = None
end_frame_val = None

start_field = Field(content=start_frame, title="Start frame")
end_field = Field(content=end_frame, title="End frame")

frame_range_selector = Field(
    content=Container([start_field, end_field], direction="horizontal"),
    title="Select video fragment",
    description="Start and end frames will be included in the result fragment",
)


card = Card(
    "3️⃣ Video preview 📹",
    content=Container(
        [preview, player, frame_range_selector],
        direction="vertical",
    ),
    lock_message='Select video in table by clicking 👆 "SELECT" button on step 2️⃣',
)
card.lock()
