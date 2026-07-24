#!/usr/bin/env python3
"""
sync_reel_gdocs.py — Réciprocité totale strate Réelle ↔ Google Docs.

Pour CHAQUE fichier .md de Actes/Reel/ :
  1. Cherche `reel_drive_id` dans le YAML (Reel puis Token miroir).
  2. Si absent/invalide → crée le Google Doc (conversion markdown native Drive)
     dans le dossier Drive « Accident Main - Docs Reel/ » (arborescence miroir),
     puis écrit `reel_drive_id` dans le YAML du fichier TOKEN miroir (Token-first,
     Règle #22) ET du fichier Reel (même valeur, cohérence immédiate).
  3. Si présent → met à jour le contenu du Google Doc depuis le .md Réel.

Le champ `drive_id` existant (qui pointe vers le Google Docs TOKENISÉ) n'est
JAMAIS modifié. `generate_breadcrumbs.py` utilise `reel_drive_id` en priorité
pour l'émoji [📄] de la strate Réelle.

Usage :
  python3 .dev/app/sync_reel_gdocs.py            # dry-run
  python3 .dev/app/sync_reel_gdocs.py --apply    # crée/synchronise réellement
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.drive_auth import get_drive_service  # noqa: E402
from googleapiclient.http import MediaIoBaseUpload  # noqa: E402

ROOT = "/home/crilocom/accident-main"
REEL_BASE = os.path.join(ROOT, "Actes", "Reel")
TOKEN_BASE = os.path.join(ROOT, "Actes", "Token")
DRIVE_ROOT_NAME = "Accident Main - Docs Reel"
VALID_ID = re.compile(r"^[A-Za-z0-9_-]{10,}$")
DOC_MIME = "application/vnd.google-apps.document"
FOLDER_MIME = "application/vnd.google-apps.folder"


def read_yaml_field(path, field):
    if not os.path.isfile(path):
        return None
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
    if not m:
        return None
    fm = re.search(r"^" + re.escape(field) + r":\s*(.+?)\s*$", m.group(1), re.MULTILINE)
    return fm.group(1).strip().strip('"').strip("'") if fm else None


def set_yaml_field(path, field, value):
    """Ajoute/remplace un champ scalaire dans le frontmatter YAML. True si écrit."""
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?\n)---", txt, re.DOTALL)
    if not m:
        return False
    fm = m.group(1)
    line = f"{field}: {value}\n"
    if re.search(r"^" + re.escape(field) + r":", fm, re.MULTILINE):
        new_fm = re.sub(r"^" + re.escape(field) + r":.*$", line.rstrip("\n"), fm, flags=re.MULTILINE)
    else:
        new_fm = fm + line
    new_txt = txt[: m.start(1)] + new_fm + txt[m.end(1):]
    open(path, "w", encoding="utf-8").write(new_txt)
    return True


def find_or_create_folder(svc, name, parent_id, cache, dry):
    key = (parent_id, name)
    if key in cache:
        return cache[key]
    safe = name.replace("'", "\\'")
    q = f"name='{safe}' and mimeType='{FOLDER_MIME}' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    files = svc.files().list(q=q, fields="files(id)").execute().get("files", [])
    if files:
        cache[key] = files[0]["id"]
        return files[0]["id"]
    if dry:
        cache[key] = "DRY_RUN_FOLDER"
        return cache[key]
    body = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        body["parents"] = [parent_id]
    fid = svc.files().create(body=body, fields="id").execute()["id"]
    cache[key] = fid
    return fid


def clean_markdown_for_gdocs(txt: str) -> str:
    """Purge le bloc YAML frontmatter, le fil d'Ariane et les icônes de bibliothèque locale [📚] avant l'export vers Google Docs."""
    # 1. Purger le bloc YAML frontmatter au début (--- ... ---)
    txt = re.sub(r"^---\s*\n.*?\n---\s*\n?", "", txt, flags=re.DOTALL)
    # 2. Purger le bloc fil d'Ariane (<!-- Breadcrumb --> ... <!-- /Breadcrumb -->) et les <hr> éventuels qui suivent
    txt = re.sub(r"<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->\s*(<hr>\s*)?", "", txt, flags=re.DOTALL)
    # 3. Purger toute ligne de fil d'Ariane Markdown non balisée (*[🏠...)
    txt = re.sub(r"^\*?\[?🏠.*?\n", "", txt, flags=re.MULTILINE)
    # 4. Purger les icônes de bibliothèque locale [📚](...) et leurs liens locaux Markdown
    txt = re.sub(r"\s*\[📚\]\(.*?\)", "", txt)
    # 5. Nettoyer les sauts de ligne initiaux
    txt = txt.lstrip("\n")
    return txt


def md_media(path):
    raw_txt = open(path, encoding="utf-8").read()
    clean_txt = clean_markdown_for_gdocs(raw_txt)
    data = clean_txt.encode("utf-8")
    return MediaIoBaseUpload(io.BytesIO(data), mimetype="text/markdown", resumable=False)


def main():
    dry = "--apply" not in sys.argv
    svc = get_drive_service()
    cache = {}
    root_id = find_or_create_folder(svc, DRIVE_ROOT_NAME, None, cache, dry)

    created, updated, skipped, errors = 0, 0, 0, []
    for dp, dn, fn in os.walk(REEL_BASE):
        dn.sort()
        for f in sorted(fn):
            if not f.endswith(".md") or f == "README.md":
                continue
            reel_path = os.path.join(dp, f)
            rel = os.path.relpath(reel_path, REEL_BASE)
            token_path = os.path.join(TOKEN_BASE, rel)

            rid = (
                read_yaml_field(reel_path, "reel_drive_id")
                or read_yaml_field(reel_path, "drive_id")
                or read_yaml_field(token_path, "reel_drive_id")
                or read_yaml_field(token_path, "drive_id")
            )
            if rid and not VALID_ID.match(rid):
                rid = None

            # Vérifie l'existence réelle du doc si ID connu
            if rid and not dry:
                try:
                    meta = svc.files().get(fileId=rid, fields="id,trashed").execute()
                    if meta.get("trashed"):
                        rid = None
                except Exception:
                    rid = None

            try:
                if rid:
                    if dry:
                        skipped += 1
                    else:
                        svc.files().update(fileId=rid, media_body=md_media(reel_path)).execute()
                        updated += 1
                else:
                    if dry:
                        print(f"[DRY] CREATE {rel}")
                        created += 1
                        continue
                    # Dossier Drive miroir
                    parent = root_id
                    for seg in os.path.dirname(rel).split(os.sep):
                        if seg:
                            parent = find_or_create_folder(svc, seg, parent, cache, dry)
                    body = {
                        "name": os.path.splitext(f)[0],
                        "mimeType": DOC_MIME,
                        "parents": [parent],
                    }
                    new_id = svc.files().create(
                        body=body, media_body=md_media(reel_path), fields="id"
                    ).execute()["id"]
                    # Token-first : écrire dans le Token miroir, puis refléter dans le Reel
                    if os.path.isfile(token_path):
                        set_yaml_field(token_path, "reel_drive_id", new_id)
                        if not read_yaml_field(token_path, "drive_id"):
                            set_yaml_field(token_path, "drive_id", new_id)
                    set_yaml_field(reel_path, "reel_drive_id", new_id)
                    if not read_yaml_field(reel_path, "drive_id"):
                        set_yaml_field(reel_path, "drive_id", new_id)
                    created += 1
                    print(f"  + CREATE {rel} → {new_id}")
            except Exception as e:
                errors.append((rel, str(e)))
                print(f"  ✗ ERREUR {rel}: {e}")

    print(f"\nMODE: {'DRY-RUN' if dry else 'APPLY'}")
    print(f"créés: {created} | mis à jour: {updated} | inchangés (dry): {skipped} | erreurs: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

