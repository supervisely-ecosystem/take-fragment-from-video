import os
import supervisely_lib as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

my_app = sly.AppService()
api: sly.Api = my_app.public_api

TASK_ID = my_app.task_id
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id()
# DATASET_ID = None
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

PROJECT_INFO = api.project.get_info_by_id(id=PROJECT_ID)
PROJECT_META = sly.ProjectMeta.from_json(data=api.project.get_meta(PROJECT_ID))

if DATASET_ID is not None:
    DATASET_INFO = api.dataset.get_info_by_id(id=DATASET_ID)
