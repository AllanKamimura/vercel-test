from app.callbacks import register_callbacks
from dash import Dash
from app.layout import create_layout

dash_app = Dash(__name__)
dash_app.layout = create_layout()
register_callbacks(dash_app)

app = dash_app.server  # Expose the WSGI app for Vercel

if __name__ == "__main__":
    dash_app.run(port=8080, dev_tools_ui=True, debug=True, host="127.0.0.1")
