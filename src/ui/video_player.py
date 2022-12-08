import supervisely as sly
from supervisely.app.widgets import (
    Card,
    Video,
    VideoThumbnail,
    Container,
    InputNumber,
    Field,
)

preview = VideoThumbnail()
preview.hide()

player = Video()


start_frame = InputNumber(value=0, min=0, max=0)
end_frame = InputNumber(value=0, min=0, max=0)

start_field = Field(content=start_frame, title="Start frame")
end_field = Field(content=end_frame, title="End frame")

frame_range_selector = Field(
    content=Container([start_field, end_field], direction="horizontal"),
    title="Select frame range",
)


card = Card(
    "📹 Video preview",
    content=Container(
        [preview, player, frame_range_selector],
        direction="vertical",
    ),
    lock_message='Select video in table by clicking 👆 "SELECT" button on step 3️⃣',
)
card.lock()
