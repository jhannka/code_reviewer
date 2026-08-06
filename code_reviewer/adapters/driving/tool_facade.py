from code_reviewer.domain.use_cases import CodeReviewToolsService

# Global service instance that will be configured by the composition root
_service: CodeReviewToolsService = None

def configure_facade(service: CodeReviewToolsService):
    global _service
    _service = service

def read_project_skills() -> str:
    """Reads all style guides, rules, and design patterns (skills) defined in the global configurations or project configurations.
    
    Returns:
        A formatted string containing the content of all found design guidelines and skills.
    """
    if _service is None:
        raise RuntimeError("Tool facade is not configured. Call configure_facade first.")
    return _service.get_skills()

def get_git_changes(project_dir: str = ".") -> str:
    """Gets the git status and git diff showing all pending modifications that are not yet committed.
    
    Args:
        project_dir: The root directory of the project to check git changes for. Defaults to current directory.
        
    Returns:
        A string containing the git status and diff output.
    """
    if _service is None:
        raise RuntimeError("Tool facade is not configured. Call configure_facade first.")
    return _service.get_changes(project_dir)

def read_source_file(file_path: str) -> str:
    """Reads the complete contents of a source code file.
    
    Args:
        file_path: The relative or absolute path to the file to read.
        
    Returns:
        The content of the file or an error message if it cannot be read.
    """
    if _service is None:
        raise RuntimeError("Tool facade is not configured. Call configure_facade first.")
    return _service.read_file(file_path)

def write_source_file(file_path: str, content: str) -> str:
    """Writes or overwrites a source code file with new contents. 
    Use this only when you are applying approved refactorings or code fixes.
    
    Args:
        file_path: The relative or absolute path to the file to write.
        content: The new contents of the file.
        
    Returns:
        A status message indicating success or failure.
    """
    if _service is None:
        raise RuntimeError("Tool facade is not configured. Call configure_facade first.")
    return _service.write_file(file_path, content)
