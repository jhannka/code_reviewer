from abc import ABC, abstractmethod

class VersionControlSystemPort(ABC):
    @abstractmethod
    def get_git_changes(self, project_dir: str = ".") -> str:
        """Retrieve git status and diff for pending changes."""
        pass

class FileSystemPort(ABC):
    @abstractmethod
    def read_file(self, file_path: str) -> str:
        """Read content from a local file."""
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a local file, creating parent directories if needed."""
        pass

class SkillsRepositoryPort(ABC):
    @abstractmethod
    def read_all_skills(self) -> str:
        """Read all style guides, rules, and design patterns (skills) defined in system or project configurations."""
        pass
