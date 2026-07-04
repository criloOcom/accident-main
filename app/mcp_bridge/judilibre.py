import json
import os
import time
import urllib.parse

from . import (
    taxonomy_cache,
    decision_cache,
    judilibre_limiter,
    retry_with_backoff,
    handle_http_error,
    extract_zones,
    format_zones_for_display,
    format_highlights,
    offline_cache,
)


class JudilibreClient:
    def __init__(self):
        import requests
        creds = json.loads(os.environ["PISTE_CREDENTIALS"])
        p = creds["piste"]["production"]
        resp = requests.post(
            "https://oauth.piste.gouv.fr/api/oauth/token",
            data={"grant_type": "client_credentials", "client_id": p["client_id"], "client_secret": p["client_secret"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self._token = resp.json()["access_token"]
        self._base = "https://api.piste.gouv.fr/cassation/judilibre/v1.0"
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self._token}", "accept": "application/json"})

    def _make_request(self, url, params=None):
        def _do_request():
            judilibre_limiter.wait_if_needed()
            resp = self._session.get(url, params=params)
            if resp.status_code == 429:
                handle_http_error(429, "Rate limit exceeded")
            elif resp.status_code in (502, 503, 504):
                handle_http_error(resp.status_code, "Server temporarily unavailable")
            elif resp.status_code >= 500:
                handle_http_error(resp.status_code, f"Server error: {resp.status_code}")
            resp.raise_for_status()
            return resp.json()
        return retry_with_backoff(_do_request, max_retries=3, base_delay=1.0)

    def search(self, query, page=1, page_size=10, chamber=None, solution=None,
               jurisdiction=None, publication=None, date_from=None, date_to=None):
        params = {"query": query, "page": page, "pageSize": page_size}
        for k, v in [("chamber", chamber), ("solution", solution),
                     ("jurisdiction", jurisdiction), ("publication", publication)]:
            if v:
                params[k] = v
        url = f"{self._base}/search"
        if date_from or date_to:
            date_params = []
            if date_from:
                date_params.append(f"date_start={date_from}")
            if date_to:
                date_params.append(f"date_end={date_to}")
            if date_params:
                url += "?" + "&".join(date_params)
        return self._make_request(url, params)

    def get_decision(self, decision_id):
        cached = offline_cache.load(f"decision:{decision_id}")
        if cached:
            return cached
        cached = decision_cache.get(f"decision:{decision_id}")
        if cached:
            return cached
        result = self._make_request(f"{self._base}/decision", params={"id": decision_id, "resolve_references": "true"})
        decision_cache.set(f"decision:{decision_id}", result, ttl=86400)
        offline_cache.save(f"decision:{decision_id}", result, ttl=86400)
        return result

    def get_taxonomy(self, taxonomy_id, context_value=None):
        cache_key = f"taxonomy:{taxonomy_id}:{context_value or ''}"
        cached = taxonomy_cache.get(cache_key)
        if cached:
            return cached
        params = {"id": taxonomy_id}
        if context_value:
            params["context_value"] = context_value
        result = self._make_request(f"{self._base}/taxonomy", params)
        taxonomy_cache.set(cache_key, result, ttl=3600)
        return result

    def get_stats(self, jurisdiction=None):
        params = {}
        if jurisdiction:
            params["jurisdiction"] = jurisdiction
        return self._make_request(f"{self._base}/stats", params)
