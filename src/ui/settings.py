# import supervisely as sly
# from supervisely.app.widgets import Card, InputNumber, Container, Field
# import src.globals as g


# start_frame = InputNumber(value=1, min=1, max=1)
# end_frame = InputNumber(value=1, min=1, max=1)

# start_field = Field(content=start_frame, title="Start frame")
# end_field = Field(content=end_frame, title="End frame")

# card = Card(
#     "Select frame range",
#     "Selected frame range will be extracted",
#     collapsable=False,
#     content=Container([start_field, end_field], direction="horizontal", gap=5),
#     lock_message="Select video in table by clicking 👆 'SELECT' button on step 3️⃣",
# )
# card.lock()
