import os
from dotenv import load_dotenv

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

import supervisely as sly
from supervisely.app.widgets import Card, Container, VideoThumbnail
import src.globals as g
import src.ui.input as input
import src.ui.video_selector as video_selector
import src.ui.video_player as video_player
import src.ui.settings as settings
import src.ui.output as output


settings = Container([input.card], direction="horizontal", gap=15, fractions=[1, 1])


input_cards = Container(
    widgets=[video_selector.card, video_player.card],
    direction="horizontal",
    gap=15,
    fractions=[1, 1],
)

layout = Container(
    widgets=[settings, output.card],
    direction="vertical",
    gap=15,
)

app = sly.Application(layout=layout)
video_selector.build_table()
