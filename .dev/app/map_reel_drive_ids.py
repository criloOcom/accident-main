#!/usr/bin/env python3
"""
map_reel_drive_ids.py — Construit la table de correspondance
  chemin local Actes/Reel/... → drive_id du fichier MIROIR RÉEL sur Google Drive
  (dossier 'Accident Main - NotebookLM/Actes Reel/', alimenté par sync_notebooklm.py).

Sortie : .dev/app/_reel_drive_ids.json  { "Actes/Reel/x/y.md": "<drive_id>", ... }

Ce mapping est consommé par generate_breadcrumbs.py pour que l'émoji [📄]
des fichiers de la strate Réelle ouvre la VERSION RÉELLE sur Drive
(et surtout PAS le Google Docs tokenisé dont l'id figure dans le YAML).

Usage :
  python3 .dev/app/map_reel_drive_ids.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.drive_auth import get_drive_service  # noqa: E402

ROOT = "/home/crilocom/accident-main"
OUT = os.path.join(ROOT, ".dev", "app", "_reel_drive_ids.json")
ROOT_FOLDER_NAME = "Accident Main - NotebookLM"
REEL_FOLDER_NAME = "Actes Reel"


def list_children(svc, folder_id):
    files, token = [], None
    while True:
        resp = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id,name,mimeType)",
            pageSize=1000,
            pageToken=token,
        ).execute()
        files.extend(resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            return files


def main():
    svc = get_drive_service()
    r = svc.files().list(
        q=f"name='{ROOT_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id)",
    ).execute()["files"]
    if not r:
        print(f"ERREUR: dossier Drive '{ROOT_FOLDER_NAME}' introuvable", file=sys.stderr)
        sys.exit(1)
    root_id = r[0]["id"]
    reel = [f for f in list_children(svc, root_id)
            if f["name"] == REEL_FOLDER_NAME and f["mimeType"].endswith("folder")]
    if not reel:
        print(f"ERREUR: sous-dossier '{REEL_FOLDER_NAME}' introuvable", file=sys.stderr)
        sys.exit(1)

    mapping = {}

    def walk(folder_id, rel_prefix):
        for f in list_children(svc, folder_id):
            if f["mimeType"] == "application/vnd.google-apps.folder":
                walk(f["id"], os.path.join(rel_prefix, f["name"]))
            else:
                mapping[os.path.join("Actes/Reel", rel_prefix, f["name"]).replace("//", "/")] = f["id"]

    walk(reel[0]["id"], "")
    # Normalise les chemins (retire './')
    mapping = {os.path.normpath(k): v for k, v in mapping.items()}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"{len(mapping)} fichiers mappés → {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
