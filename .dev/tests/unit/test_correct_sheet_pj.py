import os
import tempfile
import textwrap

import pytest

# Import the module to test
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))
import correct_sheet_pj


def create_md_file(tmp_dir, filename, uid, drive_id=None):
    content = textwrap.dedent(f"""
    ---
    uid: {uid}
    {f'drive_id: {drive_id}' if drive_id else ''}
    ---
    # Sample Document
    """)
    path = os.path.join(tmp_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def test_extract_uid_and_drive():
    with tempfile.TemporaryDirectory() as tmp:
        md_path = create_md_file(tmp, 'doc.md', 'UID123', 'DRIVE456')
        result = correct_sheet_pj.extract_uid_and_drive(md_path)
        assert result == {'uid': 'UID123', 'drive_id': 'DRIVE456'}

        md_path_no_drive = create_md_file(tmp, 'doc2.md', 'UID789')
        result = correct_sheet_pj.extract_uid_and_drive(md_path_no_drive)
        assert result == {'uid': 'UID789', 'drive_id': ''}


def test_build_uid_map(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        # Create sample markdown files in nested structure
        os.makedirs(os.path.join(tmp, 'subdir'), exist_ok=True)
        create_md_file(tmp, 'a.md', 'A1', 'D1')
        create_md_file(os.path.join(tmp, 'subdir'), 'b.md', 'B2')
        # Monkeypatch the TOKEN_DIR constant in the module
        monkeypatch.setattr(correct_sheet_pj, 'TOKEN_DIR', tmp)
        uid_map = correct_sheet_pj.build_uid_map()
        assert uid_map['A1']['path'] == 'a.md'
        assert uid_map['A1']['drive_id'] == 'D1'
        # Path should be relative with forward slashes
        assert uid_map['B2']['path'] == 'subdir/b.md'
        assert uid_map['B2']['drive_id'] == ''
