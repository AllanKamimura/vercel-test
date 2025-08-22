import plotly.graph_objects as go
from dash import Input, Output

from app.data import get_discourse_df_agg


def register_callbacks(app):
    @app.callback(
        Output("metrics-graph", "figure"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("question-type-dropdown", "value"),
        Input("sentiment-dropdown", "value"),
    )
    def update(start_date, end_date, question_type, sentiment):
        community_df = get_discourse_df_agg(start_date, end_date)

        return update_graph(community_df)

    def update_graph(community_df):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=community_df["date"],
                y=community_df["solved_norm"],
                mode="lines+markers",
                name="Solved by Bot",
                fill="tozeroy",
                fillcolor="rgba(0,0,255,0.15)",
                line=dict(
                    color="blue",
                    width=2,
                ),
                marker=dict(
                    symbol="star",
                    size=10,
                ),
                hovertemplate="<b>Acceptance rate:</b> %{y:.3f}<br><b>Week Date:</b> %{x}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=community_df["date"],
                y=community_df["likes"],
                mode="lines+markers",
                name="Community Likes",
                fill="tozeroy",
                line=dict(
                    color="green",
                    width=2,
                ),
                marker=dict(
                    size=10,
                    symbol="circle",
                ),
                fillcolor="rgba(0,255,0,0.15)",
                hovertemplate="<b>Like rate:</b> %{y:.3f}<br><b>Week Date:</b> %{x}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=community_df["date"],
                y=community_df["dislikes"],
                mode="lines+markers",
                name="Community Dislikes",
                fill="tozeroy",
                line=dict(
                    color="red",
                    width=2,
                ),
                marker=dict(
                    size=10,
                    symbol="square",
                ),
                fillcolor="rgba(255,0,0,0.15)",
                hovertemplate="<b>Dislikes rate:</b> %{y:.3f}<br><b>Week Date:</b> %{x}<extra></extra>",
            )
        )

        fig.update_layout(
            title="ToradexAI Metrics",
            xaxis_title="Date by Week",
            yaxis_title="Normalized Metric",
        )

        return fig
