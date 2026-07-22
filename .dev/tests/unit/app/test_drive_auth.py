import pytest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
from app.drive_auth import (
    get_folder_id,
    _find_repo_root,
    get_credentials_from_env,
    get_credentials_from_file,
    get_credentials_from_adc,
    get_drive_service,
    FOLDER_ID_ENV,
    DEFAULT_FOLDER_ID,
    CLIENT_ID_ENV,
    CLIENT_SECRET_ENV,
    REFRESH_TOKEN_ENV,
    DRIVE_TOKEN_FILE,
)

def test_get_folder_id_from_env():
    with patch.dict(os.environ, {FOLDER_ID_ENV: "my-folder-id"}):
        assert get_folder_id() == "my-folder-id"

def test_get_folder_id_default():
    with patch.dict(os.environ, {}, clear=True):
        assert get_folder_id() == DEFAULT_FOLDER_ID

@patch("os.path.exists")
@patch("os.getcwd")
def test_find_repo_root_current_dir(mock_getcwd, mock_exists):
    mock_getcwd.return_value = "/path/to/repo"
    # Return True for current dir, False otherwise
    mock_exists.side_effect = lambda path: path == "/path/to/repo/setup.sh"

    assert _find_repo_root() == "/path/to/repo"

@patch("os.path.exists")
@patch("os.getcwd")
def test_find_repo_root_parent_dir(mock_getcwd, mock_exists):
    mock_getcwd.return_value = "/path/to/repo/subdir"
    # Return True for parent dir
    mock_exists.side_effect = lambda path: path == "/path/to/repo/setup.sh"

    assert _find_repo_root() == "/path/to/repo"

@patch("os.path.exists")
@patch("os.getcwd")
def test_find_repo_root_not_found(mock_getcwd, mock_exists):
    mock_getcwd.return_value = "/path/to/nowhere"
    mock_exists.return_value = False

    assert _find_repo_root() == "/path/to/nowhere"

def test_get_credentials_from_env_missing():
    with patch.dict(os.environ, {}, clear=True):
        assert get_credentials_from_env() is None

def test_get_credentials_from_env_success():
    env_vars = {
        CLIENT_ID_ENV: "my-client-id",
        CLIENT_SECRET_ENV: "my-client-secret",
        REFRESH_TOKEN_ENV: "my-refresh-token",
    }
    with patch.dict(os.environ, env_vars, clear=True):
        creds = get_credentials_from_env()
        assert creds is not None
        assert creds.client_id == "my-client-id"
        assert creds.client_secret == "my-client-secret"
        assert creds.refresh_token == "my-refresh-token"

@patch("app.drive_auth._find_repo_root")
@patch("os.path.exists")
def test_get_credentials_from_file_not_found(mock_exists, mock_find_repo_root):
    mock_find_repo_root.return_value = "/repo"
    mock_exists.return_value = False

    assert get_credentials_from_file() is None

@patch("app.drive_auth._find_repo_root")
@patch("os.path.exists")
def test_get_credentials_from_file_success(mock_exists, mock_find_repo_root):
    mock_find_repo_root.return_value = "/repo"
    mock_exists.return_value = True

    mock_data = {
        "client_id": "file-client-id",
        "client_secret": "file-client-secret",
        "refresh_token": "file-refresh-token",
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        creds = get_credentials_from_file()
        assert creds is not None
        assert creds.client_id == "file-client-id"
        assert creds.client_secret == "file-client-secret"
        assert creds.refresh_token == "file-refresh-token"

@patch("app.drive_auth._find_repo_root")
@patch("os.path.exists")
def test_get_credentials_from_file_exception(mock_exists, mock_find_repo_root):
    mock_find_repo_root.return_value = "/repo"
    mock_exists.return_value = True

    with patch("builtins.open", side_effect=Exception("Read error")):
        assert get_credentials_from_file() is None

@patch("google.auth.default")
@patch("google.auth.transport.requests.Request")
def test_get_credentials_from_adc_success(mock_request, mock_auth_default):
    mock_creds = MagicMock()
    mock_auth_default.return_value = (mock_creds, "project_id")

    creds = get_credentials_from_adc()

    assert creds == mock_creds
    mock_creds.refresh.assert_called_once()

@patch("google.auth.default")
def test_get_credentials_from_adc_exception(mock_auth_default):
    mock_auth_default.side_effect = Exception("ADC error")

    assert get_credentials_from_adc() is None

@patch("app.drive_auth.get_credentials_from_env")
@patch("app.drive_auth.discovery.build")
def test_get_drive_service_from_env(mock_build, mock_get_env):
    mock_creds = MagicMock()
    mock_get_env.return_value = mock_creds
    mock_build.return_value = "drive-service"

    service = get_drive_service()

    assert service == "drive-service"
    mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)

@patch("app.drive_auth.get_credentials_from_env")
@patch("app.drive_auth.get_credentials_from_file")
@patch("app.drive_auth.discovery.build")
def test_get_drive_service_from_file(mock_build, mock_get_file, mock_get_env):
    mock_get_env.return_value = None
    mock_creds = MagicMock()
    mock_get_file.return_value = mock_creds
    mock_build.return_value = "drive-service"

    service = get_drive_service()

    assert service == "drive-service"
    mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)

@patch("app.drive_auth.get_credentials_from_env")
@patch("app.drive_auth.get_credentials_from_file")
@patch("app.drive_auth.get_credentials_from_adc")
def test_get_drive_service_no_credentials(mock_get_adc, mock_get_file, mock_get_env):
    mock_get_env.return_value = None
    mock_get_file.return_value = None
    mock_get_adc.return_value = None

    import pytest
    with pytest.raises(RuntimeError, match="No Google Drive credentials found"):
        get_drive_service()
