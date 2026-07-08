#!/usr/bin/env python3
import json
import os
import stat
import sys
import urllib.request
import urllib.parse
from typing import Optional

sys.path.insert(0, "/home/crilocom/.opencode")
sys.path.insert(0, "/home/crilocom/.opencode/mcp-legifrance")
sys.path.insert(0, "/home/crilocom/.opencode/mcp-judilibre")

try:
    from souverain import get_secret
except ImportError:
    def get_secret(key):
        raise Exception(f"Secret {key} not found (souverain not installed)")

try:
    piste_creds = get_secret("PISTE_CREDENTIALS")
    os.environ["PISTE_CREDENTIALS"] = piste_creds
    os.environ["PISTE_ENV"] = "sandbox"
except Exception as e:
    print("Warning: Failed to setup PISTE credentials in tools initialization:", e)

try:
    from server import LegifranceClient as ServerLegifranceClient
except ImportError:
    ServerLegifranceClient = None

try:
    import server as judilibre_server
    ServerJudilibreClient = judilibre_server.JudilibreClient
except Exception:
    ServerJudilibreClient = None

CREDS_PATH = os.path.expanduser("~/.opencode/.gdrive-server-credentials.json")


def _get_gdrive_token() -> str:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    with open(CREDS_PATH) as f:
        saved = json.load(f)

    creds = Credentials(
        token=saved['access_token'],
        refresh_token=saved['refresh_token'],
        token_uri=saved.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=saved.get('client_id'),
        client_secret=saved.get('client_secret'),
        scopes=saved['scope'].split() if isinstance(saved['scope'], str) else saved['scope']
    )
    if not creds.valid:
        creds.refresh(Request())
        saved['access_token'] = creds.token
        saved['expiry_date'] = int(creds.expiry.timestamp() * 1000) if creds.expiry else 0
        with open(os.open(CREDS_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR), 'w') as f:
            json.dump(saved, f)
    return creds.token


def _gdrive_api_request(path: str, params: Optional[dict] = None, data: Optional[bytes] = None, method: str = "GET", headers: Optional[dict] = None) -> dict:
    token = _get_gdrive_token()
    url = f"https://www.googleapis.com/drive/v3/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req_headers = {"Authorization": f"Bearer {token}"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_jurisprudence(query: str) -> str:
    if not ServerJudilibreClient:
        return "Erreur : Client Judilibre non disponible."
    try:
        client = ServerJudilibreClient()
        result = client.search(query=query, page_size=5)
        decisions = result.get("results", [])
        if not decisions:
            return f"Aucune jurisprudence trouvée pour la recherche : '{query}'"
        output = [f"Résultats de recherche jurisprudence pour '{query}' ({result.get('total', 0)} résultats au total) :\n"]
        for idx, d in enumerate(decisions, 1):
            title = d.get("title", f"Décision n°{d.get('id')}")
            date = d.get("decisionDate", "Date inconnue")
            chamber = d.get("chamber", "Chambre inconnue")
            solution = d.get("solution", "Solution non spécifiée")
            highlights = d.get("highlights", {}).get("text", [])
            highlight_text = " / ".join(highlights) if highlights else "Pas d'extrait disponible"
            output.append(f"{idx}. {title}\n   - Date : {date} | Chambre : {chamber} | Solution : {solution}\n   - Extrait : {highlight_text}\n")
        return "\n".join(output)
    except Exception as e:
        return f"Erreur lors de la recherche de jurisprudence : {e}"


def search_law_code(query: str) -> str:
    if not ServerLegifranceClient:
        return "Erreur : Client Légifrance non disponible."
    try:
        client = ServerLegifranceClient()
        result = client.search(query=query, fond="CODE", page_size=5)
        articles = result.get("results", [])
        if not articles:
            return f"Aucun article de loi trouvé pour la recherche : '{query}'"
        output = [f"Résultats Légifrance pour '{query}' ({result.get('totalResultNumber', 0)} articles trouvés) :\n"]
        for idx, a in enumerate(articles, 1):
            article = a.get("article", {})
            num = article.get("num", "Non numéroté")
            text_title = a.get("texteTitle", "Texte inconnu")
            text_id = article.get("id", "ID inconnu")
            output.append(f"{idx}. Article {num} du {text_title}\n   - ID article : {text_id}\n")
        return "\n".join(output)
    except Exception as e:
        return f"Erreur lors de la recherche Légifrance : {e}"


def get_law_article(article_id: str) -> str:
    if not ServerLegifranceClient:
        return "Erreur : Client Légifrance non disponible."
    try:
        client = ServerLegifranceClient()
        result = client.consulte_article(article_id)
        article = result.get("article", {})
        if not article:
            return f"Article introuvable pour l'identifiant '{article_id}'."
        num = article.get("num", "Article sans numéro")
        text = article.get("texte", "Texte vide")
        output = f"Article {num} (ID: {article_id}) :\n\n{text}"
        return output
    except Exception as e:
        return f"Erreur lors de la récupération de l'article {article_id} : {e}"


def list_gdrive_folder(folder_id: str) -> str:
    try:
        q = f"'{folder_id}' in parents and trashed = false"
        data = _gdrive_api_request("files", params={"q": q, "fields": "files(id,name,mimeType,size)"})
        files = data.get("files", [])
        if not files:
            return "Le dossier est vide ou inaccessible."
        output = [f"Fichiers contenus dans le dossier (ID: {folder_id}) :\n"]
        for f in files:
            is_folder = f["mimeType"] == "application/vnd.google-apps.folder"
            icon = "[DOSSIER]" if is_folder else "[FICHIER]"
            size = f.get("size", "N/A")
            if size != "N/A":
                size = f"{int(size)//1024}KB" if int(size) > 1024 else f"{size}B"
            output.append(f"{icon} {f['name']} | Format: {f['mimeType']} | ID: {f['id']} | Taille: {size}")
        return "\n".join(output)
    except Exception as e:
        return f"Erreur lors du listing du dossier Google Drive : {e}"


def read_gdrive_file(file_id: str) -> str:
    try:
        meta = _gdrive_api_request(file_id, params={"fields": "name,mimeType"})
        mime_type = meta.get("mimeType", "")
        name = meta.get("name", "Document sans nom")
        token = _get_gdrive_token()
        if mime_type == "application/vnd.google-apps.document":
            url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
        elif mime_type == "application/vnd.google-apps.spreadsheet":
            url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        else:
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
        try:
            text_content = content.decode("utf-8")
        except UnicodeDecodeError:
            text_content = f"[Fichier binaire ou format non décodable en UTF-8. Taille : {len(content)} octets]"
        return f"Contenu de {name} ({mime_type}) :\n\n{text_content}"
    except Exception as e:
        return f"Erreur lors de la lecture du fichier Google Drive : {e}"
