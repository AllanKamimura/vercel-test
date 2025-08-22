import datetime as dt

from dash import dcc, html


def create_layout():
    return html.Div(
        [
            html.H1("Community Session Metrics", style={"textAlign": "center"}),
            html.Div(
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "center",
                    "alignItems": "flex-start",
                    "gap": "20px",
                    "margin": "20px 0",
                },
                children=[
                    html.Div(
                        [
                            html.Label(
                                "Date Range",
                                style={"display": "block", "fontWeight": "bold"},
                            ),
                            dcc.DatePickerRange(
                                id="date-range-picker",
                                min_date_allowed=dt.date(2024, 4, 1),
                                max_date_allowed=dt.datetime.now(),
                                start_date=dt.date(2025, 3, 30),
                                end_date=dt.datetime.now(),
                                display_format="YYYY-MM-DD",
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Question Type",
                                style={"display": "block", "fontWeight": "bold"},
                            ),
                            dcc.Dropdown(
                                id="question-type-dropdown",
                                options=[
                                    {"label": "All", "value": "all"},
                                    {"label": "What is 1P", "value": "what_is_1p"},
                                    {
                                        "label": "Troubleshooting 1P",
                                        "value": "troubleshooting_1p",
                                    },
                                    {"label": "How to 1P", "value": "how_to_1p"},
                                    {
                                        "label": "Is X Supported 1P",
                                        "value": "is_x_supported_1p",
                                    },
                                    {
                                        "label": "Help Implement Extended 1P",
                                        "value": "help_implement_extended_1p",
                                    },
                                    {"label": "Other", "value": "other"},
                                    {
                                        "label": "Is X Supported 3P",
                                        "value": "is_x_supported_3p",
                                    },
                                    {
                                        "label": "Comparison to 3P",
                                        "value": "comparison_to_3p",
                                    },
                                    {"label": "How to 3P", "value": "how_to_3p"},
                                    {
                                        "label": "Troubleshooting 3P",
                                        "value": "troubleshooting_3p",
                                    },
                                    {
                                        "label": "Comparison to 1P",
                                        "value": "comparison_to_1p",
                                    },
                                    {
                                        "label": "Account Issues",
                                        "value": "account_issues",
                                    },
                                    {
                                        "label": "Migrate from 3P",
                                        "value": "migrate_from_3p",
                                    },
                                    {
                                        "label": "Prospecting & Pricing",
                                        "value": "prospecting_and_pricing",
                                    },
                                ],
                                value="all",
                                placeholder="Select Question Type",
                                style={"minWidth": "250px"},
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Sentiment",
                                style={"display": "block", "fontWeight": "bold"},
                            ),
                            dcc.Dropdown(
                                id="sentiment-dropdown",
                                options=[
                                    {"label": "All", "value": "all"},
                                    {"label": "Positive", "value": "positive"},
                                    {"label": "Neutral", "value": "neutral"},
                                    {"label": "Negative", "value": "negative"},
                                ],
                                value="all",
                                placeholder="Select Sentiment",
                                style={"minWidth": "200px"},
                            ),
                        ]
                    ),
                ],
            ),
            dcc.Graph(id="metrics-graph"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                "Top Products this Period",
                                style={"textAlign": "left"},
                            ),
                            html.Img(
                                id="wordcloud_products",
                                style={"width": "100%", "maxWidth": "600px"},
                            ),
                        ],
                        style={"flex": "1", "padding": "10px"},
                    ),
                    html.Div(
                        [
                            html.H2(
                                "Top Terms this Period",
                                style={"textAlign": "left"},
                            ),
                            html.Img(
                                id="wordcloud_subjects",
                                style={"width": "100%", "maxWidth": "600px"},
                            ),
                        ],
                        style={"flex": "1", "padding": "10px"},
                    ),
                    html.Div(
                        [
                            html.H2(
                                "Top Subjects this Period",
                                style={"textAlign": "left"},
                            ),
                            html.Img(
                                id="wordcloud_category",
                                style={"width": "100%", "maxWidth": "600px"},
                            ),
                        ],
                        style={"flex": "1", "padding": "10px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "alignItems": "flex-start",
                    "gap": "20px",
                    "margin": "30px 0",
                },
            ),
            html.Div(
                id="data-list",
                style={
                    "height": "300px",
                    "overflowY": "scroll",
                    "border": "1px solid #ccc",
                    "padding": "10px",
                    "fontFamily": "monospace",
                },
            ),
        ]
    )
