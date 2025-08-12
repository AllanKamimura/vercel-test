import base64
import re
from io import BytesIO

import pandas as pd
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, Response
from wordcloud import WordCloud

app = FastAPI()


# Utility to fetch and process Google Sheets data
def read_sheets(url, decimal=","):
    url = url.replace("/edit#gid=", "/export?format=tsv&gid=")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(BytesIO(response.content), sep="\t", decimal=decimal)


# Endpoint: Metrics aggregation
@app.get("/metrics")
def get_metrics(
    inkeep_sheets_url: str = Query(...),
    discourse_url: str = Query(...),
    discourse_api_key: str = Query(...),
    discourse_api_username: str = Query(...),
    query_id: int = Query(45),
):
    # Discourse data
    url = f"{discourse_url}/admin/plugins/explorer/queries/{query_id}/run"
    headers = {
        "Api-Key": discourse_api_key,
        "Api-Username": discourse_api_username,
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, json={"params": None}, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception:
        data = {"rows": [], "columns": []}

    df_weekly = pd.DataFrame(data["rows"], columns=data["columns"])
    df_weekly["date"] = pd.to_datetime(df_weekly["date"], errors="coerce")
    df_weekly["likes"] = df_weekly["likes"] / df_weekly["total_posts_bot"]
    df_weekly["dislikes"] = df_weekly["dislikes"] / df_weekly["total_posts_bot"]
    df_weekly["likes_norm"] = df_weekly["likes"] / (
        df_weekly["likes"] + df_weekly["dislikes"]
    )
    df_weekly["dislikes_norm"] = df_weekly["dislikes"] / (
        df_weekly["likes"] + df_weekly["dislikes"]
    )

    # Inkeep data
    df = read_sheets(inkeep_sheets_url)
    df["firstMessageTime"] = pd.to_datetime(df["firstMessageTime"], errors="coerce")
    df["lastMessageTime"] = pd.to_datetime(df["lastMessageTime"], errors="coerce")
    integration_ids = {
        "cm4r77s3x00o29r0azseh0rw6": "community",
        "cm4r6pg3r00n4qal3kd96tau9": "slack",
        "cm40hbe6r00dw25ayvcv5jfg4": "sandbox",
    }
    df["integrationName"] = df["integrationId"].map(integration_ids)
    df["week"] = (
        df["firstMessageTime"]
        .dt.tz_localize(None)
        .dt.to_period("W")
        .apply(lambda r: r.start_time)
    )

    # Example: return weekly metrics and discourse data as JSON
    return JSONResponse(
        {
            "discourse": df_weekly.to_dict(orient="records"),
            "inkeep": df.to_dict(orient="records"),
        }
    )


# Endpoint: Wordcloud image
@app.post("/wordcloud")
def generate_wordcloud_api(text: str):
    # Clean the text
    text = re.sub(r"[;,:]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    try:
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            regexp=r"[\w\.\-\(\)/]+",
            min_font_size=10,
            max_words=100,
        ).generate(text)
    except Exception:
        wc = WordCloud(width=800, height=400).generate("no_data")
    img = wc.to_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    return Response(content=encoded_image, media_type="text/plain")
