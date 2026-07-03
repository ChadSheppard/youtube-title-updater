#!/usr/bin/env python3
"""
Updates the YouTube video title with live view + like count.
Runs on a schedule via GitHub Actions (.github/workflows/update-title.yml).
Credentials come from environment variables, set as GitHub Actions secrets.
Costs 51 API units per run (1 fetch + 50 update).
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ── CONFIG ────────────────────────────────────────────────────────────────────

VIDEO_ID       = "HwFCkIESaOU"
TITLE_TEMPLATE = "This Video Has {views} Views, {likes} & {comments}"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# ── AUTH ──────────────────────────────────────────────────────────────────────

def get_authenticated_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

# ── UPDATE ────────────────────────────────────────────────────────────────────

def update_title(youtube):
    resp    = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID).execute()
    item    = resp["items"][0]
    snippet = item["snippet"]
    views    = int(item["statistics"].get("viewCount", 0))
    likes    = int(item["statistics"].get("likeCount", 0))
    comments = int(item["statistics"].get("commentCount", 0))

    new_title = TITLE_TEMPLATE.format(
        views    = f"{views:,}",
        likes    = f"{likes:,} {'Like' if likes == 1 else 'Likes'}",
        comments = f"{comments:,} {'Comment' if comments == 1 else 'Comments'}",
    )

    print(f"Old: {snippet['title']}")
    print(f"New: {new_title}")

    if snippet["title"] == new_title:
        print("No change.")
        return

    snippet["title"] = new_title
    youtube.videos().update(
        part="snippet",
        body={"id": VIDEO_ID, "snippet": snippet}
    ).execute()
    print("Title updated.")

# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    youtube = get_authenticated_service()
    update_title(youtube)
