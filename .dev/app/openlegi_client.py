"""OpenLegi MCP client — double verification of French legal references.

Connects to https://www.openlegi.fr/ (MCP proxy to Legifrance PISTE API)
for cross-checking articles, codes, and jurisprudence citations.
"""

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

import requests

def _get_openlegi_token() -> str | None:
    try:
        from souverain import get_secret
        val = get_secret("OPENLEGI_TOKEN")
        if val:
            return val
    except Exception:
        pass
    return os.environ.get("OPENLEGI_TOKEN")


@dataclass
class OpenLegiResult:
    text: str
    source_url: str | None = None
    title: str | None = None
    error: str | None = None


class OpenLegiClient:
    """Client for OpenLegi MCP (Légifrance proxy via SSE).

    Usage:
        with OpenLegiClient(token="...") as ol:
            result = ol.verify_article("LEGIARTI000006437044")
            print(result.text)
    """

    SERVICE_LEGIFRANCE = "legifrance"
    BASE_URL = "https://mcp.openlegi.fr"

    def __init__(
        self,
        token: str | None = None,
        service: str = SERVICE_LEGIFRANCE,
        timeout: int = 15,
    ):
        self.token = token or _get_openlegi_token()
        self.endpoint = f"{self.BASE_URL}/{service}/mcp"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self.token}",
        })
        self._session_id: str | None = None

    def _initialize(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "opencode-openlegi", "version": "1.0"},
            },
        }
        resp = self.session.post(self.endpoint, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        sid = resp.headers.get("mcp-session-id")
        if sid:
            self._session_id = sid
            self.session.headers.update({"mcp-session-id": sid})

    @staticmethod
    def _parse_sse(text: str) -> dict:
        for line in text.strip().split("\n"):
            if line.startswith("data: "):
                return json.loads(line[6:])
        raise ValueError("No data: line in SSE response")

    def _call(self, method: str, params: dict | None = None) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }
        resp = self.session.post(self.endpoint, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        result = self._parse_sse(resp.text)
        if "error" in result:
            raise ValueError(f"OpenLegi error: {result['error']}")
        return result["result"]

    def verify_article(self, article_id: str) -> OpenLegiResult:
        """Verify an article by LEGIARTI ID."""
        try:
            result = self._call("tools/call", {
                "name": "rechercher_code",
                "arguments": {
                    "search": article_id,
                    "code_name": "Code civil",
                    "champ": "NUM_ARTICLE",
                    "page_size": 1,
                },
            })
            content = result.get("content", [])
            text = json.dumps(content, ensure_ascii=False, indent=2) if content else "No results"
            return OpenLegiResult(text=text)
        except Exception as e:
            return OpenLegiResult(text="", error=str(e))

    def verify_article_by_number(self, article_num: str, code: str = "Code civil") -> OpenLegiResult:
        """Verify an article by number (e.g. '1240') within a code."""
        try:
            result = self._call("tools/call", {
                "name": "rechercher_code",
                "arguments": {
                    "search": article_num,
                    "code_name": code,
                    "champ": "NUM_ARTICLE",
                    "page_size": 1,
                },
            })
            content = result.get("content", [])
            text = json.dumps(content, ensure_ascii=False, indent=2) if content else "No results"
            return OpenLegiResult(text=text)
        except Exception as e:
            return OpenLegiResult(text="", error=str(e))

    def list_codes(self) -> list[str]:
        result = self._call("tools/call", {
            "name": "lister_codes_juridiques",
            "arguments": {},
        })
        content = result.get("content", [])
        return [item.get("text", "") for item in content if item.get("type") == "text"]

    def close(self):
        self.session.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self, *args):
        self.close()


def health_check(token: str | None = None) -> bool:
    """Quick health check via the public /health endpoint."""
    try:
        resp = requests.get(
            f"{OpenLegiClient.BASE_URL}/health",
            timeout=5,
        )
        data = resp.json()
        return data.get("status") == "ok" and data.get("services", {}).get("legifrance", False)
    except Exception:
        return False


if __name__ == "__main__":
    import sys

    if "--health" in sys.argv:
        ok = health_check()
        print(f"{'OK' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)

    with OpenLegiClient() as ol:
        codes = ol.list_codes()
        print(f"Codes disponibles: {len(codes)}")
        for c in codes[:10]:
            print(f"  - {c}")
        if len(codes) > 10:
            print(f"  ... et {len(codes) - 10} autres")
