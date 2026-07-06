#!/usr/bin/env bash
# OpenLegi health check — verifie disponibilite du service
set -euo pipefail

HEALTH=$(curl -s --max-time 5 https://mcp.openlegi.fr/health 2>/dev/null || echo '{"status":"error"}')
STATUS=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','error'))" 2>/dev/null || echo "error")

if [ "$STATUS" = "ok" ]; then
    echo "OK — OpenLegi operationnel"
    echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
    exit 0
else
    echo "FAIL — OpenLegi indisponible"
    echo "$HEALTH"
    exit 1
fi
