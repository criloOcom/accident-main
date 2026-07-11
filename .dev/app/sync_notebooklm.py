#!/usr/bin/env python3
"""
Sync documentation markdown files to Google Drive for NotebookLM.

Syncs these local folders:
  - ⚖️ Actes/👤 Reel/   → Accident Main - NotebookLM/Actes Reel/
  - 🧠 Memory/       → Accident Main - NotebookLM/Memory/
  - 📜 Lois/         → Accident Main - NotebookLM/Lois/

Usage:
  python3 .dev/app/sync_notebooklm.py          # real sync
  python3 .dev/app/sync_notebooklm.py --dry-run # preview only
"""

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.drive_auth import get_drive_service
from googleapiclient.http import MediaFileUpload

ROOT_FOLDER_NAME = "Accident Main - NotebookLM"

SOURCE_DIRS = {
    "Actes Reel": "⚖️ Actes/👤 Reel",
    "Memory": "🧠 Memory",
    "Lois": "📜 Lois",
}


def find_or_create_folder(service, name, parent_id=None):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    result = service.files().list(q=query, fields="files(id, name)").execute()
    files = result.get("files", [])
    if files:
        return files[0]["id"]
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        body["parents"] = [parent_id]
    folder = service.files().create(body=body, fields="id").execute()
    return folder["id"]


def list_files_in_folder(service, folder_id):
    all_files = {}
    page_token = None
    while True:
        result = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, mimeType, modifiedTime)",
            pageToken=page_token,
        ).execute()
        for f in result.get("files", []):
            all_files[f["name"]] = f
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return all_files


def local_mtime(path):
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def should_upload(local_path, drive_file):
    if drive_file is None:
        return True
    local_mod = local_mtime(local_path)
    drive_mod = datetime.fromisoformat(drive_file["modifiedTime"].replace("Z", "+00:00"))
    return local_mod > drive_mod


def sync_directory(service, local_root, drive_parent_id, dry_run):
    log = []
    local_root = os.path.abspath(local_root)
    if not os.path.isdir(local_root):
        return [f"⚠  SKIP: {local_root} not found"]

    drive_files = list_files_in_folder(service, drive_parent_id)
    local_files = {}
    for dirpath, _, filenames in os.walk(local_root):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            local_path = os.path.join(dirpath, fn)
            rel_sub = os.path.relpath(dirpath, local_root)
            subfolder_name = rel_sub if rel_sub != "." else None
            local_files.setdefault(subfolder_name, {})[fn] = local_path

    # Process subdirs: for each local subfolder, ensure Drive folder exists
    drive_subfolders = {}
    for name, meta in drive_files.items():
        if meta["mimeType"] == "application/vnd.google-apps.folder":
            drive_subfolders[name] = meta["id"]

    for subfolder_name, files in local_files.items():
        target_parent_id = drive_parent_id
        if subfolder_name:
            if subfolder_name in drive_subfolders:
                target_parent_id = drive_subfolders[subfolder_name]
            else:
                if dry_run:
                    log.append(f"  [DRY-RUN] Would create folder '{subfolder_name}'")
                    target_parent_id = "DRY_RUN_NEW_FOLDER"
                else:
                    target_parent_id = find_or_create_folder(service, subfolder_name, drive_parent_id)
                    drive_subfolders[subfolder_name] = target_parent_id
                    log.append(f"  + Folder '{subfolder_name}' created")

        sub_drive_files = list_files_in_folder(service, target_parent_id) if not dry_run else {}

        for fn, local_path in files.items():
            drive_file = sub_drive_files.get(fn) if not dry_run else None
            if not should_upload(local_path, drive_file):
                continue
            local_sz = os.path.getsize(local_path)
            if drive_file:
                if dry_run:
                    log.append(f"  [DRY-RUN] Would UPDATE '{fn}' ({local_sz} bytes)")
                else:
                    media = MediaFileUpload(local_path, mimetype="text/markdown", resumable=True)
                    service.files().update(fileId=drive_file["id"], media_body=media).execute()
                    log.append(f"  ✓ UPDATE '{fn}' ({local_sz} bytes)")
            else:
                if dry_run:
                    log.append(f"  [DRY-RUN] Would UPLOAD '{fn}' ({local_sz} bytes)")
                else:
                    media = MediaFileUpload(local_path, mimetype="text/markdown", resumable=True)
                    body = {"name": fn, "parents": [target_parent_id]}
                    service.files().create(body=body, media_body=media, fields="id").execute()
                    log.append(f"  + UPLOAD '{fn}' ({local_sz} bytes)")

        # Check for Drive files deleted locally
        for fn, meta in sub_drive_files.items():
            if fn not in files and meta["mimeType"] != "application/vnd.google-apps.folder":
                if dry_run:
                    log.append(f"  [DRY-RUN] Would DELETE '{fn}' (not in local)")
                else:
                    service.files().delete(fileId=meta["id"]).execute()
                    log.append(f"  ✗ DELETE '{fn}' (not in local)")

    return log


def main():
    parser = argparse.ArgumentParser(description="Sync markdown to Google Drive for NotebookLM")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying Drive")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    service = get_drive_service()
    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Authenticated to Google Drive.")

    root_id = find_or_create_folder(service, ROOT_FOLDER_NAME)
    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Root folder: '{ROOT_FOLDER_NAME}' (ID: {root_id})")

    total_uploads = 0
    total_deletes = 0

    for drive_sub, local_rel in SOURCE_DIRS.items():
        local_path = os.path.join(project_root, local_rel)
        print(f"\n── Syncing '{local_rel}' → '{ROOT_FOLDER_NAME}/{drive_sub}' ──")
        drive_sub_id = find_or_create_folder(service, drive_sub, root_id)
        print(f"  {'[DRY-RUN] ' if args.dry_run else ''}Drive folder ID: {drive_sub_id}")
        logs = sync_directory(service, local_path, drive_sub_id, args.dry_run)
        for line in logs:
            print(line)
            if "UPLOAD" in line or "UPDATE" in line:
                total_uploads += 1
            if "DELETE" in line:
                total_deletes += 1

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Summary: {total_uploads} uploads/updates, {total_deletes} deletions")
    if args.dry_run:
        print("(no changes were made)")
    else:
        print("Sync complete — Drive is up to date.")


if __name__ == "__main__":
    main()
