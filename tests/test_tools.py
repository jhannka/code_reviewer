import os
import pytest
from unittest.mock import MagicMock, patch

from code_reviewer.ports.driven import VersionControlSystemPort, FileSystemPort, SkillsRepositoryPort
from code_reviewer.domain.use_cases import CodeReviewToolsService
from code_reviewer.adapters.driven.local_fs import LocalFileSystemAdapter
from code_reviewer.adapters.driven.local_skills import LocalSkillsRepositoryAdapter
from code_reviewer.adapters.driven.git_vcs import GitVCSAdapter
from code_reviewer.adapters.driving.tool_facade import (
    configure_facade,
    read_project_skills,
    get_git_changes,
    read_source_file,
    write_source_file
)

# ==========================================
# Domain Service Tests (Hexagonal Mocking)
# ==========================================

def test_code_review_service_delegates_to_ports():
    # Arrange
    vcs_mock = MagicMock(spec=VersionControlSystemPort)
    fs_mock = MagicMock(spec=FileSystemPort)
    skills_mock = MagicMock(spec=SkillsRepositoryPort)
    
    vcs_mock.get_git_changes.return_value = "mock git changes"
    fs_mock.read_file.return_value = "mock file content"
    fs_mock.write_file.return_value = "mock write status"
    skills_mock.read_all_skills.return_value = "mock skills content"
    
    service = CodeReviewToolsService(vcs_port=vcs_mock, fs_port=fs_mock, skills_port=skills_mock)
    
    # Act & Assert
    assert service.get_changes() == "mock git changes"
    vcs_mock.get_git_changes.assert_called_once_with(".")
    
    assert service.read_file("test_path") == "mock file content"
    fs_mock.read_file.assert_called_once_with("test_path")
    
    assert service.write_file("test_path", "new content") == "mock write status"
    fs_mock.write_file.assert_called_once_with("test_path", "new content")
    
    assert service.get_skills() == "mock skills content"
    skills_mock.read_all_skills.assert_called_once()


# ==========================================
# Driven Adapter Tests
# ==========================================

def test_local_fs_adapter_read_write(tmp_path):
    adapter = LocalFileSystemAdapter()
    test_file = tmp_path / "test.txt"
    content = "Hello, hex arch!"
    
    # Write
    write_res = adapter.write_file(str(test_file), content)
    assert "escrito correctamente" in write_res
    assert test_file.read_text(encoding="utf-8") == content
    
    # Read
    read_res = adapter.read_file(str(test_file))
    assert read_res == content

def test_local_fs_adapter_nonexistent():
    adapter = LocalFileSystemAdapter()
    read_res = adapter.read_file("nonexistent_file_path_123.txt")
    assert "Error leyendo el archivo" in read_res


@patch("os.path.exists")
@patch("os.path.isdir")
@patch("os.walk")
def test_local_skills_adapter_walks_directories(mock_walk, mock_isdir, mock_exists):
    # Arrange
    mock_exists.return_value = True
    mock_isdir.return_value = True
    mock_walk.return_value = [
        ("/mock/home/.gemini/config/skills/rule1", [], ["SKILL.md"])
    ]
    
    adapter = LocalSkillsRepositoryAdapter()
    
    # Mock open file behavior
    with patch("builtins.open", create=True) as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = "Rule 1 Content"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Act
        res = adapter.read_all_skills()
        
        # Assert
        assert "Rule 1 Content" in res
        assert "SKILL.md" in res


# ==========================================
# Driving Facade Tests
# ==========================================

def test_facade_delegates_to_configured_service():
    # Arrange
    service_mock = MagicMock(spec=CodeReviewToolsService)
    service_mock.get_skills.return_value = "facade skills"
    service_mock.get_changes.return_value = "facade changes"
    service_mock.read_file.return_value = "facade read"
    service_mock.write_file.return_value = "facade write"
    
    configure_facade(service_mock)
    
    # Act & Assert
    assert read_project_skills() == "facade skills"
    assert get_git_changes("dir") == "facade changes"
    assert read_source_file("path") == "facade read"
    assert write_source_file("path", "content") == "facade write"
