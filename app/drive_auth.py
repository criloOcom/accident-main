import json
import os
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient import discovery

DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

FOLDER_ID_ENV = "GOOGLE_DRIVE_FOLDER_ID"
CLIENT_ID_ENV = "GOOGLE_DRIVE_CLIENT_ID"
CLIENT_SECRET_ENV = "GOOGLE_DRIVE_CLIENT_SECRET"
REFRESH_TOKEN_ENV = "GOOGLE_DRIVE_REFRESH_TOKEN"

DEFAULT_FOLDER_ID = "16Qm2fEzojRQ3_yylsSwlkynbVv1L0SvB"
DRIVE_TOKEN_FILE = ".drive-token.json"


def get_folder_id():
    return os.environ.get(FOLDER_ID_ENV) or DEFAULT_FOLDER_ID


def _find_repo_root():
    cwd = os.getcwd()
    for parent in [cwd] + [os.path.dirname(cwd)]:
        if os.path.exists(os.path.join(parent, "setup.sh")):
            return parent
    return cwd


def get_credentials_from_env():
    client_id = os.environ.get(CLIENT_ID_ENV)
    client_secret = os.environ.get(CLIENT_SECRET_ENV)
    refresh_token = os.environ.get(REFRESH_TOKEN_ENV)
    if client_id and client_secret and refresh_token:
        return Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=DRIVE_SCOPES,
        )
    return None


def get_credentials_from_file():
    file_path = os.path.join(_find_repo_root(), DRIVE_TOKEN_FILE)
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path) as f:
            data = json.load(f)
        return Credentials(
            token=None,
            refresh_token=data.get("refresh_token") or data.get("refreshToken"),
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            token_uri=data.get("token_uri", "https://oauth2.googleapis.com/token"),
            scopes=DRIVE_SCOPES,
        )
    except Exception:
        return None


def get_credentials_from_adc():
    try:
        creds, _ = google.auth.default(scopes=DRIVE_SCOPES)
        req = google.auth.transport.requests.Request()
        creds.refresh(req)
        return creds
    except Exception:
        return None


def get_drive_service():
    creds = get_credentials_from_env() or get_credentials_from_file() or get_credentials_from_adc()
    if not creds:
        raise RuntimeError(
            "No Google Drive credentials found. "
            f"Set {CLIENT_ID_ENV}, {CLIENT_SECRET_ENV}, {REFRESH_TOKEN_ENV} "
            f"or ensure {DRIVE_TOKEN_FILE} exists (from setup.sh)."
        )
    return discovery.build("drive", "v3", credentials=creds)
