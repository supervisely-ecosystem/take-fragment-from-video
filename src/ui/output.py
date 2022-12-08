import supervisely as sly
from supervisely.app.widgets import (
    Card,
    ProjectSelector,
    SelectDataset,
    Field,
    Input,
    Button,
    Container,
)
import src.globals as g


# new project
new_project = Field(
    content=Input(placeholder="Please input project name"),
    title="Result project",
    description="Define destination project and dataset",
)

new_dataset = Field(
    content=Input(placeholder="Please input dataset name"),
    title="Result dataset",
    description="Frame range will be extracted to this dataset",
)

extract_button = Button(text="Extract frame range")

new_project_container = Container(widgets=[new_project, new_dataset, extract_button])


card = Card(
    "1️⃣ Output project",
    "Select output destination",
    collapsable=True,
    content=new_project_container,
)
