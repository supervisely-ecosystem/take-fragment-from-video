import os

import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import mkdir

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id()
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

PROJECT_INFO = api.project.get_info_by_id(id=PROJECT_ID)
PROJECT_META = sly.ProjectMeta.from_json(data=api.project.get_meta(PROJECT_ID))

DATASET_INFO = None
if DATASET_ID is not None:
    DATASET_INFO = api.dataset.get_info_by_id(id=DATASET_ID)

STORAGE_DIR = os.path.join(sly.app.get_data_dir(), "video")
mkdir(STORAGE_DIR, True)

DOWNLOAD_THRESHOLD = 0.25
FULL_VIDEO = "full_video"
BY_FRAME = "by_frame"
