from dash import Dash

from callbacks import register_callbacks
from layout import create_layout


app = Dash(__name__)
app.layout = create_layout()

# register_callbacks(app, df_inkeep, df_discourse)
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
