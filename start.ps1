$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath ".env")) {
    Copy-Item -LiteralPath ".env.example" -Destination ".env"
    Write-Host "Created .env from .env.example. Add API keys if needed, then run this script again."
}

python -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
