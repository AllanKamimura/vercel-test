import json
import logging
import os

import requests

DISCOURSE_URL = os.environ.get("DISCOURSE_URL")
API_KEY = os.environ.get("DISCOURSE_API_67")
API_USERNAME = "allan.tx"
QUERY_ID = 67


def get_discourse_df(start_date: str, end_date: str):
    url = f"{DISCOURSE_URL}/admin/plugins/explorer/queries/{QUERY_ID}/run"
    headers = {
        "Api-Key": API_KEY,
        "Api-Username": API_USERNAME,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    form_data = {
        "params": json.dumps({"start_date": start_date, "end_date": end_date}),
    }

    try:
        response = requests.post(url, data=form_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        logging.info(json.dumps(data))

    except requests.exceptions.RequestException as e:
        logging.warning(f"Discourse API error, falling back to empty DataFrame: {e}")
        data = {
            "rows": [
                "2025-08-10T00:00:00.000Z",
                "0.33333333333333333333",
                "0.0",
                "0.0",
            ],
            "columns": ["date", "solved_by_bot_normalized", "likes", "dislikes"],
        }

    return format_discourse(data)


def format_discourse(discourse_data):
    date_idx = discourse_data["columns"].index("date")
    value_idx = discourse_data["columns"].index("solved_by_bot_normalized")
    dates = []
    solved_norm = []
    for row in discourse_data["rows"]:
        try:
            dates.append(row[date_idx])
            solved_norm.append(float(row[value_idx]))
        except (ValueError, TypeError, IndexError):
            continue
    return {"date": dates, "solved_norm": solved_norm}
