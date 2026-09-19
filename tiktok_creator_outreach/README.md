# TikTok Creator Outreach Desk

TikTok creator candidate management and outreach drafting for the SOSOVE Japan workflow.

It is served by the existing Instagram outreach server:

```powershell
python -m instagram_creator_outreach.server --port 8799
```

Open:

```text
http://127.0.0.1:8799/tiktok/
```

The TikTok panel mirrors the Instagram operations desk while keeping its data and browser configuration separate. It includes:

- manual-confirmation outreach queue and task board
- CSV import/export, public-search connector, URL/handle collector, filters, pinning, and deletion
- TikTok-specific scoring based on average/median views, engagement, view-to-follower ratio, posting frequency, fit, safety, and contactability
- metric enrichment, Japanese DM/email/follow-up copy, separate AI model configuration, and reply handling
- campaign, sample, shipping, video progress, Spark Ads authorization, usage-rights, coupon, order, revenue, and ROI tracking

It does not log in to TikTok, scrape hidden APIs, or send unattended bulk DMs.

Optional data path:

```env
TIKTOK_OUTREACH_DATA_DIR=./data/tiktok_creator_outreach
```
