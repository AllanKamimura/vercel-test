import plotly.graph_objects as go
from dash import Input, Output

from app.data import get_discourse_df


def register_callbacks(app):
    @app.callback(
        Output("metrics-graph", "figure"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("question-type-dropdown", "value"),
        Input("sentiment-dropdown", "value"),
    )
    def update(start_date, end_date, question_type, sentiment):
        community_df = get_discourse_df()

        return update_graph(community_df)

    def update_graph(community_df):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=community_df["date"],
                y=community_df["solved_norm"],
                mode="lines+markers",
                name="Community Likes",
                fill="tozeroy",
                line=dict(color="green"),
            )
        )

        fig.update_layout(
            title="Solved by Bot (normalized) over Date",
            xaxis_title="Date",
            yaxis_title="Solved by Bot (normalized)",
        )

        return fig
