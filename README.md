# YouTube Title Updater

Updates a YouTube video's title with its live view, like, and comment counts,
e.g. `This Video Has 12,345 Views, 678 Likes & 90 Comments`.

Runs every 15 minutes on GitHub Actions — no local machine required.

## How it works

- `update_title.py` fetches the video's stats via the YouTube Data API v3 and
  rewrites the title from `TITLE_TEMPLATE`.
- `.github/workflows/update-title.yml` runs it on a cron schedule.
- OAuth credentials are supplied through repository secrets:
  `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.

## Changing the target video

Edit `VIDEO_ID` (and `TITLE_TEMPLATE` if desired) in `update_title.py` and push.

## Notes

- Each run costs 51 YouTube API quota units (10,000/day free), so a 15-minute
  schedule uses ~4,900 units/day.
- GitHub schedules are best-effort; runs may be delayed a few minutes.
