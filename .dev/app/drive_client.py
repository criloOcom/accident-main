import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

#!/usr/bin/env python3
import argparse
import io
import json
import os
import sys
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from app.drive_auth import get_drive_service, get_folder_id
from googleapiclient import discovery


def cmd_list(args):
    service = get_drive_service()
    folder_id = args.folder_id or get_folder_id()
    query = f"'{folder_id}' in parents and trashed=false"
    if args.type:
        mime_map = {
            "document": "mimeType='application/vnd.google-apps.document'",
            "spreadsheet": "mimeType='application/vnd.google-apps.spreadsheet'",
            "folder": "mimeType='application/vnd.google-apps.folder'",
            "pdf": "mimeType='application/pdf'",
            "image": "mimeType contains 'image/'",
        }
        query += f" and {mime_map.get(args.type, f'mimeType contains \"{args.type}\"')}"
    fields = "files(id, name, mimeType, size, modifiedTime, webViewLink)"
    page_token = None
    files = []
    while True:
        result = (
            service.files()
            .list(
                q=query,
                spaces="drive",
                fields=f"nextPageToken, {fields}",
                pageToken=page_token,
                orderBy="modifiedTime desc",
            )
            .execute()
        )
        files.extend(result.get("files", []))
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    print(json.dumps(files, indent=2, ensure_ascii=False))
    return files


def cmd_upload(args):
    service = get_drive_service()
    folder_id = args.folder_id or get_folder_id()
    file_name = args.name or os.path.basename(args.local_path)
    mime_type = args.mime_type or "application/octet-stream"
    body = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(args.local_path, mimetype=mime_type, resumable=True)
    result = (
        service.files()
        .create(body=body, media_body=media, fields="id, name, mimeType, webViewLink")
        .execute()
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Uploaded: {result['webViewLink']}")


def cmd_download(args):
    service = get_drive_service()
    file_id = args.file_id
    out_path = args.output or file_id
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(out_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    print(f"Downloaded to: {out_path}")


def cmd_export(args):
    service = get_drive_service()
    file_id = args.file_id
    mime_map = {
        "markdown": "text/markdown",
        "txt": "text/plain",
        "html": "text/html",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    export_mime = mime_map.get(args.format, f"text/{args.format}")
    request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    out_path = args.output or f"{file_id}.{args.format}"
    with io.FileIO(out_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    if args.print:
        with open(out_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print(f"Exported to: {out_path}")


def cmd_create_folder(args):
    service = get_drive_service()
    parent_id = args.parent_id or get_folder_id()
    body = {
        "name": args.name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    result = service.files().create(body=body, fields="id, name, webViewLink").execute()
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_info(args):
    service = get_drive_service()
    result = (
        service.files()
        .get(fileId=args.file_id, fields="id, name, mimeType, size, modifiedTime, createdTime, webViewLink, parents, description")
        .execute()
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_read_sheet(args):
    service = get_drive_service()
    if args.sheet_id:
        range_str = args.range or "A1:Z1000"
        result = service.files().get(fileId=args.sheet_id, fields="name").execute()
        sheet_name = result["name"]
        sheets = discovery.build("sheets", "v4", credentials=service._http.credentials)
        try:
            data = sheets.spreadsheets().values().get(
                spreadsheetId=args.sheet_id, range=range_str
            ).execute()
        except Exception:
            data = sheets.spreadsheets().values().get(
                spreadsheetId=args.sheet_id, range=args.range or "A:Z"
            ).execute()
        rows = data.get("values", [])
        print(f"Sheet: {sheet_name}")
        print(f"Rows: {len(rows)}, Columns: {max(len(r) for r in rows) if rows else 0}")
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print("Error: --sheet-id required", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    service = get_drive_service()
    query_parts = []
    if args.name:
        query_parts.append(f"name contains '{args.name}'")
    if args.folder_id:
        query_parts.append(f"'{args.folder_id}' in parents")
    query_parts.append("trashed=false")
    query = " and ".join(query_parts)
    result = (
        service.files()
        .list(q=query, fields="files(id, name, mimeType, modifiedTime, webViewLink)")
        .execute()
    )
    files = result.get("files", [])
    print(json.dumps(files, indent=2, ensure_ascii=False))
    print(f"\nFound {len(files)} file(s)")


def main():
    parser = argparse.ArgumentParser(description="Google Drive client for Jules")
    parser.add_argument("--folder-id", help=f"Target folder ID (default: env {os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '') or '16Qm2f...'} )")

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List files in folder")
    p_list.add_argument("--type", help="Filter by type: document, spreadsheet, folder, pdf, image")
    p_list.set_defaults(func=cmd_list)

    p_up = sub.add_parser("upload", help="Upload a file")
    p_up.add_argument("local_path")
    p_up.add_argument("--name", help="Name in Drive (default: basename)")
    p_up.add_argument("--mime-type", default="application/octet-stream")
    p_up.set_defaults(func=cmd_upload)

    p_dl = sub.add_parser("download", help="Download a file by ID")
    p_dl.add_argument("file_id")
    p_dl.add_argument("--output", help="Output path")
    p_dl.set_defaults(func=cmd_download)

    p_ex = sub.add_parser("export", help="Export a Google Doc by ID")
    p_ex.add_argument("file_id")
    p_ex.add_argument("--format", default="markdown", help="Format: markdown, txt, html, pdf, docx")
    p_ex.add_argument("--output", help="Output path")
    p_ex.add_argument("--print", action="store_true", help="Print content to stdout")
    p_ex.set_defaults(func=cmd_export)

    p_cf = sub.add_parser("create-folder", help="Create a subfolder")
    p_cf.add_argument("name")
    p_cf.add_argument("--parent-id")
    p_cf.set_defaults(func=cmd_create_folder)

    p_info = sub.add_parser("info", help="Get file metadata")
    p_info.add_argument("file_id")
    p_info.set_defaults(func=cmd_info)

    p_rs = sub.add_parser("read-sheet", help="Read a Google Sheet")
    p_rs.add_argument("--sheet-id", required=True)
    p_rs.add_argument("--range", default="A1:Z1000", help="Sheet range (default: A1:Z1000)")
    p_rs.set_defaults(func=cmd_read_sheet)

    p_search = sub.add_parser("search", help="Search files by name")
    p_search.add_argument("--name", help="Search term in filename")
    p_search.add_argument("--folder-id")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
