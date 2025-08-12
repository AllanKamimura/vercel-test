from app.callbacks import register_callbacks
from dash import Dash
from app.layout import create_layout

app = Dash(__name__)
app.layout = create_layout()

# register_callbacks(app, df_inkeep, df_discourse)
register_callbacks(app)

if __name__ == "__main__":
    app.run(port=8080, dev_tools_ui=True, debug=True, host="127.0.0.1")
