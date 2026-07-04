#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════
# setup.sh — Environment setup for Jules / accident-main
#
# Usage:
#   chmod +x setup.sh && ./setup.sh
#
# Prerequisites (configured in Jules settings at jules.google.com/settings):
#   GOOGLE_DRIVE_CLIENT_ID      ← OAuth 2.0 Client ID (Desktop app)
#   GOOGLE_DRIVE_CLIENT_SECRET  ← OAuth 2.0 Client Secret
#   GOOGLE_DRIVE_REFRESH_TOKEN  ← Offline refresh token (Drive scopes)
#   GOOGLE_DRIVE_FOLDER_ID      ← (Optional) Target Drive folder ID
# ═══════════════════════════════════════════════════════════════════════════

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "=== setup.sh — accident-main ==="
echo "Repository: $REPO_DIR"
echo ""

# ── Step 1: Python + uv ────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    echo "uv not found. Installing..."
    pip install uv
fi

echo "Installing project dependencies..."
uv sync
echo "Dependencies ready."
echo ""

# ── Step 2: Google Drive Auth ──────────────────────────────────────────
DRIVE_TOKEN_FILE="$REPO_DIR/.drive-token.json"

if [[ -n "${GOOGLE_DRIVE_CLIENT_ID:-}" && \
      -n "${GOOGLE_DRIVE_CLIENT_SECRET:-}" && \
      -n "${GOOGLE_DRIVE_REFRESH_TOKEN:-}" ]]; then
    cat > "$DRIVE_TOKEN_FILE" << EOF
{
  "type": "authorized_user",
  "client_id": "$GOOGLE_DRIVE_CLIENT_ID",
  "client_secret": "$GOOGLE_DRIVE_CLIENT_SECRET",
  "refresh_token": "$GOOGLE_DRIVE_REFRESH_TOKEN",
  "quota_project_id": "crilo-prod-automation"
}
EOF
    echo "Drive credentials written to $DRIVE_TOKEN_FILE"
else
    echo "⚠  GOOGLE_DRIVE_CLIENT_ID / GOOGLE_DRIVE_CLIENT_SECRET / GOOGLE_DRIVE_REFRESH_TOKEN not all set."
    echo "   Skipping Drive auth file creation."
    echo "   To set them: https://jules.google.com/settings → Environment variables"
    echo ""
fi

# ── Step 3: Piste / MCP Bridge ─────────────────────────────────────────
if [[ -n "${PISTE_CREDENTIALS:-}" ]]; then
    echo "PISTE_CREDENTIALS detected → MCP Bridge ready"
else
    echo "⚠  PISTE_CREDENTIALS not set. MCP Bridge (Judilibre/Légifrance) unavailable."
    echo "   To set: https://jules.google.com/settings → Environment variables"
fi

# ── Step 4: Verify ─────────────────────────────────────────────────────
echo ""
echo "=== Verification ==="
echo "Python: $(uv run python3 --version)"
echo "Drive auth: $([ -f "$DRIVE_TOKEN_FILE" ] && echo 'CONFIGURED' || echo 'MISSING')"
echo "MCP Bridge: $([ -n "${PISTE_CREDENTIALS:-}" ] && echo 'CONFIGURED' || echo 'MISSING')"
echo "Legal library: $(ls lois/*.md 2>/dev/null | wc -l) fichiers .md"
echo "Target folder: ${GOOGLE_DRIVE_FOLDER_ID:-16Qm2fEzojRQ3_yylsSwlkynbVv1L0SvB}"
echo ""
echo "=== Ready ==="
echo ""
echo "Drive CLI usage examples:"
echo "  List files:     uv run python -m app.drive_client list"
echo "  Read Sheet:     uv run python -m app.drive_client read-sheet --sheet-id <ID>"
echo "  Upload file:    uv run python -m app.drive_client upload ./monfichier.pdf"
echo "  Export doc:     uv run python -m app.drive_client export <FILE_ID> --format markdown --print"
echo "  Search files:   uv run python -m app.drive_client search --name Assignation"
echo ""
echo "Bridge juridique:"
echo "  Check:          uv run python -m app.mcp_bridge.cli check"
echo "  Search Judi:    uv run python -m app.mcp_bridge.cli judilibre-search 'accident' --chamber civ1"
echo "  Search Légif:   uv run python -m app.mcp_bridge.cli legifrance-search 'article 1242' --fond CODE"
echo ""
echo "Legal library: cat lois/INDEX.md"
