from pathlib import Path

from app import button_manual, card_manual, form_manual, grid_manual, input_manual, heading_manual,text_manual, row_manual, column_manual
from app import media_manual, switch_manual, select_manual, modern_button_manual , nav_interaction_manual
from app import data_feedback_manual , table_manual


from pylage import run

button_manual_app = button_manual.get_app()
media_manual_app = media_manual.get_app()
input_manual_app = input_manual.get_app()
heading_manual_app = heading_manual.get_app()
text_manual_app = text_manual.get_app()
card_manual_app = card_manual.get_app()
row_manual_app = row_manual.get_app()
column_manual_app = column_manual.get_app()
grid_manual_app = grid_manual.get_app()
form_manual_app = form_manual.get_app()
switch_manual_app = switch_manual.get_app()
select_manual_app = select_manual.get_app()
modern_button_manual_app = modern_button_manual.get_app()
nav_interaction_manual_app = nav_interaction_manual.get_app()
data_feedback_manual_app = data_feedback_manual.get_app()
table_manual_app = table_manual.get_app()



run(table_manual_app, title="Manual_testing", output=Path("index.html"),serve=True,host="127.0.0.1", port=8080, open_browser=True)

