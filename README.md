# SOSOVE Creator Outreach

Instagram and TikTok creator outreach workspaces for the SOSOVE Japan workflow.

The project is a private operator tool for candidate management, CSV import, public-search connectors, outreach copy drafting, reply handling, and partnership tracking. It does not log in to social accounts, scrape hidden APIs, or send unattended bulk DMs.

## Panels

- Instagram: `http://127.0.0.1:8796/`
- TikTok: `http://127.0.0.1:8796/tiktok/`
- Health check: `http://127.0.0.1:8796/api/health`

Instagram and TikTok use separate data files and endpoints.

## Install On Another Computer

Requirements:

- Git
- Python 3.11 or newer

Clone and start:

```powershell
git clone https://github.com/sosoveooo-bit/sosove-creator-outreach.git
cd sosove-creator-outreach
Copy-Item .env.example .env
python -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
```

On macOS or Linux:

```bash
git clone https://github.com/sosoveooo-bit/sosove-creator-outreach.git
cd sosove-creator-outreach
cp .env.example .env
python3 -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
```

The application uses the Python standard library only, so there is no `pip install` step for the core server.

## Docker

Create `.env` first:

```bash
cp .env.example .env
docker compose up -d --build
```

Change the public port when needed:

```env
PANEL_PORT=8796
```

Persistent candidate data is stored in `./data` on the host.

## Environment Variables

Start with [.env.example](.env.example). The most common integrations are:

```env
GOOGLE_CSE_API_KEY=
GOOGLE_CSE_CX=
SERPAPI_API_KEY=

META_ACCESS_TOKEN=
META_IG_USER_ID=

OUTREACH_COPY_MODEL_PROVIDER=cpa
OUTREACH_COPY_MODEL_BASE_URL=
OUTREACH_COPY_MODEL_NAME=
OUTREACH_COPY_MODEL_API_KEY=
OUTREACH_COPY_MODEL_AUTH_MODE=bearer
```

The model gateway is OpenAI-compatible. CPA proxy mode uses the `/chat/completions` endpoint and bearer authentication by default.

Keep `.env` private. The repository intentionally ignores `.env`, runtime data, logs, CSV exports, and candidate JSON files.

## Tests

```powershell
python -m unittest discover -s instagram_creator_outreach/tests -v
python -m unittest discover -s tiktok_creator_outreach/tests -v
```

## VPS Notes

The Docker command publishes the service directly on the selected port. If the VPS firewall is enabled, allow that port. For public internet exposure, place the panel behind an access-control layer such as a VPN, firewall allowlist, or reverse proxy with authentication.
