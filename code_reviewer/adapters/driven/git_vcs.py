import subprocess
from code_reviewer.ports.driven import VersionControlSystemPort

class GitVCSAdapter(VersionControlSystemPort):
    def get_git_changes(self, project_dir: str = ".") -> str:
        try:
            status_res = subprocess.run(
                ["git", "status", "-s"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            status_output = status_res.stdout.strip()
            
            if not status_output:
                return "No hay cambios pendientes de commit en el repositorio git."
                
            diff_res = subprocess.run(
                ["git", "diff"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            diff_output = diff_res.stdout.strip()
            
            return f"Git Status:\n{status_output}\n\nGit Diff:\n{diff_output}"
        except FileNotFoundError:
            return "Error: Comando git no encontrado en el sistema."
        except subprocess.CalledProcessError as e:
            return f"Error al ejecutar git en '{project_dir}': {e.stderr}"
        except Exception as e:
            return f"Error inesperado al obtener cambios de git: {str(e)}"
