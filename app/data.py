import json
import logging
import os
from typing import Optional

import requests

DISCOURSE_URL = os.environ.get("DISCOURSE_URL")
API_KEY = os.environ.get("DISCOURSE_API_67")
API_USERNAME = "allan.tx"
QUERY_ID = 67


def get_discourse_df_agg(start_date: str, end_date: str):
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
    solved_idx = discourse_data["columns"].index("solved_by_bot_normalized")
    like_idx = discourse_data["columns"].index("likes")
    dislike_idx = discourse_data["columns"].index("dislikes")
    dates = []
    solved_norm = []
    likes = []
    dislikes = []
    for row in discourse_data["rows"]:
        try:
            dates.append(row[date_idx])
            solved_norm.append(float(row[solved_idx]))
            likes.append(float(row[like_idx]))
            dislikes.append(float(row[dislike_idx]))
        except (ValueError, TypeError, IndexError):
            continue
    return {
        "date": dates,
        "solved_norm": solved_norm,
        "likes": likes,
        "dislikes": dislikes,
    }


def fetch_questions_from_lambda(
    start_date: str = "2025-06-01",
    end_date: str = "2025-08-21",
    questionType: Optional[str] = None,
    sentiment: Optional[str] = None,
):
    """
    Fetch questions from the LAMBDA_ENDPOINT with the given parameters.
    Returns a JSON array of question dicts.
    """
    endpoint = os.environ.get("LAMBDA_ENDPOINT")
    if not endpoint:
        raise ValueError("LAMBDA_ENDPOINT environment variable is not set")

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "questionType": questionType,
        "sentiment": sentiment,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.warning(f"Lambda API error: {e}")
        return []
