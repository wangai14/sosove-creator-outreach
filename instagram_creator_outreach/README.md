# Instagram Creator Outreach Desk

Local workflow app for Japan Instagram creator discovery, candidate management, outreach copy drafting, reply handling, and campaign tracking.

The app is designed for manual review workflows. It does not log in to Instagram, scrape private Instagram pages, or send bulk DMs automatically.

## Run

```powershell
python -m instagram_creator_outreach.server --port 8796
```

Then open:

```text
http://127.0.0.1:8796/
```

The same server also exposes an independent TikTok creator outreach desk:

```text
http://127.0.0.1:8796/tiktok/
```

Instagram and TikTok use separate candidate files and CSV endpoints. The default TikTok data path is `./data/tiktok_creator_outreach`, configurable with `TIKTOK_OUTREACH_DATA_DIR`.

## Optional API Configuration

Set these environment variables before starting the server if you want API-backed public search or model-generated copy.

```powershell
$env:GOOGLE_CSE_API_KEY = "your-google-custom-search-api-key"
$env:GOOGLE_CSE_CX = "your-programmable-search-engine-id"
$env:SERPAPI_API_KEY = "your-serpapi-key"

$env:META_GRAPH_MODE = ""
$env:META_GRAPH_API_VERSION = "v25.0"
$env:META_ACCESS_TOKEN = "your-long-lived-meta-or-instagram-token"
$env:META_IG_USER_ID = "your-connected-instagram-professional-user-id"

$env:OUTREACH_COPY_MODEL_PROVIDER = "cpa"
$env:OUTREACH_COPY_MODEL_BASE_URL = "https://api.example.com/v1"
$env:OUTREACH_COPY_MODEL_NAME = "your-model-name"
$env:OUTREACH_COPY_MODEL_API_KEY = "your-model-api-key"
```

You can also configure the copy model from the browser UI.

For Instagram API enrichment, keep the token server-side in `.env`. The browser button only asks the backend to enrich the selected handle with official public profile fields such as avatar, followers, biography, website, and media count. `IGAA...` Instagram Login tokens are auto-detected and can enrich only the authorized account itself through `graph.instagram.com/me`. To enrich other creator handles in the candidate pool, use the Facebook/Page connected Instagram professional account flow so `business_discovery` works with `META_IG_USER_ID`.

## VPS Deploy

Clone the private repository on your VPS:

```bash
git clone https://github.com/sosoveooo-bit/instagram-creator-outreach.git
cd instagram-creator-outreach
cp .env.example .env
```

Edit `.env` and fill in only the keys you need. Keep `.env` private.

Run directly with Python:

```bash
python3 -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
```

Run with Docker:

```bash
docker build -t instagram-creator-outreach .
docker run -d --name instagram-creator-outreach \
  --env-file .env \
  -p 8796:8796 \
  -v "$(pwd)/data:/app/data" \
  instagram-creator-outreach
```

Run with systemd:

```bash
sudo mkdir -p /opt/instagram-creator-outreach
sudo cp -r . /opt/instagram-creator-outreach/
sudo cp deploy/instagram-creator-outreach.service.example /etc/systemd/system/instagram-creator-outreach.service
sudo systemctl daemon-reload
sudo systemctl enable --now instagram-creator-outreach
```

If you expose the app publicly, put it behind Nginx and basic auth or another access control layer. The app is intended as a private operator tool.

## Test

```powershell
python -m unittest instagram_creator_outreach.tests.test_backend
node --check instagram_creator_outreach/static/app.js
```

## Included Workflows

- CSV import and candidate de-duplication
- Separate TikTok outreach panel at `/tiktok/`
- Public-search connector via Google CSE or SerpApi
- Compliant collector for user-provided search results, HTML, URLs, and handle lists
- Creator website inspector for public non-Instagram pages
- Official Instagram Graph API enrichment for imported handles
- Candidate pool sorting, pinning, deletion, and CSV export
- Manual outreach queue
- Japanese DM/email copy generation
- OpenAI-compatible or CPA proxy model gateway
- Reply assistant with local rules and optional AI model generation
- Partnership, shipping, posting, coupon, order, revenue, and ROI tracking
