from code_reviewer.ports.driven import VersionControlSystemPort, FileSystemPort, SkillsRepositoryPort

class CodeReviewToolsService:
    def __init__(
        self,
        vcs_port: VersionControlSystemPort,
        fs_port: FileSystemPort,
        skills_port: SkillsRepositoryPort
    ):
        self._vcs_port = vcs_port
        self._fs_port = fs_port
        self._skills_port = skills_port

    def get_skills(self) -> str:
        return self._skills_port.read_all_skills()

    def get_changes(self, project_dir: str = ".") -> str:
        return self._vcs_port.get_git_changes(project_dir)

    def read_file(self, file_path: str) -> str:
        return self._fs_port.read_file(file_path)

    def write_file(self, file_path: str, content: str) -> str:
        return self._fs_port.write_file(file_path, content)
