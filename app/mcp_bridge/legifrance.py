import json
import os

from pylegifrance import LegifranceClient as PylegifranceClient
from pylegifrance import ApiConfig
from pylegifrance.models.generated.model import (
    SearchRequestDTO, RechercheSpecifiqueDTO, ChampDTO, CritereDTO,
    Operateur, TypeChamp, TypeRecherche, TypePagination, Fond,
    JuriConsultRequest, ConsultRequest,
)
from pylegifrance.utils import EnumEncoder

from . import (
    legifrance_limiter,
    retry_with_backoff,
    handle_http_error,
    offline_cache,
)


PISTE_URLS = {
    "sandbox": {
        "oauth": "https://sandbox-oauth.piste.gouv.fr/api/oauth/token",
        "api": "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app/",
    },
    "production": {
        "oauth": "https://oauth.piste.gouv.fr/api/oauth/token",
        "api": "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/",
    },
}


def _strip_nulls(d):
    if isinstance(d, dict):
        return {k: _strip_nulls(v) for k, v in d.items() if v is not None}
    if isinstance(d, list):
        return [_strip_nulls(v) for v in d]
    return d


class LegifranceClient:
    def __init__(self):
        env = os.environ.get("PISTE_ENV", "sandbox")
        creds = json.loads(os.environ["PISTE_CREDENTIALS"])
        p = creds["piste"][env]
        urls = PISTE_URLS[env]
        self._client = PylegifranceClient(
            ApiConfig(
                client_id=p["client_id"],
                client_secret=p["client_secret"],
                token_url=urls["oauth"],
                api_url=urls["api"],
            )
        )

    def _make_request(self, api_name, payload):
        def _do_request():
            legifrance_limiter.wait_if_needed()
            resp = self._client.call_api(api_name, payload)
            if hasattr(resp, 'status_code'):
                if resp.status_code == 429:
                    handle_http_error(429, "Rate limit exceeded")
                elif resp.status_code in (502, 503, 504):
                    handle_http_error(resp.status_code, "Server temporarily unavailable")
                elif resp.status_code >= 500:
                    handle_http_error(resp.status_code, f"Server error: {resp.status_code}")
            return resp.json()
        return retry_with_backoff(_do_request, max_retries=3, base_delay=1.0)

    def search(self, query, fond, page_size=5, page_number=1):
        fond_map = {
            "JURI": Fond.juri, "CODE": Fond.code_etat, "LODA": Fond.loda_etat,
            "KALI": Fond.kali, "CNIL": Fond.cnil, "CONSTIT": Fond.constit, "JUF": Fond.jufi,
        }
        criteria = CritereDTO(valeur=query, operateur=Operateur.et,
                              typeRecherche=TypeRecherche.un_des_mots, proximite=None, criteres=None)
        champ = ChampDTO(criteres=[criteria], operateur=Operateur.et, typeChamp=TypeChamp.all)
        spec = RechercheSpecifiqueDTO(
            champs=[champ], filtres=[], pageNumber=page_number, pageSize=page_size,
            sort="PERTINENCE", fromAdvancedRecherche=False, secondSort="ID",
            typePagination=TypePagination.defaut, operateur=Operateur.et,
        )
        request = SearchRequestDTO(recherche=spec, fond=fond_map.get(fond, Fond.juri))
        payload = request.model_dump(by_alias=True)
        payload = json.loads(json.dumps(payload, cls=EnumEncoder))
        payload = _strip_nulls(payload)
        return self._make_request("search", payload)

    def consulte_decision(self, text_id):
        cached = offline_cache.load(f"legifrance:{text_id}")
        if cached:
            return cached
        payload = JuriConsultRequest(textId=text_id, searchedString="").model_dump(by_alias=True, exclude_none=True)
        result = self._make_request("consult/juri", payload)
        offline_cache.save(f"legifrance:{text_id}", result, ttl=86400)
        return result

    def consulte_texte(self, text_id):
        cached = offline_cache.load(f"legifrance:texte:{text_id}")
        if cached:
            return cached
        payload = ConsultRequest(textId=text_id).model_dump(by_alias=True, exclude_none=True)
        result = self._make_request("consult/texte", payload)
        offline_cache.save(f"legifrance:texte:{text_id}", result, ttl=86400)
        return result

    def consulte_article(self, text_id):
        cached = offline_cache.load(f"legifrance:article:{text_id}")
        if cached:
            return cached
        payload = ConsultRequest(textId=text_id).model_dump(by_alias=True, exclude_none=True)
        result = self._make_request("consult/code", payload)
        offline_cache.save(f"legifrance:article:{text_id}", result, ttl=86400)
        return result
