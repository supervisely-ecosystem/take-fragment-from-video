import os

import supervisely as sly
from dotenv import load_dotenv

# for convenient debug, has no effect in production
if sly.utils.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input
import src.ui.output as output
import src.ui.video_player as video_player
import src.ui.video_selector as video_selector

input_cards = Container(
    widgets=[video_selector.card, video_player.card],
    direction="horizontal",
    gap=15,
    fractions=[1, 1],
)

layout = Container(
    widgets=[input.card, input_cards, output.card],
    direction="vertical",
    gap=15,
)

app = sly.Application(layout=layout)
video_selector.build_table()
