import supervisely as sly
from supervisely.app.widgets import Card, DatasetThumbnail, ProjectThumbnail

import src.globals as g

if g.DATASET_ID is None:
    card = Card(
        "1️⃣ Input project",
        "Select videos in current project",
        collapsable=True,
        content=ProjectThumbnail(g.PROJECT_INFO),
    )
else:
    card = Card(
        "1️⃣ Input dataset",
        "Select videos in current dataset",
        collapsable=True,
        content=DatasetThumbnail(g.PROJECT_INFO, g.DATASET_INFO),
    )
